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
        self.on_off_button.clicked.connect(self.on_off_cliked)
        self.m1_input_box.valueChanged.connect(self.show_result)
        self.m2_input_box.valueChanged.connect(self.show_result)
        self.m3_input_box.valueChanged.connect(self.show_result)
        self.show()

    def on_off_cliked(self):
        print("ON/OFF CLICKED !!")

    def show_result(self):
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
