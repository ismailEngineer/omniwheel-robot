#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import zmq

def create_socket(ip_adress):
    context = zmq.Context()

    #  Socket to talk to server
    print("Connecting to hello world server…")
    socket = context.socket(zmq.REQ)

    # replace localhost by the ip adress of the server
    socket.connect("tcp://"+ip_adress+":5555")

    return socket

def init_json_message():
    # BUILD JSON
    robot_request = {
        "motor1":0,
        "motor2":0,
        "motor3":0,
        "lcd":1,
        "led":0
    }
    return robot_request

def edit_json_message(m1,m2,m3,lcd,led,robot_request):
    robot_request['motor1'] = m1
    robot_request['motor2'] = m2
    robot_request['motor3'] = m3
    robot_request['lcd'] = lcd
    robot_request['led'] = led

    return robot_request

def send_json_msg(socket,robot_request):
    print("Sending request  …")
    socket.send_json(robot_request)

    #  Get the reply.
    message = socket.recv_json()
    print("Received reply -->",message)