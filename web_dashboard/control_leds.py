from flask import Flask, render_template, request, jsonify
from hardware_control import *


app = Flask(__name__)

# Configuration des GPIO
led_pin = 18
output_pins = [led_pin] # 
button_pin = 17
input_pins = [button_pin] # 
init_all()
bus = init_i2c(1) # indicates /dev/ic2-1
setup_GPIOs_OUT(output_pins)
setup_GPIOs_IN(input_pins)

value_to_display = 0

# Configure i2C adress
arduino_addr = 0x8 # bus arduino_address


def get_request():
    data = request.get_json()
    device = data['device']
    state = data['state']
    return(data,device,state)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/control', methods=['POST'])
def control():
    global value_to_display
    data, device, state = get_request()
    
    if device == 'motor1' or  device == 'motor2' or  device == 'motor3':
        if state == 'on':
            turn_on_output_gpio(led_pin)
            sent_message_i2c(bus,arduino_addr,0x10)
        else:
            turn_off_output_gpio(led_pin)
            sent_message_i2c(bus,arduino_addr,0x0)

    value_to_display += 1
    
    return jsonify({'status': 'OK'})

@app.route('/get_value', methods=['GET'])
def get_value():
    global value_to_display
    return jsonify({'value': value_to_display})


@app.route('/read_input', methods=['GET'])
def read_input():
    # Lire l'état de la broche d'entrée
    input_state = get_input_value(button_pin)
    return jsonify({'input_state': input_state})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


