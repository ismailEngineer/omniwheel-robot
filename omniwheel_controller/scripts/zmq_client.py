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
# replace localhost by the ip adress of the server
socket.connect("tcp://localhost:5555")

#  Do 10 requests, waiting each time for a response
for request in range(10):
    request = {"ID": 123, "name": 321}
    print("Sending request  …", request)
    socket.send_json(request)

    #  Get the reply.
    message = socket.recv_json()
    print("Received reply -->",message)