import sys
import can
import can.interfaces.slcan
import threading
import os
from os.path import abspath, dirname, join
from datetime import datetime, date
import time
from textwrap import wrap

from PyQt5 import QtCore, QtGui, QtQml
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer
from PyQt5.QtQuick import QQuickView

from vars import *

def radioFunctions():
    global rdsText, isSeeking, source, freq, stationMem, modType, radioBand, volume, radioPower, showAudioMenu, srcImage
    if not radioPower:
        rdsText = "Radio Off"
        freq = ""
        radioBand = ""
        modType = ""
        stationMem = ""
        srcImage = "power_off.png"
    else:
        if source == "AUX":
            rdsText = "Playing from AUX"
            freq = ""
            radioBand = ""
            modType = ""
            stationMem = ""
            srcImage = "aux_cable.png"
        elif source == "CD":
            if discType == "Audio CD":
                rdsText = "Track " + str(cdCurrentTrack) +" / " + str(trackAll)
                freq = currentTrackTime
                radioBand = discType
                modType = ""
                stationMem = ""
            else:
                rdsText = cdTrackDetails[1][:25]
                freq = cdTrackDetails[0]
                radioBand = discType
                modType = ""
                stationMem = currentTrackTime
        elif source == "Radio":
            srcImage = "radio.png"
        elif source == "USB":
            rdsText = usbTrackName[1][:25]
            freq = usbTrackName[0]
            radioBand =  current_time_USB
            modType = ""
            srcImage = "usb.png"
            stationMem = ""

    if isLRBal or isRFBal or isBass or isTreble or isLoudness or isAutoVol or isEQPreset:
        showAudioMenu = True
    else:
        showAudioMenu = False

def tripFunction():
    global tripImage
    if tripMode == 0:
        tripImage = ["trip_gasstation.png", "trip_fuel.png", "trip_distance.png"]
    if tripMode == 1:
        tripImage = ["trip_fuel.png", "trip_gasstation.png","trip_distance.png"]

def canSend():
    global menuItem
    #Main Menu task (Fix shit code later)
    msgList = can.Message(arbitration_id=0x09F, data=[0x30, 0x00, 0x0A], is_extended_id=False)
    print (menuItem)
    if menuItem == "List":
        bus.send(msgList)
        menuItem = "None"
    


#Send Audio Settings only if menu visible to cut overall delay
def sendAudioValues():
    #Show Setting
    engine.rootObjects()[0].setProperty('isBass', isBass)
    engine.rootObjects()[0].setProperty('isTreble', isTreble)
    engine.rootObjects()[0].setProperty('isLoudness', isLoudness)
    engine.rootObjects()[0].setProperty('isAutoVol', isAutoVol)
    engine.rootObjects()[0].setProperty('isRFBal', isRFBal)
    engine.rootObjects()[0].setProperty('isLRBal', isLRBal)
    engine.rootObjects()[0].setProperty('isEQPreset', isEQPreset)
    #Send Value
    engine.rootObjects()[0].setProperty('bassValue', bassValue)
    engine.rootObjects()[0].setProperty('trebleValue', trebleValue)
    engine.rootObjects()[0].setProperty('loudValue', loudValue)
    engine.rootObjects()[0].setProperty('autoVolValue', autoVolValue)
    engine.rootObjects()[0].setProperty('rfValue', rfValue)
    engine.rootObjects()[0].setProperty('lrValue', lrValue)
    engine.rootObjects()[0].setProperty('eqPresetValue', eqPresetValue)

def sendList():
    engine.rootObjects()[0].setProperty('trackList', trackList)
    engine.rootObjects()[0].setProperty('trackListSel', trackListSel)

