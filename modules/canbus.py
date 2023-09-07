import can.interfaces.slcan
import modules.settings as settings
import time
from modules.display import *
from modules.kml import *
from pynput.keyboard import Key, Controller

keyboard = Controller()

def canRead():

    # settings.bus = can.ThreadSafesettings.bus(interface='socketcan', channel='can0', bitrate=125000)
    #Define stuff
    curr_timer = time.time()
    curr_shutdown = time.time()
    frameNum = 0
    usbName = ""
    frameLen = 0
    cdframeNum = 0
    cdframeLen = 0
    cdName = ""
    bigList = ""
    bigListSplit = ""
    initialList = True
    settings.tripMode = 0
    settings.diagBoxShow = False
    power = True
    test = False
    # print (settings.bus)
    for msg in settings.bus:
        id = msg.arbitration_id
        # print (id)
        if id == 0x0F6:
            message = (msg.data).hex("#")
            messageSplit = message.split("#")
            scale = 16
            bitNum = 8
            messageStr = [bin(int(n, 16))[2:].zfill(bitNum) for n in messageSplit]
            if (messageStr[0][4] == 0 or messageSplit[0] == "00") and power == True:
                settings.rdsText = "GoodBye!"
                # call("uhubctl -p 2 -l 1-1 -a 0", shell=True)
                power = False
                curr_shutdown = time.time()
            elif (messageStr[0][4] == 1 or messageSplit[0] == "08") and power == False:
                # call("uhubctl -p 2 -l 1-1 -a 1", shell=True)
                settings.rdsText = "ON"
                power = True
            if (time.time() - curr_shutdown) >= 90 and power == False:
                # call("halt", shell=True)
                continue
            
        #This one gets the RDS text (if available) and displays it. PSA did us a solid and is sending it in ASCII. Thanks French Gods
        if id == 677 and settings.radioPower:
            rdsbytearr = msg.data
            if rdsbytearr == b'\x00\x00\x00\x00\x00\x00\x00\x00':
                settings.rdsText = "No RDS Available"
            else:
                settings.rdsText = rdsbytearr.decode('ISO-8859-1')
        #This one is for the radio's Band Display (FM1,etc) and displaying if we are using MHz or KHz
        elif id == 549 and settings.radioPower:
            radioStatusarr = msg.data
            radioStatus = radioStatusarr.hex('#')
            radioHex = radioStatusarr.hex()
            scale = 16
            bitNum = 8
            
            radioSplit = radioStatus.split("#")
            radioStr = [bin(int(n, 16))[2:].zfill(bitNum) for n in radioSplit]
            if str(radioSplit[2]) == "10":
                settings.radioBand = "FM-1"
                settings.modType = "MHz"
            elif str(radioSplit[2]) == "20":
                settings.radioBand = "FM-2"
                settings.modType = "MHz"
            elif str(radioSplit[2]) == "40":
                settings.radioBand = "FM-AST"
                settings.modType = "MHz"
            elif str(radioSplit[2]) == "50":
                settings.radioBand = "AM"
                settings.modType = "KHz"
            settings.freqHex = radioSplit[3] + radioSplit[4]
            settings.freq = int(settings.freqHex, 16)
            settings.freq = (settings.freq * 0.05) + 50
            settings.freq = "%.2f" % settings.freq
            memHex = radioSplit[1]
            settings.stationMemarr = list(str(memHex))
            settings.stationMem = settings.stationMemarr[0]
        #This one reads the settings.source frame and displays accordingly. Added BT and USB just so you don't have to
        elif id == 357:
            settings.sourcearr = msg.data
            settings.sourceHex = settings.sourcearr.hex('#')
            settings.sourceSplit = settings.sourceHex.split("#")
            if settings.sourceSplit[2] == "10":
                settings.source = "Radio"
            elif settings.sourceSplit[2] == "20":
                settings.source = "CD"
            elif settings.sourceSplit[2] == "40":
                settings.source = "AUX"
            elif settings.sourceSplit[2] == "60":
                settings.source = "USB"
            elif settings.sourceSplit[2] == "70":
                settings.source = "Bluetooth"
            if settings.sourceSplit[0] == "40":
                #Set if Power is off. Everything else is on
                settings.radioPower = False
            elif settings.sourceSplit[0] == "E0":
                settings.radioPower = True
                #Add mute state
            else:
                settings.radioPower = True
            
        #Gets the settings.volume frame, turns HEX to Binary, splits the first 3 bits that tell us if the settings.volume is currently being changed and translates the rest to integer
        elif id == 421:
            volarr = msg.data
            volHex = volarr.hex()
            scale = 16
            bitNum = 8
            volStr = bin(int(volHex, scale))[2:].zfill(bitNum)
            settings.volume = int(volStr[3:], 2)
            if volStr[:3] == "000":
                settings.isVolumeChanging = True
                settings.isVolumeStillChanging = True
                curr_timer = time.time()
            else:
                settings.isVolumeStillChanging = False
            if (time.time() - curr_timer) >= 2:
                settings.isVolumeChanging = False
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
                settings.isLRBal = True
            else:
                settings.isLRBal = False
            if soundSetBin[1][0] == "1":
                settings.isRFBal = True
            else:
                settings.isRFBal = False
            if soundSetBin[2][0] == "1":
                settings.isBass = True
            else:
                settings.isBass = False
            if soundSetBin[4][0] == "1":
                settings.isTreble = True
            else:
                settings.isTreble = False
            if soundSetBin[5][0] == "1":
                settings.isLoudness = True
            else:
                settings.isLoudness = False
            if soundSetBin[5][3] == "1":
                settings.isAutoVol = True
            else:
                settings.isAutoVol = False
            if soundSetBin[6][1] == "1":
                settings.isEQPreset = True
            else:
                settings.isEQPreset = False
            #Handle the values and send them over, regardless of menu visibility
            settings.lrValue = int(soundSetBin[0][1:], 2) - 63
            settings.rfValue = int(soundSetBin[1][1:], 2) - 63
            settings.bassValue = int(soundSetBin[2][1:], 2) - 63
            settings.trebleValue = int(soundSetBin[4][1:], 2) - 63
            settings.loudValue = int(soundSetBin[5][1])
            settings.autoVolValue = int(soundSetBin[5][5:])
            #Set EQ text
            eqBin = int(soundSetBin[6][3:], 2)
            if eqBin == 3:
                settings.eqPresetValue = "None"
            elif eqBin == 7:
                settings.eqPresetValue = "Classical"
            elif eqBin == 11:
                settings.eqPresetValue = "Jazz-Blues"
            elif eqBin == 15:
                settings.eqPresetValue = "Pop-Rock"
            elif eqBin == 19:
                settings.eqPresetValue = "Vocal"
            elif eqBin == 23:
                settings.eqPresetValue = "Techno"
        elif id == 869:
            cdPresenceInfo = (msg.data).hex("#")
            cdPresenceSplit = cdPresenceInfo.split("#")
            settings.trackAll = int(cdPresenceSplit[0], 16)
            if settings.trackAll == 255:
                settings.cdCurrentTrack = "--"
            if str(cdPresenceSplit[3]) == "01":
                settings.discType = "MP3 Disc"
                settings.srcImage = "cd_mp3.png"
            else:
                settings.discType = "Audio CD"
                settings.srcImage = "cd_audio.png"
        elif id == 933 and settings.source == "CD":
            cdTrackHex = (msg.data).hex("#")
            cdTrackSplit = cdTrackHex.split("#")
            settings.cdCurrentTrack = int(cdTrackSplit[0], 16)
            if settings.cdCurrentTrack == 255:
                settings.cdCurrentTrack = "--"
            settings.currentTrackTime = str("{:02}".format(int(cdTrackSplit[3], 16))) + ":" + str("{:02}".format(int(cdTrackSplit[4], 16)))
            if settings.currentTrackTime == "255:127":
                settings.currentTrackTime = "--:--"
        elif id == 0x3E5:
            #Main Menu shit code stuff
            message = (msg.data).hex("#")
            messageSplit = message.split("#")
            scale = 16
            bitNum = 8
            messageStr = [bin(int(n, 16))[2:].zfill(bitNum) for n in messageSplit]
            if messageStr[0][1] == "1":
                settings.menuItem = "Menu"
                msgMenu = can.Message(arbitration_id=0xDF, data=[0x90, 0x00, 0x70], is_extended_id=False)
                task = settings.bus.send_periodic(msgMenu, 0.1)
                task.start()
                settings.showMainMenu = True
            elif messageStr[2][3] == "1" and settings.menuItem == "Menu":
                settings.menuItem = "None"
                task.stop()
                settings.showMainMenu = False
            if messageStr[1][3] == "1":
                #Mode button will change trip for now
                settings.tripMode += 1
                if settings.tripMode == 3:
                    settings.tripMode = 0
            elif messageStr[2][5] == "1":
                if settings.darkMode:
                    call("uhubctl -p 2 -l 1-1 -a 1", shell=True)
                    settings.darkMode = False
                else:
                    call("uhubctl -p 2 -l 1-1 -a 0", shell=True)
                    settings.darkMode = True
            elif messageStr[5][5] == "1":
                print("r")
                keyboard.press(Key.right)
                keyboard.release(Key.right)
            elif messageStr[5][7] == "1":
                print("l")
                keyboard.press(Key.left)
                keyboard.release(Key.left)
            elif messageStr[2][1] == "1":
                print("Space")
                keyboard.press(Key.space)
                time.sleep(0.2)
                keyboard.release(Key.space)
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
            settings.bus.send(msgFCF)
            if cdframeNum == 7:
                #When the length of the variable is the same as what the radio declared at the start, 
                #push it into the Global and split is at the NULL character so we have artist and track name separate
                cdTrackNameStr = cdName[20:]
                cdTrackName = cdTrackNameStr.split("\x00")[0]
                cdTrackArtStr = cdName[:20]
                cdTrackArtist = cdTrackArtStr.split("\x00")[0]
                settings.cdTrackDetails = [cdTrackArtist, cdTrackName]
            #Sleep for better results because the sleep aids the kid and the sun the cow (Greek stuff you don't know)
            time.sleep(0.1)
        elif id == 0x363:
            message = (msg.data).hex("#")
            messageSplit = message.split("#")
            secondsForm = int(messageSplit[6], 16) / 4
            settings.current_time_USB = str("{:02}".format(int(messageSplit[7], 16))) + ":" +  str("{:02}".format(int(secondsForm)))
        elif id == 0x2E3:
            # This one is the USB and BT text frame. It contains the track and artist data. Not documented so it was hard to find and even harder to find the FCF for it
            # It's a CAN-TP frame, starting with 10 (because it's a multiframe) followed by the length of the name and then 0x63 (no idea why but I'm dumb)
            # This piece of shit code takes the frame, hexifies it and splits it so we get the text length from it. Then, it shaves the first 3 bytes off
            # of the original frame and passes it to the "completed" name variable. The frames after the initial one only have one byte we don't need, the index one
            # so we shave it off and store them to the final text string as well. I have no precaution whatsoever about frames being send in the wrong order, might implement later
            message = msg.data
            messageHex = (msg.data).hex("#")
            messageSplit = messageHex.split("#")

            if settings.source == "Bluetooth":
                if messageSplit[0] == "10" and messageSplit[2] == "63":
                    frameNum = 0
                    usbName = ""
                
                frameNum = frameNum + 1
                if frameNum == 1:
                    frameLen = int(messageSplit[1], 16)
                    nameClean = message[3:]
                    singleFrame = nameClean.decode('ISO-8859-1')
                    usbName = singleFrame
                else:
                    nameClean = message[1:]
                    singleFrame = nameClean.decode('ISO-8859-1')

                if not frameNum == 1:
                    usbName = usbName + singleFrame
                                #Send the Flow Control Frame over to the radio so it gives us the rest of the frames
                msgFCF = can.Message(arbitration_id=351, data=[0x30, 0x00, 0x0A], is_extended_id=False)
                settings.bus.send(msgFCF)
                if frameLen == (len(usbName) + 1):
                    #When the length of the variable is the same as what the radio declared at the start, 
                    #push it into the Global and split is at the NULL character so we have artist and track name separate
                    settings.usbTrackName = usbName.split("\x00")

            else:
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
                settings.bus.send(msgFCF)
                if frameLen == (len(usbName) + 1):
                    #When the length of the variable is the same as what the radio declared at the start, 
                    #push it into the Global and split is at the NULL character so we have artist and track name separate
                    settings.usbTrackName = usbName.split("\x00")
            time.sleep(0.1)
        elif id == 0x125 and settings.discType == "MP3 Disc":
            # List Thing. Each title is 20 chars long. When 1st byte is 06, get the selected track
            message = msg.data
            messageHex = (msg.data).hex("#")
            messageSplit = messageHex.split("#")
            if messageSplit[0] == "05" and messageSplit[1] == "00":
                settings.showList = False
                initialList = True
                settings.trackList = []
            else:
                settings.showList = True
            #If we have just opened it, initialize everything
            if initialList:
                settings.trackList = []
                settings.trackListSel = [False, False, False, False]
                settings.trackListSel[1] = True
            #this closes and opens the list
                if messageSplit[0] == "05":
                    bigList = ""
                #Waits for all the names to be loaded
                if messageSplit[0] >= "21" and initialList:
                    settings.trackList = [" ", "Loading...", " ", " "]
                    nameClean = message[1:]
                    singleFrame = nameClean.decode('ISO-8859-1')
                    bigList += singleFrame
                #This signals the final frame
                if messageSplit[0] == "2c" and initialList:
                    settings.trackList = []
                    bigListSplit = [bigList[i:i+20] for i in range(0, len(bigList), 20)]
                    initialList = False
                    #Split the track names so nulls get ded and create the track list
                    for x in bigListSplit:
                        temp = x.rsplit('\x00')
                        settings.trackList.append(temp[0])
                    bigList = ""
            else:
                #Shit code stuff that handles what happens after the list is loaded and we try to scroll up or down
                #Made in a completely unorthodox way but if it works, it works
                if messageSplit[0] == "06" and messageSplit[1] == "98" and not initialList:
                    selection = int(messageSplit[4], 16)
                    settings.trackListSel = [False, False, False, False]
                    settings.trackListSel[selection] = True
                if messageSplit[0] == "21":
                    if selection == 0:
                        settings.trackList.pop(3)
                    else:
                        settings.trackList.pop(0)
                    settings.trackList.insert(selection, "Loading...")
                    bigList = ""
                if messageSplit[0] >= "21" and not initialList:
                    nameClean = message[1:]
                    singleFrame = nameClean.decode('ISO-8859-1')
                    bigList += singleFrame
                if messageSplit[0] == "23" and not initialList:
                    settings.trackList.pop(selection)
                    temp = bigList.rsplit('\x00')
                    settings.trackList.insert(selection, temp[0])
            if messageSplit[0] == "06" and messageSplit[1] == "90":
                    settings.trackListSel = [False, False, False, False]
                    settings.trackListSel[1] = True
                    settings.trackList = [" ", settings.discType, " ", " "]
                    initialList = True

            msgFCF = can.Message(arbitration_id=0x11F, data=[0x30, 0x00, 0x0A], is_extended_id=False)
            settings.bus.send(msgFCF)
            time.sleep(0.15)
        elif id == 0x221 and settings.tripMode == 0:
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
            settings.tripInfo = [str(kmUntilDead), str(litersPerHundo/10), str(kmRest)]
        elif id == 0x2A1 and settings.tripMode == 1:
            message = (msg.data).hex("#")
            messageSplit = message.split("#")
            litersPerHundoHex = messageSplit[3] + '' + messageSplit[4]
            avSpeedHex = messageSplit[0]
            milesTripHex = messageSplit[1] + '' + messageSplit[2]
            litersPerHundo = int(litersPerHundoHex, 16)
            avSpeed = int(avSpeedHex, 16)
            milesTrip = int(milesTripHex, 16)
            settings.tripInfo = [str(avSpeed), str(litersPerHundo/10), str(avSpeed)]
        elif id == 0x261 and settings.tripMode == 2:
            message = (msg.data).hex("#")
            messageSplit = message.split("#")
            litersPerHundoHex = messageSplit[3] + '' + messageSplit[4]
            avSpeedHex = messageSplit[0]
            milesTripHex = messageSplit[1] + '' + messageSplit[2]
            litersPerHundo = int(litersPerHundoHex, 16)
            avSpeed = int(avSpeedHex, 16)
            milesTrip = int(milesTripHex, 16)
            settings.tripInfo = [str(avSpeed), str(litersPerHundo/10), str(avSpeed)]
        elif id == 0x1A1:
            message = (msg.data).hex("#")
            messageSplit = message.split("#")
            print (messageSplit)
            if messageSplit[0] == "80":
                diagWindowHandler(messageSplit)
            else:
                settings.diagBoxShow = False
                settings.engine.rootObjects()[0].setProperty('diagBoxShow', settings.diagBoxShow)
        elif id == 0x1A3:
            # take the useful data from each byte and pass it to the other function
            message = msg.data
            second_byte = message[1]
            call_avail = (second_byte >> 1) & 0x01
            connected = (message[0] >> 7) & 0x01
            signal = message[2]
            battery = message[3]
            sms_avail = (second_byte >> 6) & 0x01
            pair_request = message[5] 


            data = {
                "connected": connected,
                "signal": signal,
                "battery": battery,
                "call": call_avail,
                "sms": sms_avail,
                "pair_request": pair_request
            }

            kmlHandler(data)
            # print("currently on call")
        elif id == 0x123:
            message = msg.data
            messagehex = (msg.data).hex("#")
            messageSplit = messagehex.split("#")
            # print("statusByte: ",statusByte)
            # print("Whole Hex: ", message.hex("#"))

            # first byte is 10, means new stuff is coming
            if messageSplit[0] == "10":
                frameNum = 0
                callerName = ""
                msgType = messageSplit[2]
            
            frameNum = frameNum + 1
            if frameNum == 1:
                frameLen = int(messageSplit[1], 16)
                if msgType == "80":
                    nameClean = message[4:]
                else:
                    nameClean = message[5:]
                    
                singleFrame = nameClean.decode('ISO-8859-1')
                callerName = singleFrame
            else:
                nameClean = message[1:]
                singleFrame = nameClean.decode('ISO-8859-1')

            if not frameNum == 1:
                callerName = callerName + singleFrame
            
            #Send the Flow Control Frame over to the radio so it gives us the rest of the frames
            msgFCF = can.Message(arbitration_id=0x29F, data=[0x30, 0x00, 0x0A], is_extended_id=False)
            settings.bus.send(msgFCF)
            if contains_only_null_bytes(callerName) :
                callerName = "Unknown Number"

            if msgType == "80":
                #pair request. Sends repeated signal to Radio so we can listen to keypress
                settings.engine.rootObjects()[0].setProperty('kmlPairTxt', callerName.split("\x00")[0])
                msgMenu = can.Message(arbitration_id=0xDF, data=[0x90, 0x00, 0x70], is_extended_id=False)
                task = settings.bus.send_periodic(msgMenu, 0.2, 10)
                task.start()
            elif msgType == "10":
                settings.engine.rootObjects()[0].setProperty('kmlTextTxt', "Call: "+callerName.split("\x00")[0])

               
          
def contains_only_null_bytes(string):
    for char in string:
        if char != '\x00':
            return False
    return True
