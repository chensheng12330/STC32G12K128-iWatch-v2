import serial.tools.list_ports
import os
import sys
import time
import xlsxwriter
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import*
from PyQt5.QtCore import QTimer
from UI import *
from serialthread import *
import pyqtgraph as pg

#MainWindow.setWindowIcon(QtGui.QIcon(':/icon.ico'))

class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        # 初始化图表
        # 初始化温度图表
        self.graphicsViewA = pg.GraphicsLayoutWidget()
        self.plotA = self.graphicsViewA.addPlot(row=0, col=0, title="温度")
        self.plotA.showGrid(x=True, y=True)
        self.plotA.setLabel(axis="left", text="温度/℃")
        self.plotA.setLabel(axis="bottom", text="时间/100ms")
        self.plotA.addLegend()
        self.curveA = self.plotA.plot(pen=pg.mkPen("r", width=2), name="温度")
        # 初始化湿度图表
        self.plotB = self.graphicsViewA.addPlot(row=1, col=0, title="湿度")
        self.plotB.showGrid(x=True, y=True)
        self.plotB.setLabel(axis="left", text="湿度/%")
        self.plotB.setLabel(axis="bottom", text="时间/100ms")
        self.plotB.addLegend()
        self.curveB = self.plotB.plot(pen=pg.mkPen("g", width=2), name="湿度")
        # 初始化气压图表
        self.plotC = self.graphicsViewA.addPlot(row=2, col=0, title="气压")
        self.plotC.showGrid(x=True, y=True)
        self.plotC.setLabel(axis="left", text="气压/Pa")
        self.plotC.setLabel(axis="bottom", text="时间/50ms")
        self.plotC.addLegend()
        self.curveC = self.plotC.plot(pen=pg.mkPen("b", width=2), name="气压")
        # 初始化加速度和角速度数据图表
        self.graphicsViewD = pg.GraphicsLayoutWidget()
        self.plotD = self.graphicsViewD.addPlot(row=0, col=0, title="加速度")
        self.plotD.showGrid(x=True, y=True)
        self.plotD.setLabel(axis="left", text="加速度")
        self.plotD.setLabel(axis="bottom", text="时间/20ms")
        self.plotD.addLegend()
        self.curveAX = self.plotD.plot(pen=pg.mkPen("r", width=2), name="x")
        self.curveAY = self.plotD.plot(pen=pg.mkPen("g", width=2), name="y")
        self.curveAZ = self.plotD.plot(pen=pg.mkPen("b", width=2), name="z")
        self.plotG = self.graphicsViewD.addPlot(row=1, col=0, title="角速度")
        self.plotG.showGrid(x=True, y=True)
        self.plotG.setLabel(axis="left", text="角速度")
        self.plotG.setLabel(axis="bottom", text="时间/20ms")
        self.plotG.addLegend()
        self.curveGX = self.plotG.plot(pen=pg.mkPen("r", width=2), name="x")
        self.curveGY = self.plotG.plot(pen=pg.mkPen("g", width=2), name="y")
        self.curveGZ = self.plotG.plot(pen=pg.mkPen("b", width=2), name="z")
        # 初始化磁力计数据图表
        self.graphicsViewE = pg.GraphicsLayoutWidget()
        self.plotE = self.graphicsViewE.addPlot(title="三轴地磁数据")
        self.plotE.showGrid(x=True, y=True)
        self.plotE.setLabel(axis="left", text="磁场强度/高斯")
        self.plotE.setLabel(axis="bottom", text="时间/20ms")
        self.plotE.addLegend()
        self.curveMX = self.plotE.plot(pen=pg.mkPen("r", width=2), name="x")
        self.curveMY = self.plotE.plot(pen=pg.mkPen("g", width=2), name="y")
        self.curveMZ = self.plotE.plot(pen=pg.mkPen("b", width=2), name="z")
        # 初始化步数数据图表
        self.graphicsViewF = pg.GraphicsLayoutWidget()
        self.date_axis = pg.AxisItem(orientation='bottom')
        self.plotF = self.graphicsViewF.addPlot(title="过去七天的步数", axisItems={'bottom': self.date_axis})
        self.plotF.setLabel(axis="left", text="步数/步")
        self.plotF.setLabel(axis="bottom", text="日期")
        self.plotF.addLegend()
        self.barItem = pg.BarGraphItem(x=[0], height=[0], width=1, brush='b', name='步数')
        self.plotF.addItem(self.barItem)
        self.setPlotDisplay(0)
        # 初始化图表的数据
        self.HDC2080Data = [[], []]
        self.BMP390Data = []
        self.LSM6DSLData = [[], [], [], [], [], []]
        self.QMC5883LData = [[], [], []]
        self.data_mode = 1
        self.windowWidth = 100

        self.weekday_in_str = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
        # 串口连接状态指示
        self.is_serial_open = False
        # 使用一个定时器来更界面上的时间显示
        self.timer = QTimer()
        self.timer.timeout.connect(self.timeUpdate)
        self.timer.start(100)
        self.refreshSerialList()


    def timeUpdate(self):
        self.time = time.localtime(time.time())
        self.label_time.setText("%02d:%02d:%02d"%(self.time[3], self.time[4], self.time[5]))
        self.label_date.setText("%d年%d月%d日  %s"%(self.time[0], self.time[1], self.time[2], self.weekday_in_str[self.time[6]]))

    # 刷新串口列表
    def refreshSerialList(self):
        port_list = list(serial.tools.list_ports.comports())
        self.com_list = [['0'] * len(port_list), ['0'] * len(port_list)]  # 初始化com_list
        for i in range(0, len(port_list)):
            self.com_list[0][i] = port_list[i][0]
            self.com_list[1][i] = port_list[i][1]
        self.comboBox_serialList.clear()
        self.comboBox_serialList.addItems(self.com_list[1])
    # 串口连接
    def serialConnect(self):
        if self.is_serial_open == True:
            return
        try:
            self.serial = serial.Serial(self.com_list[0][self.comboBox_serialList.currentIndex()], 115200, timeout=0.01)
        except Exception:
            self.CreatWarmingDialog("串口打开失败！")
            return
        self.is_serial_open = True
        # 创建一个线程用于串口接收
        self.serialReceiveThread = SerialReceiveThread(self.serial)
        # 绑定信号接收槽函数
        self.serialReceiveThread.sinOut.connect(self.serialRxHandle)
        # 开始线程
        self.serialReceiveThread.start()
        self.pushButton_serialConnect.setDisabled(True)
        self.pushButton_serialDisconnect.setEnabled(True)
        cmd1 = "getConfig\r\n"
        self.serial.write(cmd1.encode("utf-8"))
        cmd1 = "getAlarm\r\n"
        self.serial.write(cmd1.encode("utf-8"))
        cmd1 = "setDataMode 0\r\n"
        self.serial.write(cmd1.encode("utf-8"))
    # 断开串口连接
    def serialDisconnect(self):
        if self.is_serial_open == False:
            return
        self.serialReceiveThread.stop()
        self.serialReceiveThread.deleteLater()
        self.serialReceiveThread.wait()
        self.serial.close()
        self.is_serial_open = False
        self.pushButton_serialConnect.setEnabled(True)
        self.pushButton_serialDisconnect.setDisabled(True)
    # 串口接收线程的信号槽，处理串口接受的信息
    def serialRxHandle(self, temp):
        # 手表设置信息
        if temp[0] == "CF":
            self.slider_screentime.setValue(int(temp[1]))
            self.label_1.setText(temp[1])
            self.slider_brightness.setValue(int(temp[2]))
            self.label_2.setText(temp[2])
            self.slider_brightness.setValue(int(temp[2]))
            self.checkBox_inverse.setCheckState(int(temp[3]))
            self.checkBox_AWT.setCheckState(int(temp[4]))
            self.checkBox_keysound.setCheckState(int(temp[5]))
        # 手表闹钟信息
        elif temp[0] == "AL":
            alarmMode = int(temp[1])
            alarmHour = int(temp[2])
            alarmMin = int(temp[3])
            alarmDay = int(temp[4])
            self.comboBox_alarmMode.setCurrentIndex(alarmMode)
            self.timeEdit_alarmTime.setTime(QTime(alarmHour, alarmMin))
            self.spinBox_alarmDay.setValue(alarmDay)
            self.setAlarmMode()
        elif temp[0] == "ST":
            time_str = [0,0,0,0,0,0,0]
            step = [0,0,0,0,0,0,0]
            for i in range(7):
                d = temp[i + 1].split(' ')
                time_str[i] = d[0]
                step[i] = int(d[1])
            xdict = dict(enumerate(time_str))
            self.plotF.removeItem(self.barItem)
            self.date_axis.setTicks([xdict.items()])
            self.barItem = pg.BarGraphItem(x = range(7), height = step, width=1, brush='b', name='步数')
            self.plotF.addItem(self.barItem)
        # 手表温度，湿度
        elif temp[0] == "TH":
            if self.data_mode == 1:
                for i in range(2):
                    self.HDC2080Data[i].append(float(temp[i + 1]))
                if len(self.HDC2080Data[0]) > self.windowWidth:
                    for i in range(2):
                        self.HDC2080Data[i] = self.HDC2080Data[i][1:]
                self.curveA.setData(self.HDC2080Data[0])
                self.curveB.setData(self.HDC2080Data[1])
        # 手表气压
        elif temp[0] == "PA":
            if self.data_mode == 1:
                self.BMP390Data.append(float(temp[1]))
                if len(self.BMP390Data) > self.windowWidth:
                    self.BMP390Data= self.BMP390Data[1:]
                self.curveC.setData(self.BMP390Data)
        # 手表加速度，角速度
        elif temp[0] == "AG":
            if self.data_mode == 2:
                for i in range(6):
                    self.LSM6DSLData[i].append(int(temp[i + 1]))
                if len(self.LSM6DSLData[0]) > self.windowWidth:
                    for i in range(6):
                        self.LSM6DSLData[i] = self.LSM6DSLData[i][1:]
                self.curveAX.setData(self.LSM6DSLData[0])
                self.curveAY.setData(self.LSM6DSLData[1])
                self.curveAZ.setData(self.LSM6DSLData[2])
                self.curveGX.setData(self.LSM6DSLData[3])
                self.curveGY.setData(self.LSM6DSLData[4])
                self.curveGZ.setData(self.LSM6DSLData[5])
        # 手表三轴地磁
        elif temp[0] == "MG":
            if self.data_mode == 3:
                for i in range(3):
                    self.QMC5883LData[i].append(int(temp[i + 1]))
                if len(self.QMC5883LData[0]) > self.windowWidth:
                    for i in range(3):
                        self.QMC5883LData[i] = self.QMC5883LData[i][1:]
                self.curveMX.setData(self.QMC5883LData[0])
                self.curveMY.setData(self.QMC5883LData[1])
                self.curveMZ.setData(self.QMC5883LData[2])
        # 手表应答消息
        elif temp[0] == "OK":
            self.statusBar.showMessage("设置成功", 1000)
    # 通过串口发送指令给手表
    def serialSendCmd(self):
        if self.is_serial_open == False:
            self.CreatWarmingDialog("串口未连接！")
            return
        sender = self.sender()
        if sender == self.pushButton_setTime:
            cmd1 = "setTime %d %d %d %d %d %d %d\r\n" % (
            self.time[0], self.time[1], self.time[2], self.time[3], self.time[4], self.time[5], self.time[6])
        elif sender == self.pushButton_setConfig:
            cmd1 = "setConfig %d %d %d %d %d\r\n" % (
            self.slider_screentime.value(), self.slider_brightness.value(), self.checkBox_inverse.isChecked(),
            self.checkBox_AWT.isChecked(), self.checkBox_keysound.isChecked())
        elif sender == self.pushButton_setAlarm:
            alarmMode = self.comboBox_alarmMode.currentIndex()
            alarmTime = self.timeEdit_alarmTime.time()
            alarmDay = self.spinBox_alarmDay.value()
            cmd1 = "setAlarm %d %d %d %d\r\n" % (alarmMode, alarmTime.hour(), alarmTime.minute(), alarmDay)
        elif sender == self.pushButton_startOrPause:
            if self.pushButton_startOrPause.text() == "开始":
                self.pushButton_startOrPause.setText("暂停")
                cmd1 = "setDataMode %d\r\n" % self.data_mode
            else:
                self.pushButton_startOrPause.setText("开始")
                cmd1 = "setDataMode 0\r\n"
        elif sender == self.comboBox_dataSelect:
            if self.comboBox_dataSelect.currentIndex() != 3:
                self.pushButton_startOrPause.setText("开始")
                cmd1 = "setDataMode 0\r\n"
            else:
                cmd1 = "getStep\r\n"
        elif sender == self.pushButton_setBLE:
            cmd1 = "AT+BM" + self.lineEdit_BLEName.text() + "\r\n"
        elif sender == self.pushButton_setSPP:
            cmd1 = "AT+BD" + self.lineEdit_SPPName.text() + "\r\n"
        elif sender == self.checkBox_BLEswitch:
            if self.checkBox_BLEswitch.isChecked() == 1:
                cmd1 = "AT+B401\r\n"
            else:
                cmd1 = "AT+B400\r\n"
        elif sender == self.checkBox_SPPswitch:
            if self.checkBox_SPPswitch.isChecked() == 1:
                cmd1 = "AT+B501\r\n"
            else:
                cmd1 = "AT+B500\r\n"
        self.serial.write(cmd1.encode("utf-8"))
        #print(cmd1)

    def setWindowWidth(self):
        self.windowWidth = self.slider_windowWidth.value()
    def setAlarmMode(self):
        alarmMode = self.comboBox_alarmMode.currentIndex()
        if alarmMode == 0:
            self.timeEdit_alarmTime.setEnabled(False)
            self.spinBox_alarmDay.setEnabled(False)
        elif alarmMode != 4:
            self.timeEdit_alarmTime.setEnabled(True)
            self.spinBox_alarmDay.setEnabled(False)
        else:
            self.timeEdit_alarmTime.setEnabled(True)
            self.spinBox_alarmDay.setEnabled(True)

    def setPlotDisplay(self, index):
        self.data_mode = index + 1
        for i in range(self.plotLayout_1.count()):
            self.plotLayout_1.itemAt(i).widget().hide()
            self.plotLayout_1.removeWidget(self.plotLayout_1.itemAt(i).widget())
        if index == 0:
            self.plotLayout_1.addWidget(self.graphicsViewA)
            self.graphicsViewA.show()
        elif index == 1:
            self.plotLayout_1.addWidget(self.graphicsViewD)
            self.graphicsViewD.show()
        elif index == 2:
            self.plotLayout_1.addWidget(self.graphicsViewE)
            self.graphicsViewE.show()
        elif index == 3:
            self.plotLayout_1.addWidget(self.graphicsViewF)
            self.graphicsViewF.show()
    def dataClear(self):
        if self.data_mode == 1:
            self.HDC2080Data[0].clear()
            self.HDC2080Data[1].clear()
            self.BMP390Data.clear()
            self.curveA.setData(self.HDC2080Data[0])
            self.curveB.setData(self.HDC2080Data[1])
            self.curveC.setData(self.BMP390Data)
        elif self.data_mode == 2:
            for i in range(6):
                self.LSM6DSLData[i].clear()
            self.curveAX.setData(self.LSM6DSLData[0])
            self.curveAY.setData(self.LSM6DSLData[1])
            self.curveAZ.setData(self.LSM6DSLData[2])
            self.curveGX.setData(self.LSM6DSLData[3])
            self.curveGY.setData(self.LSM6DSLData[4])
            self.curveGZ.setData(self.LSM6DSLData[5])
        elif self.data_mode == 3:
            for i in range(3):
                self.QMC5883LData[i].clear()
            self.curveMX.setData(self.QMC5883LData[0])
            self.curveMY.setData(self.QMC5883LData[1])
            self.curveMZ.setData(self.QMC5883LData[2])
    def dataSave(self):
        if self.data_mode == 1:
            n = len(self.HDC2080Data[0])
        elif self.data_mode == 2:
            n = len(self.LSM6DSLData[0])
        elif self.data_mode == 3:
            n = len(self.QMC5883LData[0])
        if n == 0:
            self.CreatWarmingDialog("没有可保存的数据！")
            return
        cwd = os.getcwd()  # 获取当前程序文件位置
        fileName_choose, filetype = QFileDialog.getSaveFileName(self, "保存数据", cwd, "表格(*.xlsx)")
        if fileName_choose == "":  # 没有输入文件名
            return
        workbook = xlsxwriter.Workbook(fileName_choose)  # 用输入的文件名创建一个excel文件
        worksheet = workbook.add_worksheet()  # 在这个excel文件中创建一个工作表
        if self.data_mode == 1:
            worksheet.write(0, 0, "temperature/℃")
            worksheet.write(0, 1, "humidity/%")
            worksheet.write(0, 2, "pressure/Pa")
            for i in range(len(self.HDC2080Data[0])):
                worksheet.write(1 + i, 0, self.HDC2080Data[0][i])
                worksheet.write(1 + i, 1, self.HDC2080Data[1][i])
            for i in range(len(self.BMP390Data)):
                worksheet.write(1 + i, 2, self.BMP390Data[i])
        elif self.data_mode == 2:
            worksheet.write(0, 0, "AccX")
            worksheet.write(0, 1, "AccY")
            worksheet.write(0, 2, "AccZ")
            worksheet.write(0, 3, "GyrX")
            worksheet.write(0, 4, "GyrY")
            worksheet.write(0, 5, "GyrZ")
            for i in range(6):
                for j in range(len(self.LSM6DSLData[0])):
                    worksheet.write(1 + j, i, self.LSM6DSLData[i][j])
        elif self.data_mode == 3:
            worksheet.write(0, 0, "MagX")
            worksheet.write(0, 1, "MagY")
            worksheet.write(0, 2, "MagZ")
            for i in range(3):
                for j in range(len(self.QMC5883LData[0])):
                    worksheet.write(1 + j, i, self.QMC5883LData[i][j])
        workbook.close()
        self.CreatWarmingDialog("保存成功")
        return

    # 创建一个提示窗口
    def CreatWarmingDialog(self, message):
        self.di = QDialog()
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(14)
        self.di.setFont(font)
        self.di.setFixedSize(220, 120)
        self.di.setWindowTitle("提示")
        self.di.setWindowIcon(QIcon(':/warming.ico'))
        hbox = QHBoxLayout()
        lable = QLabel()
        lable.setText(message)
        hbox.addWidget(lable)
        lable.setAlignment(QtCore.Qt.AlignCenter)
        self.di.setLayout(hbox)
        self.di.show()
        self.di.exec_()
    # 关闭界面窗口时，会执行这个函数
    def closeEvent(self, event):
        # 关闭线程及串口
        if self.is_serial_open == True:
            self.serialReceiveThread.stop()
            self.serialReceiveThread.deleteLater()
            self.serialReceiveThread.wait()
            self.serial.close()



if __name__ == "__main__":
    # 每一pyqt5应用程序必须创建一个应用程序对象。sys.argv参数是一个列表，从命令行输入参数。
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    # 显示在屏幕上
    myWin.show()
    sys.exit(app.exec_())