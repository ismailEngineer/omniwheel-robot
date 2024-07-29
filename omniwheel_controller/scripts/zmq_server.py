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

    print("Motor1 : ",message["motor1"])
    print("Motor2 : ",message["motor2"])
    print("Motor3 : ",message["motor3"])
    print("LCD : ",message["lcd"])
    print("LED : ",message["led"])

    # JSON MESSAGE 
    ret = {"result": 0}

    #  Send reply back to client
    socket.send_json(ret)