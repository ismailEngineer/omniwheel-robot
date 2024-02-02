import sys
from PyQt5 import QtWidgets, uic
from zmq_client import create_socket,init_json_message,edit_json_message,send_json_msg


socket = create_socket("192.168.1.33")
msg = init_json_message()
msg = edit_json_message(1,2,3,5,6,msg)
print(msg)
send_json_msg(socket,msg)


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('../ui/controller.ui', self)
        self.show()

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
