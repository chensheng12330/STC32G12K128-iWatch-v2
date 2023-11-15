# -*- coding: utf-8 -*-
import serial
import serial.tools.list_ports
from PyQt5.QtCore import *

class SerialReceiveThread(QThread):
    sinOut = pyqtSignal(list)
    def __init__(self, ser = serial.Serial(), parent=None):
        super(SerialReceiveThread, self).__init__(parent)
        self.working = True
        self.ser = ser

    def run(self):
        while self.working:
            try:
                temp = self.ser.readline().decode('utf-8').strip('\r\n').split('#')
                self.sinOut.emit(temp)
            except Exception:
                break


    def stop(self):
        self.working = False