from PyQt5.QtQml import QQmlApplicationEngine
import can.interfaces.slcan

def init():
    global rdsText, isSeeking, source, freq, stationMem, modType, radioBand, volume, isVolumeChanging, isVolumeStillChanging, radioPower, isLRBal, isRFBal, isBass, isTreble, isLoudness, isAutoVol, isEQPreset
    global lrValue, rfValue, bassValue, trebleValue, loudValue, autoVolValue, eqPresetValue
    global trackAll, discType, srcImage, cdCurrentTrack, currentTrackTime, menuItem, showMainMenu, current_time_USB, theID, usbTrackName, cdTrackDetails, trackList, showList, trackListSel
    global tripInfo, darkMode, tripMode, diagBoxShow, kmlBoxShow,kmlPairShow
    global engine
    global tripImage
    global showAudioMenu
    global bus


    bus = can.ThreadSafeBus(interface='slcan', channel='/dev/ttyUSB0@115200', bitrate=125000)
    engine = QQmlApplicationEngine()
    rdsText  = ""
    source = ""
    freq = ""
    stationMem = ""
    modType = ""
    radioBand = ""
    volume = 0
    isVolumeChanging = False
    isVolumeStillChanging = False
    radioPower = False
    isLRBal = False
    showAudioMenu = False
    isRFBal = False
    isBass = False
    isTreble = False
    isLoudness = False
    isAutoVol = False
    isEQPreset = False
    lrValue = "0"
    rfValue = "0"
    bassValue = "0"
    trebleValue = "0"
    loudValue = "0"
    autoVolValue = "0"
    eqPresetValue = ""
    srcImage = "aux_cable.png"
    trackAll = 0
    discType = "Audio CD"
    cdCurrentTrack = 0
    currentTrackTime = "0"
    isMenuOpen = False
    menuItem = "None"
    showMainMenu = False
    current_time_USB = "00:00"
    usbTrackName = ["Artist","Track Name"]
    cdTrackDetails = ["Artist", "Track Name"]
    trackList = [" ", " ", " ", " "]
    showList = False
    trackListSel = [False, False, False, False]
    tripInfo = ["--", "pepe", "--"]
    darkMode = False
    tripMode = 0
    tripImage = ["trip_distance.png", "trip_fuel.png", "trip_gasstation.png"]
    diagBoxShow = False
    kmlBoxShow = False
    kmlPairShow = False