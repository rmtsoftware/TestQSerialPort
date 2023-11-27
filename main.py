from mainwindow import Ui_MainWindow
from PySide6 import QtWidgets, QtGui
from PySide6 import QtSerialPort
from PySide6.QtCore import QIODevice, QTimer, Signal, QObject, Slot
from PySide6 import QtCore
import sys
import ctypes


class EstimatorCS:
    def __init__(self):
        self.f = ctypes.cdll.LoadLibrary('.\\c_module\\checksum.dll')
        self.f.calculateChecksum.restype = ctypes.c_char
        self.f.calculateChecksum.argtypes = [ctypes.POINTER(ctypes.c_char), ]

    def get_CS(self, cmd):
        return ord(self.f.calculateChecksum(cmd.encode('utf-8')))

class Signals(QObject):
    get_gps = Signal(object)
    get_imu = Signal(object)
    get_man_perm = Signal(object)
    mov_forw = Signal()
    mov_back = Signal()
    mov_left = Signal()
    mov_right= Signal()


class Base:
    def start_listen(self): ...
    def stop_listen(self): ...
    def __init_serial_port(self): ...
    def readFromSerial(self): ...
    def get_gps(self): ...
    def get_imu(self): ...
    def write_manual(self): ...
    def actns_rcv_gps(self): ...
    def actns_rcv_imu(self): ...
    def actns_rcv_man_perm(self): ...
    def keyPressEvent(self): ...
    def actns_press_w(self): ...
    def actns_press_a(self): ...
    def actns_press_s(self): ...
    def actns_press_d(self): ...
    
    
    
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
        self.msg_signals.get_imu.connect(self.actns_rcv_imu)
        self.msg_signals.get_man_perm.connect(self.actns_rcv_man_perm)

        self._w_flag = False
        self._a_flag = False
        self._s_flag = False
        self._d_flag = False

        self._manCS = 0

        self.msg_signals.mov_forw.connect(self.actns_press_w)
        self.msg_signals.mov_back.connect(self.actns_press_s)
        self.msg_signals.mov_left.connect(self.actns_press_a)
        self.msg_signals.mov_right.connect(self.actns_press_d)


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
        
        DEBAG = True

        _b_resp = self.port.readAll()
        _resp =  bytes(_b_resp ).decode()
        
        if DEBAG == True:
            if _resp == 'D,s,4,GPS*\r\n': _resp = 'D,s,1,49,5949.08250,N,03019.66393,S,00155.5,2023,10,23,180723.00,0.004,*,96,\r,\n'
            if _resp == 'D,s,4,IMU*\r\n': _resp = 'D,s,2,65535,65535,65535,65535,65535,65535,65535,65535,65535,65535,185,*,81,\r,\n'
            if _resp == 'D,s,3,F,100*\r\n': _resp = 'D,s,3,*,27,\r,\n'
            if _resp == 'D,s,3,B,100*\r\n': _resp = 'D,s,3,*,31,\r,\n'
            if _resp == 'D,s,3,R,100*\r\n': _resp = 'D,s,3,*,15,\r,\n'
            if _resp == 'D,s,3,L,100*\r\n': _resp = 'D,s,3,*,17,\r,\n'
        
        if _resp[0:5] == 'D,s,1':
            self.msg_signals.get_gps.emit(_resp)
            
        if _resp[0:5] == 'D,s,2':
            self.msg_signals.get_imu.emit(_resp)
            
        if _resp[0:5] == 'D,s,3':
            self.msg_signals.get_man_perm.emit(_resp)


    def get_gps(self):
        self.port.write(b'D,s,4,GPS*\r\n')


    def get_imu(self):
        self.port.write(b'D,s,4,IMU*\r\n')


    def write_manual(self, direction):
        cmd = f'D,s,3,{direction},100*\r\n'
        self.port.write(bytes(cmd, 'utf-8'))
        self._manCS = self.estimator.get_CS(cmd)


    @Slot(object)
    def actns_rcv_gps(self, rcv_msg):
        _calculatedCS = self.estimator.get_CS(rcv_msg)
        _parsedCS = int(rcv_msg.split(',')[-3:-2][0])

        if _calculatedCS != _parsedCS:
            print("Ошибка CRC данных GPS")
            return -1
        
        if _calculatedCS == _parsedCS:
            print('GPS данные получены успешно')
            return 0


    @Slot(object)
    def actns_rcv_imu(self, rcv_msg):
        _calculatedCS = self.estimator.get_CS(rcv_msg)
        _parsedCS = int(rcv_msg.split(',')[-3:-2][0])

        if _calculatedCS != _parsedCS:
            print("Ошибка CRC данных IMU")
            return -1
        
        if _calculatedCS == _parsedCS:
            print('IMU данные получены успешно')
            return 0


    @Slot(object)
    def actns_rcv_man_perm(self, rcv_msg):
        try:
            _parsedCS = int(rcv_msg.split(',')[-3:-2][0])
        except Exception as e:
            print(e)

        if self._manCS != _parsedCS:
            print("Ошибка записи ручной команды")
            print(f"Получено: {rcv_msg}")
            return -1
        
        if self._manCS == _parsedCS:
            return 0
        

    def keyPressEvent(self, event):
        key_press = event.key()

        if key_press == QtCore.Qt.Key.Key_W:
            self.msg_signals.mov_forw.emit()

        if key_press == QtCore.Qt.Key.Key_S:
            self.msg_signals.mov_back.emit()

        if key_press == QtCore.Qt.Key.Key_A:
            self.msg_signals.mov_left.emit()

        if key_press == QtCore.Qt.Key.Key_D:
            self.msg_signals.mov_right.emit()

    
    def actns_press_w(self):

        def _reset_flag():
            self._w_flag = False

        if self._w_flag == True:
            return
        self._w_flag = True
        self.write_manual('F') # Forward
        print('Forward')
        QTimer.singleShot(500, _reset_flag)


    def actns_press_s(self):

        def _reset_flag():
            self._s_flag = False

        if self._s_flag == True:
            return
        self._s_flag = True
        self.write_manual('B') # Back
        print('Back')
        QTimer.singleShot(500, _reset_flag)


    def actns_press_a(self):

        def _reset_flag():
            self._a_flag = False

        if self._a_flag == True:
            return
        self._a_flag = True
        self.write_manual('L') # Left
        print('Left')
        QTimer.singleShot(500, _reset_flag)


    def actns_press_d(self):

        def _reset_flag():
            self._d_flag = False

        if self._d_flag == True:
            return
        self._d_flag = True 
        self.write_manual('R') # Right
        print('Right')
        QTimer.singleShot(500, _reset_flag)

        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())