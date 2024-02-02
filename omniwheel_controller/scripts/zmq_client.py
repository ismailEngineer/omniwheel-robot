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
socket.connect("tcp:/"+ip_adress+":5555")

# BUILD JSON
Robot_request = {
    "Motor1":0,
    "Motor2":0,
    "Motor3":0,
    "LCD":1,
    "LED":0
}

#  Do 10 requests, waiting each time for a response
for request in range(10):
    print("Sending request  …", request)
    socket.send_json(Robot_request)

    #  Get the reply.
    message = socket.recv_json()
    print("Received reply -->",message)