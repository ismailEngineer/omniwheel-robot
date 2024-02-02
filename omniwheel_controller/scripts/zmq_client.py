#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import zmq

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)

# IP ADRESS 
ip_adress = "192.168.1.167"

# replace localhost by the ip adress of the server
socket.connect("tcp://"+ip_adress+":5555")

# BUILD JSON
Robot_request = {
    "motor1":0,
    "motor2":0,
    "motor3":0,
    "lcd":1,
    "led":0
}

#  Do 10 requests, waiting each time for a response
for request in range(10):
    print("Sending request  …", request)
    socket.send_json(Robot_request)

    #  Get the reply.
    message = socket.recv_json()
    print("Received reply -->",message)