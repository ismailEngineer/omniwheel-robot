import RPi.GPIO as GPIO
from smbus import SMBus
import serial
import time

def init_all():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

def init_i2c(i2c_bus):
    bus = SMBus(1) # indicates /dev/ic2-1
    return bus

def setup_GPIOs_OUT(list_of_outputs_pins):
    for gpios in list_of_outputs_pins :
        GPIO.setup(gpios, GPIO.OUT)

def setup_GPIOs_IN(list_of_inputs_pins):
    for gpios in list_of_inputs_pins :
        GPIO.setup(gpios, GPIO.IN)

def turn_on_motors(list_of_motors):
    for id_m,state in list_of_motors :
        if state == 1 :
            GPIO.output(id_m, GPIO.HIGH)
        else :
            GPIO.output(id_m, GPIO.LOW)


def turn_on_output_gpio(gpio_num):
    GPIO.output(gpio_num, GPIO.HIGH)

def turn_off_output_gpio(gpio_num):
    GPIO.output(gpio_num, GPIO.LOW)

def get_input_value(gpio_num):
    input_state = GPIO.input(gpio_num)
    return input_state


def sent_message_i2c(bus,addr, message):
    bus.write_byte(addr, message) # switch it on


def init_serial(serial_adress):
    ser = serial.Serial(serial_adress, 9600)
    time.sleep(0.5)
    return ser


def close_serial(ser_obj):
    ser_obj.close()

def send_message_serial(ser_obj,message):
    ser_obj.write(message)
    time.sleep(0.5)


def move_forward(ser_obj,velocity):
    print("Moving Forward ...")
    message = 'M1:0;M2:'+str(velocity)+';M3:'+str(velocity)+'\n'
    message = message.encode('utf-8')
    send_message_serial(ser_obj,message)

def move_backward(ser_obj,velocity):
    print("Moving Backward ...")
    message = 'M1:0;M2:'+str(-velocity)+';M3:'+str(-velocity)+'\n'
    message = message.encode('utf-8')
    send_message_serial(ser_obj,message)
    

def turn_right(ser_obj,velocity):
    print("Turning Right ...")
    message = str('M1:'+str(-velocity)+';M2:'+str(-velocity)+';M3:'+str(velocity)+'\n')
    message = message.encode('utf-8')
    send_message_serial(ser_obj,message)

def turn_left(ser_obj,velocity):
    print("Turning Right ...")
    message = 'M1:'+str(velocity)+';M2:'+str(velocity)+';M3:'+str(-velocity)+'\n'
    message = message.encode('utf-8')
    send_message_serial(ser_obj,message)
