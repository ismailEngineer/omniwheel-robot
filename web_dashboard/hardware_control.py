import RPi.GPIO as GPIO
from smbus import SMBus


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