def canRead():
    #bus = can.Bus(interface='slcan', channel='COM10', receive_own_messages=True)
    global bus
    bus = can.ThreadSafeBus(interface='slcan', channel='COM4')
    #Define stuff
    global rdsText, isSeeking, source, freq, stationMem, modType, radioBand, volume, isVolumeChanging, isVolumeStillChanging, radioPower, isLRBal, isRFBal, isBass, isTreble, isLoudness, isAutoVol, isEQPreset
    global lrValue, rfValue, bassValue, trebleValue, loudValue, autoVolValue, eqPresetValue
    global trackAll, discType, srcImage, cdCurrentTrack, currentTrackTime, menuItem, showMainMenu, current_time_USB, theID, usbTrackName, cdTrackDetails, trackList, showList, trackListSel
    global tripInfo, darkMode, tripMode
    curr_timer = time.time()
    frameNum = 0
    usbName = ""
    frameLen = 0
    cdframeNum = 0
    cdframeLen = 0
    cdName = ""
    bigList = ""
    bigListSplit = ""
    initialList = True
    tripMode = 0
    for msg in bus:
        id = msg.arbitration_id
        if id == 0x123:
            message = msg.data
            messageAsc = message.hex(" ")
            print (messageAsc)
            
        #This one gets the RDS text (if available) and displays it. PSA did us a solid and is sending it in ASCII. Thanks French Gods
        if id == 677 and radioPower:
            rdsbytearr = msg.data
            if rdsbytearr == b'\x00\x00\x00\x00\x00\x00\x00\x00':
                rdsText = "No RDS Available"
            else:
                rdsText = rdsbytearr.decode()
        #This one is for the radio's Band Display (FM1,etc) and displaying if we are using MHz or KHz
        elif id == 549 and radioPower:
            radioStatusarr = msg.data
            radioStatus = radioStatusarr.hex('#')
            radioHex = radioStatusarr.hex()
            scale = 16
            bitNum = 8
            
            radioSplit = radioStatus.split("#")
            radioStr = [bin(int(n, 16))[2:].zfill(bitNum) for n in radioSplit]
            if str(radioSplit[2]) == "10":
                radioBand = "FM-1"
                modType = "MHz"
            elif str(radioSplit[2]) == "20":
                radioBand = "FM-2"
                modType = "MHz"
            elif str(radioSplit[2]) == "40":
                radioBand = "FM-AST"
                modType = "MHz"
            elif str(radioSplit[2]) == "50":
                radioBand = "AM"
                modType = "KHz"
            freqHex = radioSplit[3] + radioSplit[4]
            freq = int(freqHex, 16)
            freq = (freq * 0.05) + 50
            freq = "%.2f" % freq
            memHex = radioSplit[1]
            stationMemarr = list(str(memHex))
            stationMem = stationMemarr[0]
        #This one reads the Source frame and displays accordingly. Added BT and USB just so you don't have to
        elif id == 357:
            sourcearr = msg.data
            sourceHex = sourcearr.hex('#')
            sourceSplit = sourceHex.split("#")
            if sourceSplit[2] == "10":
                source = "Radio"
            elif sourceSplit[2] == "20":
                source = "CD"
            elif sourceSplit[2] == "40":
                source = "AUX"
            elif sourceSplit[2] == "60":
                source = "USB"
            elif sourceSplit[2] == "70":
                source = "Bluetooth"
            if sourceSplit[0] == "40":
                #Set if Power is off. Everything else is on
                radioPower = False
            elif sourceSplit[0] == "E0":
                radioPower = True
                #Add mute state
            else:
                radioPower = True
            
        #Gets the volume frame, turns HEX to Binary, splits the first 3 bits that tell us if the volume is currently being changed and translates the rest to integer
        elif id == 421:
            volarr = msg.data
            volHex = volarr.hex()
            scale = 16
            bitNum = 8
            volStr = bin(int(volHex, scale))[2:].zfill(bitNum)
            volume = int(volStr[3:], 2)
            if volStr[:3] == "000":
                isVolumeChanging = True
                isVolumeStillChanging = True
                curr_timer = time.time()
                msgFCF = can.Message(arbitration_id=0x525, data=[0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00], is_extended_id=False)
                bus.send(msgFCF)
                msgFCF = can.Message(arbitration_id=0x52E, data=[0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00], is_extended_id=False)
                bus.send(msgFCF)
                msgFCF = can.Message(arbitration_id=0x52F, data=[0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00], is_extended_id=False)
                bus.send(msgFCF)
            else:
                isVolumeStillChanging = False
            if (time.time() - curr_timer) >= 2:
                isVolumeChanging = False
        #This long-ass code handles the audio settings menu
        elif id == 485:
            scale = 16
            bitNum = 8
            soundSetarr = msg.data
            soundSetHex = soundSetarr.hex("#")
            splits = soundSetHex.split("#")
            soundSetBin = [bin(int(n, 16))[2:].zfill(bitNum) for n in splits]
            #Left-Right Balance
            if soundSetBin[0][0] == "1":
                isLRBal = True
            else:
                isLRBal = False
            if soundSetBin[1][0] == "1":
                isRFBal = True
            else:
                isRFBal = False
            if soundSetBin[2][0] == "1":
                isBass = True
            else:
                isBass = False
            if soundSetBin[4][0] == "1":
                isTreble = True
            else:
                isTreble = False
            if soundSetBin[5][0] == "1":
                isLoudness = True
            else:
                isLoudness = False
            if soundSetBin[5][3] == "1":
                isAutoVol = True
            else:
                isAutoVol = False
            if soundSetBin[6][1] == "1":
                isEQPreset = True
            else:
                isEQPreset = False
            #Handle the values and send them over, regardless of menu visibility
            lrValue = int(soundSetBin[0][1:], 2) - 63
            rfValue = int(soundSetBin[1][1:], 2) - 63
            bassValue = int(soundSetBin[2][1:], 2) - 63
            trebleValue = int(soundSetBin[4][1:], 2) - 63
            loudValue = int(soundSetBin[5][1])
            autoVolValue = int(soundSetBin[5][5:])
            #Set EQ text
            eqBin = int(soundSetBin[6][3:], 2)
            if eqBin == 3:
                eqPresetValue = "None"
            elif eqBin == 7:
                eqPresetValue = "Classical"
            elif eqBin == 11:
                eqPresetValue = "Jazz-Blues"
            elif eqBin == 15:
                eqPresetValue = "Pop-Rock"
            elif eqBin == 19:
                eqPresetValue = "Vocal"
            elif eqBin == 23:
                eqPresetValue = "Techno"
        elif id == 869:
            cdPresenceInfo = (msg.data).hex("#")
            cdPresenceSplit = cdPresenceInfo.split("#")
            trackAll = int(cdPresenceSplit[0], 16)
            if trackAll == 255:
                cdCurrentTrack = "--"
            if str(cdPresenceSplit[3]) == "01":
                discType = "MP3 Disc"
                srcImage = "cd_mp3.png"
            else:
                discType = "Audio CD"
                srcImage = "cd_audio.png"
        elif id == 933 and source == "CD":
            cdTrackHex = (msg.data).hex("#")
            cdTrackSplit = cdTrackHex.split("#")
            cdCurrentTrack = int(cdTrackSplit[0], 16)
            if cdCurrentTrack == 255:
                cdCurrentTrack = "--"
            currentTrackTime = str("{:02}".format(int(cdTrackSplit[3], 16))) + ":" + str("{:02}".format(int(cdTrackSplit[4], 16)))
            if currentTrackTime == "255:127":
                currentTrackTime = "--:--"
        elif id == 0x3E5:
            #Main Menu shit code stuff
            message = (msg.data).hex("#")
            messageSplit = message.split("#")
            scale = 16
            bitNum = 8
            messageStr = [bin(int(n, 16))[2:].zfill(bitNum) for n in messageSplit]
            #if messageStr[0][1] == "1":
                #menuItem = "Menu"
                #msgMenu = can.Message(arbitration_id=0xDF, data=[0x90, 0x00, 0x70], is_extended_id=False)
                #task = bus.send_periodic(msgMenu, 0.1)
                #task.start()
                #showMainMenu = True
            #elif messageStr[2][3] == "1" and menuItem == "Menu":
                #menuItem = "None"
                #task.stop()
                #showMainMenu = False
            if messageStr[1][3] == "1":
                #Mode button will change trip for now
                tripMode += 1
                if tripMode == 3:
                    tripMode = 0
            elif messageStr[2][5] == "1":
                if darkMode:
                    darkMode = False
                else:
                    darkMode = True
                print (darkMode)
        elif id == 0x0A4:
            # This one gets the track name from the CD. Works with MP3s, no idea if it works with Audio CDs (tests show that normal CDs don't have track data)
            message = msg.data
            messageHex = (msg.data).hex("#")
            messageSplit = messageHex.split("#")
            if messageSplit[0] == "10":
                cdframeNum = 0
                cdName = ""
                cdframeLen = int(messageSplit[1], 16)
                nameClean = message[6:]
                singleFrame = nameClean.decode('ISO-8859-1')
            else:
                nameClean = message[1:]
                singleFrame = nameClean.decode('ISO-8859-1')
            cdframeNum = cdframeNum + 1
            cdName = cdName + singleFrame
            # Flow Control Frame
            msgFCF = can.Message(arbitration_id=0x09F, data=[0x30, 0x00, 0x0A], is_extended_id=False)
            bus.send(msgFCF)
            if cdframeNum == 7:
                #When the length of the variable is the same as what the radio declared at the start, 
                #push it into the Global and split is at the NULL character so we have artist and track name separate
                cdTrackNameStr = cdName[20:]
                cdTrackName = cdTrackNameStr.split("\x00")[0]
                cdTrackArtStr = cdName[:20]
                cdTrackArtist = cdTrackArtStr.split("\x00")[0]
                cdTrackDetails = [cdTrackArtist, cdTrackName]
            #Sleep for better results because the sleep aids the kid and the sun the cow (Greek stuff you don't know)
            time.sleep(0.1)
        elif id == 0x363:
            message = (msg.data).hex("#")
            messageSplit = message.split("#")
            secondsForm = int(messageSplit[6], 16) / 4
            current_time_USB = str("{:02}".format(int(messageSplit[7], 16))) + ":" +  str("{:02}".format(int(secondsForm)))
        elif id == 0x2E3:
            # This one is the USB text frame. It contains the track and artist data. Not documented so it was hard to find and even harder to find the FCF for it
            # It's a CAN-TP frame, starting with 10 (because it's a multiframe) followed by the length of the name and then 0x63 (no idea why but I'm dumb)
            # This piece of shit code takes the frame, hexifies it and splits it so we get the text length from it. Then, it shaves the first 3 bytes off
            # of the original frame and passes it to the "completed" name variable. The frames after the initial one only have one byte we don't need, the index one
            # so we shave it off and store them to the final text string as well. I have no precaution whatsoever about frames being send in the wrong order, might implement later
            message = msg.data
            messageHex = (msg.data).hex("#")
            messageSplit = messageHex.split("#")
            # The radio sends a frame with data [10, 60]. This signals that it will start sending the new title. We identify that and reinitiallize all of our variables.
            if messageSplit[0] == "01" and messageSplit[1] == "60":
                frameNum = 0
                usbName = ""
            
            frameNum = frameNum + 1
            if frameNum == 2:
                frameLen = int(messageSplit[1], 16)
                nameClean = message[3:]
                singleFrame = nameClean.decode('ISO-8859-1')
            else:
                nameClean = message[1:]
                singleFrame = nameClean.decode('ISO-8859-1')
            if not frameNum == 1:
                usbName = usbName + singleFrame
            #Send the Flow Control Frame over to the radio so it gives us the rest of the frames
            msgFCF = can.Message(arbitration_id=351, data=[0x30, 0x00, 0x0A], is_extended_id=False)
            bus.send(msgFCF)
            if frameLen == (len(usbName) + 1):
                #When the length of the variable is the same as what the radio declared at the start, 
                #push it into the Global and split is at the NULL character so we have artist and track name separate
                usbTrackName = usbName.split("\x00")
            time.sleep(0.1)
        elif id == 0x125 and discType == "MP3 Disc":
            # List Thing. Each title is 20 chars long. When 1st byte is 06, get the selected track
            message = msg.data
            messageHex = (msg.data).hex("#")
            messageSplit = messageHex.split("#")
            if messageSplit[0] == "05" and messageSplit[1] == "00":
                showList = False
                initialList = True
                trackList = []
            else:
                showList = True
            #If we have just opened it, initialize everything
            if initialList:
                trackList = []
                trackListSel = [False, False, False, False]
                trackListSel[1] = True
            #this closes and opens the list
                if messageSplit[0] == "05":
                    bigList = ""
                #Waits for all the names to be loaded
                if messageSplit[0] >= "21" and initialList:
                    trackList = [" ", "Loading...", " ", " "]
                    nameClean = message[1:]
                    singleFrame = nameClean.decode('ISO-8859-1')
                    bigList += singleFrame
                #This signals the final frame
                if messageSplit[0] == "2c" and initialList:
                    trackList = []
                    bigListSplit = [bigList[i:i+20] for i in range(0, len(bigList), 20)]
                    initialList = False
                    #Split the track names so nulls get ded and create the track list
                    for x in bigListSplit:
                        temp = x.rsplit('\x00')
                        trackList.append(temp[0])
                    bigList = ""
            else:
                #Shit code stuff that handles what happens after the list is loaded and we try to scroll up or down
                #Made in a completely unorthodox way but if it works, it works
                if messageSplit[0] == "06" and messageSplit[1] == "98" and not initialList:
                    selection = int(messageSplit[4], 16)
                    trackListSel = [False, False, False, False]
                    trackListSel[selection] = True
                if messageSplit[0] == "21":
                    if selection == 0:
                        trackList.pop(3)
                    else:
                        trackList.pop(0)
                    trackList.insert(selection, "Loading...")
                    bigList = ""
                if messageSplit[0] >= "21" and not initialList:
                    nameClean = message[1:]
                    singleFrame = nameClean.decode('ISO-8859-1')
                    bigList += singleFrame
                if messageSplit[0] == "23" and not initialList:
                    trackList.pop(selection)
                    temp = bigList.rsplit('\x00')
                    trackList.insert(selection, temp[0])
            if messageSplit[0] == "06" and messageSplit[1] == "90":
                    trackListSel = [False, False, False, False]
                    trackListSel[1] = True
                    trackList = [" ", discType, " ", " "]
                    initialList = True

            msgFCF = can.Message(arbitration_id=0x11F, data=[0x30, 0x00, 0x0A], is_extended_id=False)
            bus.send(msgFCF)
            time.sleep(0.15)
        elif id == 0x221 and tripMode == 0:
            #Trip Time my dude
            message = (msg.data).hex("#")
            messageSplit = message.split("#")
            litersPerHundoHex = messageSplit[1] + '' + messageSplit[2]
            kmUntilDeadHex = messageSplit[3] + '' + messageSplit[4]
            kmRestHex = messageSplit [5] + '' + messageSplit[6]
            litersPerHundo = int(litersPerHundoHex, 16)
            kmUntilDead = int(kmUntilDeadHex, 16)
            kmRest = int(kmRestHex, 16)
            #print ("Liters: " + str(litersPerHundo) + " Km Dead: " + str(kmUntilDead) + " Km Rest: " + str(kmRest))
            tripInfo = [str(kmUntilDead), str(litersPerHundo/10), str(kmRest)]
        elif id == 0x2A1 and tripMode == 1:
            message = (msg.data).hex("#")
            messageSplit = message.split("#")
            litersPerHundoHex = messageSplit[3] + '' + messageSplit[4]
            avSpeedHex = messageSplit[0]
            milesTripHex = messageSplit[1] + '' + messageSplit[2]
            litersPerHundo = int(litersPerHundoHex, 16)
            avSpeed = int(avSpeedHex, 16)
            milesTrip = int(milesTripHex, 16)
            tripInfo = [str(avSpeed), str(litersPerHundo/10), str(avSpeed)]
        elif id == 0x261 and tripMode == 2:
            message = (msg.data).hex("#")
            messageSplit = message.split("#")
            litersPerHundoHex = messageSplit[3] + '' + messageSplit[4]
            avSpeedHex = messageSplit[0]
            milesTripHex = messageSplit[1] + '' + messageSplit[2]
            litersPerHundo = int(litersPerHundoHex, 16)
            avSpeed = int(avSpeedHex, 16)
            milesTrip = int(milesTripHex, 16)
            tripInfo = [str(avSpeed), str(litersPerHundo/10), str(avSpeed)]
        



