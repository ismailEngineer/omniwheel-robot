import sys
from PyQt5 import QtWidgets, uic
from zmq_client import create_socket,init_json_message,edit_json_message,send_json_msg


# socket = create_socket("192.168.1.33")
# msg = init_json_message()
# msg = edit_json_message(1,2,3,5,6,msg)
# print(msg)
# send_json_msg(socket,msg)


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('../ui/controller.ui', self)
        self.m1_value = 0
        self.m2_value = 0
        self.m3_value = 0
        self.stop_motor_button.clicked.connect(self.stop_cliked)
        self.stop_button.clicked.connect(self.stop_cliked)
        self.go_button.clicked.connect(self.start_motor)
        self.set_max_button.clicked.connect(self.set_max_value)
        self.set_min_button.clicked.connect(self.set_min_value)
        self.reset_button.clicked.connect(self.set_min_value)
        self.show()

    def stop_cliked(self):
        print("STOP CLICKED !!")
        self.set_min_value()



    def set_max_value(self):
        self.m1_value = 255
        self.m2_value = 255
        self.m3_value = 255
        # change value in input box
        self.m1_input_box.setValue(self.m1_value)
        self.m2_input_box.setValue(self.m2_value)
        self.m3_input_box.setValue(self.m3_value)

    def set_min_value(self):
        self.m1_value = 0
        self.m2_value = 0
        self.m3_value = 0
        # change value in input box
        self.m1_input_box.setValue(self.m1_value)
        self.m2_input_box.setValue(self.m2_value)
        self.m3_input_box.setValue(self.m3_value)

    def start_motor(self):
        global socket
        print("IN ")
        m1 = self.m1_input_box.value()
        m2 = self.m2_input_box.value()
        m3 = self.m3_input_box.value()
        msg = init_json_message()
        msg = edit_json_message(m1,m2,m3,5,6,msg)
        send_json_msg(socket,msg) #bug of sending twice when using arrows of spinboxs
        print("OUT ")

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()

