import modules.settings as settings

def radioFunctions():
    #global settings.rdsText, settings.isSeeking, settings.source, settings.freq, settings.stationMem, settings.modType, settings.radioBand, settings.volume, settings.radioPower, settings.showAudioMenu, settings.srcImage
    if not settings.radioPower:
        settings.rdsText = "Radio Off"
        settings.freq = ""
        settings.radioBand = ""
        settings.modType = ""
        settings.stationMem = ""
        settings.srcImage = "power_off.png"
    else:
        if settings.source == "AUX":
            settings.rdsText = "Playing from AUX"
            settings.freq = ""
            settings.radioBand = ""
            settings.modType = ""
            settings.stationMem = ""
            settings.srcImage = "aux_cable.png"
        elif settings.source == "CD":
            if settings.discType == "Audio CD":
                settings.rdsText = "Track " + str(settings.cdCurrentTrack) +" / " + str(settings.trackAll)
                settings.freq = settings.currentTrackTime
                settings.radioBand = settings.discType
                settings.modType = ""
                settings.stationMem = ""
            else:
                settings.rdsText = settings.cdTrackDetails[1][:25]
                settings.freq = settings.cdTrackDetails[0]
                settings.radioBand = settings.discType
                settings.modType = ""
                settings.stationMem = settings.currentTrackTime
        elif settings.source == "Radio":
            settings.srcImage = "radio.png"
        elif settings.source == "USB":
            settings.rdsText = settings.usbTrackName[1][:25]
            settings.freq = settings.usbTrackName[0]
            settings.radioBand =  settings.current_time_USB
            settings.modType = ""
            settings.srcImage = "usb.png"
            settings.stationMem = ""
        elif settings.source == "Bluetooth":
            settings.rdsText = settings.usbTrackName[1][:25]
            settings.freq = settings.usbTrackName[0]
            settings.radioBand =  settings.current_time_USB
            settings.modType = ""
            settings.srcImage = "bluetooth.png"
            settings.stationMem = ""

    if settings.isLRBal or settings.isRFBal or settings.isBass or settings.isTreble or settings.isLoudness or settings.isAutoVol or settings.isEQPreset:
        settings.showAudioMenu = True
    else:
        settings.showAudioMenu = False