application_path = (
    sys._MEIPASS
    if getattr(sys, "frozen", False)
    else os.path.dirname(os.path.abspath(__file__))
)

def main():
    global engine
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()
    
    

    # Get the path of the current directory, and then add the name
    # of the QML file, to load it.
    qmlFile = os.path.join(application_path, "dashUI.qml")
    engine.load(QtCore.QUrl.fromLocalFile(qmlFile))
    #The big OOF that need optimization. Sends all data to the QML file for it to display. Updates ever 50ms (yikes) so station seeking and volume looks smooth
    
    #Start Reading Thread
    #th = threading.Thread(target=canRead)
    #th.start()
    def update_display():
        radioFunctions()
        tripFunction()
        engine.rootObjects()[0].setProperty('radioBand', radioBand)
        engine.rootObjects()[0].setProperty('rdsText', rdsText)
        engine.rootObjects()[0].setProperty('freq', freq)
        engine.rootObjects()[0].setProperty('stationMem', stationMem)
        engine.rootObjects()[0].setProperty('modType', modType)
        engine.rootObjects()[0].setProperty('source', source)
        engine.rootObjects()[0].setProperty('srcImage', srcImage)
        engine.rootObjects()[0].setProperty('showMainMenu', showMainMenu)
        engine.rootObjects()[0].setProperty('isListVisible', showList)
        engine.rootObjects()[0].setProperty('tripInfo', tripInfo)
        engine.rootObjects()[0].setProperty('darkMode', darkMode)
        engine.rootObjects()[0].setProperty('tripImage', tripImage)
        engine.rootObjects()[0].setProperty('isVolumeChanging', isVolumeChanging)
        engine.rootObjects()[0].setProperty('showAudioMenu', showAudioMenu)
        if isVolumeChanging:
            engine.rootObjects()[0].setProperty('volume', volume)
        if showAudioMenu:
            sendAudioValues()
        if showList:
            sendList()
        
    #Gets and updates the date and time every second from the Pi's local time because I'm lazy and don't want to implement a datetime function that talks to the BSI
    def update_datetime():
        today = date.today()
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        curr_date = today.strftime("%d/%m/%Y")
        engine.rootObjects()[0].setProperty('time', current_time)
        engine.rootObjects()[0].setProperty('date', curr_date)
    #Timer for updating everything
    timer = QTimer()
    timer.setInterval(50)  # msecs 1000 = 1 sec
    timer.timeout.connect(update_display)
    timer.start()
    #Timer for updating date and time
    timer2 = QTimer()
    timer2.setInterval(1000)
    timer2.timeout.connect(update_datetime)
    timer2.start()
    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec_())


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    