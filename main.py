import sys
from PySide6.QtWidgets import QApplication, QMainWindow,QMessageBox
from PySide6.QtCore import QFile
from ui_mainwindow import Ui_MainWindow
import ui_mainwindow
import Motor_4
import canopen
import time
from PySide6.QtCore import QThread,Signal


class MainWindow(QMainWindow,ui_mainwindow.Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
       # self.ui = Ui_MainWindow()
       # self.ui.setupUi(self)
        self.setupUi(self)
        #self.turn_on_Button.clicked.connect(m.init)
        self.turn_on_Button.clicked.connect(self.turn_on_motor)
        #self.turn_on_Button.clicked.connect(self.start_threading())

        #self.turn_off_Button.clicked.connect(m.halt)
        self.turn_off_Button.clicked.connect(self.turn_off_motor)
        #self.turn_off_Button.clicked.connect(self.end_threading())

        self.Homingbutton.clicked.connect(m.Homing)

        #self.lineEdit.setEnabled(not self.vel_radio_button.isChecked())
        self.vel_radio_button.toggled.connect(self.lineEdit.setDisabled)


        #self.start_threading()
        self.reference_button.clicked.connect(self.set_reference)

        #self.start_threading_switch()
        self.start_motor.clicked.connect(self.select)
        self.stop_motor.clicked.connect(self.select_stop)

        #self.label_bit_0.setStyleSheet("background-color: red")

    def set_reference(self):
        # self.end_threading()
        # #self.thread_started.isRunning=False
        # m.relative_positioning(turns=1,velocity=0.2)
        # time.sleep(2)
        # while(True):
        #
        #
        #     if m.inquire_DIN6==34 :
        #         print(m.inquire_DIN6)
        #         pos_value=m.turns*360
        #         break
        # #pos_value = m.turns * 360
        # new_pos_value=(180+ pos_value ) /360
        # m.absolute_positioning(turns=new_pos_value,velocity=0.1)
        # time.sleep(5)
        # m.Homing()
        # self.start_threading()
        m.home_to_switch()
        cw_homing_done="0xc437"
        if m.status==cw_homing_done:

            m.Homing()
            self.pop_up_done()
        else :
            self.pop_up_fail()


    def pop_up_done(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Information")
        msg.setText("Referencing the motor done successfully, please proceed ")
        x = msg.exec()

    def pop_up_fail(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Information")
        msg.setText("Referencing the motor failed, please try again")
        x = msg.exec()

    def select(self):

        if self.rel_radio_button.isChecked():
            self.rel()
        if self.abs_radio_button.isChecked():
            self.abs()
        if self.vel_radio_button.isChecked():

            self.vel_mode()
    def vel_mode(self):

        try:
            #t = int(self.lineEdit.text())
            v = float(self.lineEdit_2.text())
        except:
            t = 0
            v = 0
        m.velocity_mode(target_velocity=v)
    def rel(self):  # m.relative_positioning(turns=4, velocity=1)

        try:
            t = int(self.lineEdit.text())
            if self.comboBox.currentIndex()==1:
                t=t/360
            v = float(self.lineEdit_2.text())
        except:
            t = 0
            v = 0
        m.relative_positioning(turns=t, velocity=v)

    def abs(self):  # m.absolute_positioning(turns=4, velocity=1)
        try:
            t = int(self.lineEdit.text())
            if self.comboBox.currentIndex()==1:
                t=t/360
            v = float(self.lineEdit_2.text())
        except:
            t = 0
            v = 0
        m.absolute_positioning(turns=t, velocity=v)
    def select_stop(self):
        if self.rel_radio_button.isChecked():
            try:
               t = int(self.lineEdit.text())
               if self.comboBox.currentIndex() == 1:
                   t=t/360
               # v = int(self.lineEdit_2.text())
            except:
                 t = 0
                 v = 0
            m.absolute_positioning(turns=t, velocity=0)

        if self.abs_radio_button.isChecked():

            m.absolute_positioning(turns=0,velocity=0)
        if self.vel_radio_button.isChecked():
            m.stop_velocity_mode()

    # def loadclicked1(self):
    #     # print(m.inquire_statusword())
    #     bool_str = m.inquire_statusword_bool()
    #     status_word = m.status
    #     str1 = 'Reference found is {0} , Commutation found is {1} ,'.format(bool_str[0], bool_str[1])
    #
    #     str2 = (' Reference error is {0} , Setpoint Acknowledge/Halt/Reference found is {1} ,'.format(bool_str[2], bool_str[3]))
    #     str3 = (' Internal limit active is {0} , Target reached is {1} ,'.format(bool_str[4], bool_str[5]))
    #     str4 = (' Reserved is {0} , Manufacturer specific  is {1} ,'.format(bool_str[6], bool_str[7]))
    #     str5 = (' Warning  is {0} , Switch on Disable is {1} ,'.format(bool_str[8], bool_str[9]))
    #     str6 = (' Quick Stop  is {0} , Voltage Enabled  is {1} ,'.format(bool_str[10], bool_str[11]))
    #     str7 = (' Fault is {0} , Operation Enable  is {1} ,'.format(bool_str[12], bool_str[13]))
    #     str8 = (' Switched on is {0} , Ready to switch on  is {1}.'.format(bool_str[14], bool_str[15]))
    #     str9 = (',   Status word is {0}.'.format(status_word))
    #     str = str1 + str2 + str3 + str4 + str5 + str6 + str7 + str8 + str9
    #     self.textBrowser.setText(str)
    #
    # def loadclicked2(self):
    #     actual_velocity = m.velocity
    #     str = ('actual velocity is  {0} U/s.'.format(m.velocity))
    #     self.textBrowser.setText(str)
    #
    # def loadclicked3(self):
    #     actual_postion = m.turns
    #     str = ('actual position is  {0} turns.'.format(m.turns))
    #     self.textBrowser.setText(str)

    def turn_on_motor(self):
       m.init()
       self.start_threading()

    def turn_off_motor(self):
       m.halt()
       time.sleep(1)
       self.end_threading()


    def start_threading(self):
        self.thread_started = ThreadClass()
        self.thread_started.start()
        self.thread_started.status_word_label_changed.connect(self.label_status_word_dis.setText)
        self.thread_started.label_actual_velocity_changed.connect(self.label_actual_velocity.setText)
        self.thread_started.label_actual_position_changed.connect(self.label_actual_position.setText)
        self.thread_started.label_actual_position_degree_changed.connect(self.label_actual_position_degree.setText)
        self.thread_started.Motor_status_changed.connect(self.Motor_status.setStyleSheet)
        self.thread_started.label_bit_0_changed.connect(self.label_bit_0.setStyleSheet)
        self.thread_started.label_bit_0_changed.connect(self.label_bit_0_copy.setStyleSheet)
        self.thread_started.label_bit_1_changed.connect(self.label_bit_1.setStyleSheet)
        self.thread_started.label_bit_2_changed.connect(self.label_bit_2.setStyleSheet)
        self.thread_started.label_bit_3_changed.connect(self.label_bit_3.setStyleSheet)
        self.thread_started.label_bit_4_changed.connect(self.label_bit_4.setStyleSheet)
        self.thread_started.label_bit_5_changed.connect(self.label_bit_5.setStyleSheet)
        self.thread_started.label_bit_6_changed.connect(self.label_bit_6.setStyleSheet)
        self.thread_started.label_bit_7_changed.connect(self.label_bit_7.setStyleSheet)
        self.thread_started.label_bit_8_changed.connect(self.label_bit_8.setStyleSheet)
        self.thread_started.label_bit_9_changed.connect(self.label_bit_9.setStyleSheet)
        self.thread_started.label_bit_10_changed.connect(self.label_bit_10.setStyleSheet)
        self.thread_started.label_bit_11_changed.connect(self.label_bit_11.setStyleSheet)
        self.thread_started.label_bit_12_changed.connect(self.label_bit_12.setStyleSheet)
        self.thread_started.label_bit_13_changed.connect(self.label_bit_13.setStyleSheet)
        self.thread_started.label_bit_14_changed.connect(self.label_bit_14.setStyleSheet)
        self.thread_started.label_bit_15_changed.connect(self.label_bit_15.setStyleSheet)
        self.thread_started.label_oPer_mode_dis_changed.connect(self.label_oPer_mode_dis.setText)

    # def start_threading_switch(self):
    #     self.thread_started_switch = ThreadClass_switch()
    #     self.thread_started_switch.start()



    def end_threading(self):
        #self.thread_started = ThreadClass()

        #self.thread_started.quit()
        #self.thread_started.terminate()
        self.thread_started.stop()
        #self.thread_started.isRunning=False

# class ThreadClass_switch(QThread):
#     switch_status_changed = Signal(str)
#     def __init__(self, parent=None):
#         QThread.__init__(self, parent=parent)
#         self.isRunning = True

    # def run(self):
    #     while self.isRunning:
    #
    #      print(m.inquire_DIN6())



class ThreadClass(QThread):
    status_word_label_changed = Signal(str)
    label_actual_velocity_changed = Signal(str)
    label_actual_position_changed = Signal(str)
    label_actual_position_degree_changed = Signal(str)
    Motor_status_changed = Signal(str)
    label_bit_0_changed = Signal(str)
    label_bit_1_changed = Signal(str)
    label_bit_2_changed = Signal(str)
    label_bit_3_changed = Signal(str)
    label_bit_4_changed = Signal(str)
    label_bit_5_changed = Signal(str)
    label_bit_6_changed = Signal(str)
    label_bit_7_changed = Signal(str)
    label_bit_8_changed = Signal(str)
    label_bit_9_changed = Signal(str)
    label_bit_10_changed = Signal(str)
    label_bit_11_changed = Signal(str)
    label_bit_12_changed = Signal(str)
    label_bit_13_changed = Signal(str)
    label_bit_14_changed = Signal(str)
    label_bit_15_changed = Signal(str)
    label_oPer_mode_dis_changed=Signal(str)
    #label_bit_0_changed= Signal(str)
    def __init__(self, parent=None):
        QThread.__init__(self, parent=parent)
        self.isRunning = True


    def run(self):

        while self.isRunning:
            #print(5)
            time.sleep(0.3)
            self.label_oPer_mode_dis_changed.emit(str(m.operating_mode))
            time.sleep(0.3)
            on_str="background-color: green"
            off_str="background-color: red"
            if m.status==m.sw_turned_off_1 or m.status==m.sw_turned_off_2  :
                self.Motor_status_changed.emit(str(off_str))
            else:
                self.Motor_status_changed.emit(str(on_str))
            time.sleep(0.1)
            self.status_word_label_changed.emit(str(m.status))
            time.sleep(0.1)
            self.label_actual_velocity_changed.emit(str(m.velocity))
            time.sleep(0.1)
            self.label_actual_position_changed.emit(str(m.turns))
            time.sleep(0.1)
            self.label_actual_position_degree_changed.emit(str(m.turns*360))
            time.sleep(0.1)
            bool_str = m.inquire_statusword_bool()
            if bool_str[0] == True:
                self.label_bit_0_changed.emit(str("background-color: green"))
            else:
                self.label_bit_0_changed.emit(str("background-color: red"))
            if bool_str[1] == True:
                self.label_bit_1_changed.emit(str("background-color: green"))
            else:
                self.label_bit_1_changed.emit(str("background-color: red"))
            if bool_str[2] == True:
                self.label_bit_2_changed.emit(str("background-color: green"))
            else:
                self.label_bit_2_changed.emit(str("background-color: red"))
            if bool_str[3] == True:
                self.label_bit_3_changed.emit(str("background-color: green"))
            else:
                self.label_bit_3_changed.emit(str("background-color: red"))
            if bool_str[4] == True:
                self.label_bit_4_changed.emit(str("background-color: green"))
            else:
                self.label_bit_4_changed.emit(str("background-color: red"))
            if bool_str[5] == True:
                self.label_bit_5_changed.emit(str("background-color: green"))
            else:
                self.label_bit_5_changed.emit(str("background-color: red"))
            if bool_str[6] == True:
                self.label_bit_6_changed.emit(str("background-color: green"))
            else:
                self.label_bit_6_changed.emit(str("background-color: red"))
            if bool_str[7] == True:
                self.label_bit_7_changed.emit(str("background-color: green"))
            else:
                self.label_bit_7_changed.emit(str("background-color: red"))
            if bool_str[8] == True:
                self.label_bit_8_changed.emit(str("background-color: green"))
            else:
                self.label_bit_8_changed.emit(str("background-color: red"))
            if bool_str[9] == True:
                self.label_bit_9_changed.emit(str("background-color: green"))
            else:
                self.label_bit_9_changed.emit(str("background-color: red"))
            if bool_str[10] == True:
                self.label_bit_10_changed.emit(str("background-color: green"))
            else:
                self.label_bit_10_changed.emit(str("background-color: red"))
            if bool_str[11] == True:
                self.label_bit_11_changed.emit(str("background-color: green"))
            else:
                self.label_bit_11_changed.emit(str("background-color: red"))
            if bool_str[12] == True:
                self.label_bit_12_changed.emit(str("background-color: green"))
            else:
                self.label_bit_12_changed.emit(str("background-color: red"))
            if bool_str[13] == True:
                self.label_bit_13_changed.emit(str("background-color: green"))
            else:
                self.label_bit_13_changed.emit(str("background-color: red"))
            if bool_str[14] == True:
                self.label_bit_14_changed.emit(str("background-color: green"))
            else:
                self.label_bit_14_changed.emit(str("background-color: red"))
            if bool_str[15] == True:
                self.label_bit_15_changed.emit(str("background-color: green"))
            else:
                self.label_bit_15_changed.emit(str("background-color: red"))



    def stop(self):
        self.isRunning = False
        #self.quit()
        #self.quit()
        #self.terminate()




if __name__ == "__main__":
    network = canopen.Network()
    network.connect(bustype='pcan', channel='PCAN_USBBUS1', bitrate=1000000)
    # Add some nodes with corresponding Object Dictionaries

    _node = canopen.RemoteNode(1, 'EcoVARIO_114_214_414.eds')
    network.add_node(_node)
    m = Motor_4.Motor(_node)


    app = QApplication(sys.argv)
    gui = MainWindow()
    # setup stylesheet
   # apply_stylesheet(app, theme='light_red.xml')
    window = MainWindow()
    window.show()

    sys.exit(app.exec())
