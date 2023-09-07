import sys
import can
import threading
import os
from os.path import abspath, dirname, join
from datetime import datetime, date
import time
from textwrap import wrap
from subprocess import call

from PyQt5 import QtCore, QtGui, QtQml
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer
from PyQt5.QtQuick import QQuickView

from modules.radio import *
import modules.settings as settings
from modules.canbus import *
from modules.kml import *
from modules.display import *

# from vars import *
    

application_path = (
    sys._MEIPASS
    if getattr(sys, "frozen", False)
    else os.path.dirname(os.path.abspath(__file__))
)

def main():
    
    app = QApplication(sys.argv)
    
    settings.init()
    

    # Get the path of the current directory, and then add the name
    # of the QML file, to load it.
    qmlFile = os.path.join(application_path, "dashUI.qml")
    settings.engine.load(QtCore.QUrl.fromLocalFile(qmlFile))
    #The big OOF that need optimization. Sends all data to the QML file for it to display. Updates ever 50ms (yikes) so station seeking and settings.volume looks smooth
    
    #Start Reading Thread
    th = threading.Thread(target=canRead)
    th.start()

    kml = KML()
    settings.engine.rootContext().setContextProperty("kml", kml)
    
    def update_display():
        radioFunctions()
        tripFunction()
        settings.engine.rootObjects()[0].setProperty('radioBand', settings.radioBand)
        settings.engine.rootObjects()[0].setProperty('rdsText', settings.rdsText)
        settings.engine.rootObjects()[0].setProperty('freq', settings.freq)
        settings.engine.rootObjects()[0].setProperty('stationMem', settings.stationMem)
        settings.engine.rootObjects()[0].setProperty('modType', settings.modType)
        settings.engine.rootObjects()[0].setProperty('source', settings.source)
        settings.engine.rootObjects()[0].setProperty('srcImage', settings.srcImage)
        settings.engine.rootObjects()[0].setProperty('showMainMenu', settings.showMainMenu)
        settings.engine.rootObjects()[0].setProperty('isListVisible', settings.showList)
        settings.engine.rootObjects()[0].setProperty('tripInfo', settings.tripInfo)
        settings.engine.rootObjects()[0].setProperty('darkMode', settings.darkMode)
        settings.engine.rootObjects()[0].setProperty('tripImage', settings.tripImage)
        settings.engine.rootObjects()[0].setProperty('isVolumeChanging', settings.isVolumeChanging)
        settings.engine.rootObjects()[0].setProperty('showAudioMenu', settings.showAudioMenu)
        if settings.isVolumeChanging:
            settings.engine.rootObjects()[0].setProperty('volume', settings.volume)
        if settings.showAudioMenu:
            sendAudioValues()
        if settings.showList:
            sendList()
        
    #Gets and updates the date and time every second from the Pi's local time because I'm lazy and don't want to implement a datetime function that talks to the BSI
    def update_datetime():
        today = date.today()
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        curr_date = today.strftime("%d/%m/%Y")
        settings.engine.rootObjects()[0].setProperty('time', current_time)
        settings.engine.rootObjects()[0].setProperty('date', curr_date)
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
    if not settings.engine.rootObjects():
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
    
