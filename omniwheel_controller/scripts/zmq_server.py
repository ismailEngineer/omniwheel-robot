import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    #  Wait for next request from client
    message = socket.recv_json()
    print("Received request: ",message)

    #  Do some 'work'
    time.sleep(1)

    # JSON MESSAGE 
    ret = {"a": 123, "b": 321}

    #  Send reply back to client
    socket.send_json(ret)