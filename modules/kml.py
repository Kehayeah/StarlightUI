import modules.settings as settings
from PyQt5.QtCore import QObject, pyqtSlot 
from modules.canbus import *
import can.interfaces.slcan

def kmlHandler(kmlProps):
    
    call_avail = kmlProps['call']
    settings.engine.rootObjects()[0].setProperty('phoneStatus', kmlProps['connected'])
    settings.engine.rootObjects()[0].setProperty('phoneSignal', kmlProps["signal"] if kmlProps['signal'] <= 4 else 4)
    settings.engine.rootObjects()[0].setProperty('phoneBat', kmlProps["battery"] if kmlProps['battery'] <= 4 else 4)

    # print(kmlProps)
    # Do we have a pair request?
    if kmlProps["pair_request"] == 0x01:
        settings.kmlPairShow = True
        settings.engine.rootObjects()[0].setProperty('kmlPairShow', settings.kmlPairShow)
    else:
        settings.kmlPairShow = False
        settings.engine.rootObjects()[0].setProperty('kmlPairShow', settings.kmlPairShow)

    # Do we have a call request?
    if call_avail:
        settings.kmlBoxShow = True
        # settings.engine.rootObjects()[0].setProperty('kmlTextTxt', call_avail)
        settings.engine.rootObjects()[0].setProperty('kmlBoxShow', settings.kmlBoxShow)
    else:
        settings.kmlBoxShow = False
        settings.engine.rootObjects()[0].setProperty('kmlBoxShow', settings.kmlBoxShow)


class KML(QObject):
    
    @pyqtSlot(str)
    def sendAcc(self, name):

        msgList = can.Message(arbitration_id=0x1DF, data=[0x00, 0x00, 0x20, 0x00], is_extended_id=False)
        task = settings.bus.send_periodic(msgList, 0.2, 4)
        task.start()

        msgPass = can.Message(arbitration_id=0x2DF, data=[0x05, 0x01, 0x30, 0x30, 0x30, 0x30], is_extended_id=False)
        task2 = settings.bus.send_periodic(msgPass, 1, 7)
        task2.start()

    @pyqtSlot(str)
    def sendDeny(self, name):

        msgList = can.Message(arbitration_id=0x1DF, data=[0x00, 0x00, 0x10, 0x00], is_extended_id=False)
        task = settings.bus.send_periodic(msgList, 0.2, 4)
        task.start()