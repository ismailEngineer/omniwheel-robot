from flask import Flask, render_template, request, jsonify
import RPi.GPIO as GPIO


from smbus import SMBus

app = Flask(__name__)

# Configuration des GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
led_pin = 18
button_pin = 17
GPIO.setup(led_pin, GPIO.OUT)
GPIO.setup(button_pin, GPIO.IN)
value_to_display = 0

# Configure i2C adress
addr = 0x8 # bus address
bus = SMBus(1) # indicates /dev/ic2-1


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/control', methods=['POST'])
def control():
    global value_to_display
    data = request.get_json()
    device = data['device']
    state = data['state']
    
    if device == 'motor1' or  device == 'motor2' or  device == 'motor3':
        if state == 'on':
            GPIO.output(led_pin, GPIO.HIGH)
            bus.write_byte(addr, 0x10) # switch it on
        else:
            GPIO.output(led_pin, GPIO.LOW)
            bus.write_byte(addr, 0x0) # switch it on
    elif device == 'any':
        if state == 'on':
            GPIO.output(motor_pin, GPIO.HIGH)
        else:
            GPIO.output(motor_pin, GPIO.LOW)

    value_to_display += 1
    
    return jsonify({'status': 'OK'})

@app.route('/get_value', methods=['GET'])
def get_value():
    global value_to_display
    return jsonify({'value': value_to_display})


@app.route('/read_input', methods=['GET'])
def read_input():
    # Lire l'état de la broche d'entrée
    input_state = GPIO.input(button_pin)
    return jsonify({'input_state': input_state})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


