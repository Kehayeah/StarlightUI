import modules.settings as settings

def tripFunction():
    
    if settings.tripMode == 0:
        tripImage = ["trip_gasstation.png", "trip_fuel.png", "trip_distance.png"]
    if settings.tripMode == 1:
        tripImage = ["trip_fuel.png", "trip_gasstation.png","trip_distance.png"]

def diagWindowHandler(diagMessage):
    diagText = ""
    
    if diagMessage[1] == "01":
        diagText = "Engine Temperature Too High"
    elif diagMessage[1] == "03":
        diagText = "Coolant Level Too Low"
    elif diagMessage[1] == "04":
        diagText = "Check Engine Oil Level"
    elif diagMessage[1] == "05":
        diagText = "Engine Oil Pressure Too Low"
    elif diagMessage[1] == "08":
        diagText = "Brake System Faulty"
    elif diagMessage[1] == "0a":
        diagText = "Air Suspension OK"
    elif diagMessage[1] == "0b":
        diagText = "Door Open"
    elif diagMessage[1] == "0d":
        diagText = "Tyre Puncture Detected"
    elif diagMessage[1] == "11":
        diagText == "Suspension Faulty: Max Speed 90 Km/h"
    elif diagMessage[1] == "12":
        diagText == "Suspension Faulty"
    elif diagMessage[1] == "13":
        diagText = "Power Steering Faulty"
    elif diagMessage[1] == "61":
        diagText = "Handbrake On"
    elif diagMessage[1] == "67":
        diagText = "Brake Pads Worn"
    elif diagMessage[1] == "68":
        diagText = "Handbrake Faulty"
    elif diagMessage[1] == "6a":
        diagText = "ABS System Faulty"
    elif diagMessage[1] == "6c":
        diagText = "Suspension Faulty"
    elif diagMessage[1] == "6d":
        diagText = "Power Steering Faulty"
    elif diagMessage[1] == "6f":
        diagText = "Cruise Control System Faulty"
    elif diagMessage[1] == "74":
        diagText = "Sidelamp Bulb Faulty"
    elif diagMessage[1] == "76":
        diagText = "Directional Headlamps Faulty"
    elif diagMessage[1] == "7a":
        diagText = "Gearbox Faulty"
    elif diagMessage[1] == "7e":
        diagText = "Engine Management System Faulty"
    elif diagMessage[1] == "8a":
        diagText = "Battery Charge or Electrical Supply Faulty"
    elif diagMessage[1] == "8d":
        diagText = "Tyre Pressure Too Low"
    elif diagMessage[1] == "9e":
        diagText = "Direction Indicator Faulty"
    elif diagMessage[1] == "a0":
        diagText = "Sidelamp Bulb Faulty"
    elif diagMessage[1] == "a1":
        diagText = "Parking Lamp Faulty"
    elif diagMessage[1] == "cd":
        diagText = "Cruise Control Not Possible: Speed Too Low"
    elif diagMessage[1] == "ce":
        diagText = "Cruise Not Possible: Enter The Speed"
    elif diagMessage[1] == "d2":
        diagText = "Front Seat Belts Not Fastened"
    elif diagMessage[1] == "d9":
        diagText = "Handbrake!"
    elif diagMessage[1] == "de":
        diagText = "Door Open"
    elif diagMessage[1] == "df":
        diagText = "Screen Wash Fluid Low"
    elif diagMessage[1] == "e0":
        diagText = "Fuel Level Low"
    
    settings.diagBoxShow = True
    settings.engine.rootObjects()[0].setProperty('diagTextTxt', diagText)
    settings.engine.rootObjects()[0].setProperty('diagBoxShow', settings.diagBoxShow)



#Send Audio Settings only if menu visible to cut overall delay
def sendAudioValues():
    #Show Setting
    settings.engine.rootObjects()[0].setProperty('isBass', settings.isBass)
    settings.engine.rootObjects()[0].setProperty('isTreble', settings.isTreble)
    settings.engine.rootObjects()[0].setProperty('isLoudness', settings.isLoudness)
    settings.engine.rootObjects()[0].setProperty('isAutoVol', settings.isAutoVol)
    settings.engine.rootObjects()[0].setProperty('isRFBal', settings.isRFBal)
    settings.engine.rootObjects()[0].setProperty('isLRBal', settings.isLRBal)
    settings.engine.rootObjects()[0].setProperty('isEQPreset', settings.isEQPreset)
    #Send Value
    settings.engine.rootObjects()[0].setProperty('bassValue',settings. bassValue)
    settings.engine.rootObjects()[0].setProperty('trebleValue', settings.trebleValue)
    settings.engine.rootObjects()[0].setProperty('loudValue', settings.loudValue)
    settings.engine.rootObjects()[0].setProperty('autoVolValue', settings.autoVolValue)
    settings.engine.rootObjects()[0].setProperty('rfValue', settings.rfValue)
    settings.engine.rootObjects()[0].setProperty('lrValue', settings.lrValue)
    settings.engine.rootObjects()[0].setProperty('eqPresetValue', settings.eqPresetValue)

def sendList():
    settings.engine.rootObjects()[0].setProperty('trackList', settings.trackList)
    settings.engine.rootObjects()[0].setProperty('trackListSel', settings.trackListSel)