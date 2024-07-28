import RPi.GPIO as GPIO


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
