from mainwindow import Ui_MainWindow
from PySide6 import QtWidgets, QtGui
from PySide6 import QtSerialPort
from PySide6.QtCore import QIODevice, QTimer, Signal, QObject, Slot
import sys
import ctypes


class EstimatorCS:
    def __init__(self):
        self.f = ctypes.cdll.LoadLibrary('.\\c_module\\checksum.dll')
        self.f.calculateChecksum.restype = ctypes.c_char
        self.f.calculateChecksum.argtypes = [ctypes.POINTER(ctypes.c_char), ]

    def get_CS(self, cmd):
        return ord(self.f.calculateChecksum(cmd.encode('utf-8')))

cmd = 'D,s,1,49,5949.08250,N,03019.66393,S,00155.5,2023,10,23,180723.00,0.004,*,96,\r,\n'
estimator = EstimatorCS()
cs = estimator.get_CS(cmd)
print(cs)

class Signals(QObject):
    get_gps = Signal(object)
    get_imu = Signal(object)
    get_man_perm = Signal(object)


class Base:
    def start_listen(self): ...
    def stop_listen(self): ...
    def __init_serial_port(self): ...
    def readFromSerial(self): ...
    def get_gps(self): ...
    def get_imu(self): ...
    def write_manual(self): ...
    
    
class App(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(App, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.ui.btn_connect.clicked.connect(self.start_listen)
        self.ui.btn_disconnect.clicked.connect(self.stop_listen)
        
        self.ui.btn_get_gps.clicked.connect(self.get_gps)
        self.ui.btn_get_imu.clicked.connect(self.get_imu)
        self.ui.btn_write_man.clicked.connect(self.write_manual)
        
        self.port = QtSerialPort.QSerialPort()
        self.port.readyRead.connect(self.readFromSerial)
        
        self.msg_signals = Signals()

        self.estimator = EstimatorCS()
        
        self.msg_signals.get_gps.connect(self.actns_rcv_gps)
        self.msg_signals.get_imu.connect(lambda: print('imu получено'))
        self.msg_signals.get_man_perm.connect(lambda: print('ручная команда получена клиентом'))


    def start_listen(self):
        self.__init_serial_port()
        self.port.open(QIODevice.OpenModeFlag.ReadWrite)
        self.port.setDataTerminalReady(True)


    def stop_listen(self):
        self.port.clear()
        self.port.close()

      
    def __init_serial_port(self):
        self.port.setPortName("COM5")
        self.port.setBaudRate(QtSerialPort.QSerialPort.BaudRate.Baud115200)
        self.port.setParity(QtSerialPort.QSerialPort.Parity.NoParity)
        self.port.setDataBits(QtSerialPort.QSerialPort.DataBits.Data8)
        self.port.setStopBits(QtSerialPort.QSerialPort.StopBits.OneStop)

        
    def readFromSerial(self):
        
        _b_resp = self.port.readAll()
        _resp =  bytes(_b_resp ).decode()
        
        if _resp == 'D,s,4,GPS*\r\n': _resp = 'D,s,1,49,5949.08250,N,03019.66393,S,00155.5,2023,10,23,180723.00,0.004,*,96,\r,\n'
        if _resp == 'D,s,4,IMU*\r\n': _resp = 'D,s,2,65535,65535,65535,65535,65535,65535,65535,65535,65535,65535,185,*,81,\r,\n'
        
        if _resp[0:5] == 'D,s,1':
            #print('получение gps')
            self.msg_signals.get_gps.emit(_resp)
            
            
        if _resp[0:5] == 'D,s,2':
            #print('получение imu')
            self.msg_signals.get_imu.emit()
            
        if _resp[0:5] == 'D,s,3':
            #print('подтверждение отправки ручной команды')
            self.msg_signals.get_man_perm.emit()
            
    def get_gps(self):
        self.port.write(b'D,s,4,GPS*\r\n')
        
    def get_imu(self):
        self.port.write(b'D,s,4,IMU*\r\n')
        
    def write_manual(self):
        self.port.write(b'D,s,3,F,100*\r\n')

    @Slot(object)
    def actns_rcv_gps(self, rcv_msg):
        _calculatedCS = self.estimator.get_CS(rcv_msg)
        _parsedCS = int(rcv_msg.split(',')[-3:-2][0])

        if _calculatedCS != _parsedCS:
            print("Ошибка CRC")
            return -1
        
        if _calculatedCS == _parsedCS:
            print('Данные получены успешно')
            return 0
        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())