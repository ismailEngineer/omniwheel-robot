from flask import Flask, render_template, request, jsonify
import sys
import argparse
import sys
import math

app = Flask(__name__)

led_pin = 18
output_pins = [led_pin] # 
button_pin = 17
input_pins = [button_pin] # 
bus = None
serial_object = None

def configurationGpioFN():
    global serial_object
    # Configuration des GPIO
    led_pin = 18
    output_pins = [led_pin] # 
    button_pin = 17
    input_pins = [button_pin] # 
    init_all()
    bus = init_i2c(1) # indicates /dev/ic2-1
    serial_object = init_serial('/dev/ttyUSB0')
    setup_GPIOs_OUT(output_pins)
    setup_GPIOs_IN(input_pins) 

value_to_display = 0

# Configure i2C adress
arduino_addr = 0x8 # bus arduino_address

def app_init(setup_option):
    if setup_option == "real":
        print("Initi REAL mode")
    else : 
        print("Initi Simulation mode")

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
    global value_to_display,serial_object
    data, device, state = get_request()
    print(f"ARGS : {args.env}")

    if (device == 'motor1' or  device == 'motor2' or  device == 'motor3') and args.env == "raspberry":
        if state == 'on':
            turn_on_output_gpio(led_pin)
            if device == 'motor1': 
                move_forward(serial_object,150)
            elif device == 'motor2':
                move_backward(serial_object,150)
            elif device == 'motor3':
                turn_right(serial_object,100)
            #sent_message_i2c(bus,arduino_addr,0x10)
        else:
            turn_off_output_gpio(led_pin)
            send_message_serial(serial_object,b'M1:0;M2:-0;M3:0\n')
            #sent_message_i2c(bus,arduino_addr,0x0)

    value_to_display += 1
    
    return jsonify({'status': 'OK'})

@app.route('/get_value', methods=['GET'])
def get_value():
    global value_to_display
    return jsonify({'value': value_to_display})


@app.route('/read_input', methods=['GET'])
def read_input():
    if args.env == "raspberry":
        # Lire l'état de la broche d'entrée
        input_state = get_input_value(button_pin)
        return jsonify({'input_state': input_state})
    else :
        return jsonify({'input_state': "-1"})
    
@app.route('/joystick', methods=['POST'])
def joystick():
    data = request.get_json()
    x = data['x']
    y = data['y']

    # KINEMATIQUE INVERSE
    # M1 (0°)
    #W1 = y
    W1 = -x

    # M2 (120°)
    #W2 = - (math.sqrt(3)/2)*x - 0.5*y
    W2 = 0.5*x + (math.sqrt(3)/2)*y

    # M3 (240°)
    #W3 = (math.sqrt(3)/2)*x - 0.5*y
    W2 = -0.5*x + (math.sqrt(3)/2)*y

    # Affiche ou envoie à ton robot
    print(f'X={x:.2f} Y={y:.2f}')
    print(f'M1={W1:.2f} M2={W2:.2f} M3={W3:.2f}')

    m1, m2, m3 = scale_motor_speeds(W1, W2, W3)

    print(f"Vitesses moteurs: M1={m1:.0f}, M2={m2:.0f}, M3={m3:.0f}")

    turnMotors(serial_object,m1,m2,m3)

    # ➕ à adapter : envoyer les vitesses au robot via serial, socket, etc.

    return jsonify({"m1": W1, "m2": W2, "m3": W3})

def scale_motor_speeds(w1, w2, w3, min_speed=70, max_speed=220):
    # Trouver le plus grand coefficient absolu
    max_coef = max(abs(w1), abs(w2), abs(w3))

    # Éviter division par 0 (joystick au centre)
    if max_coef == 0:
        return 0, 0, 0

    # Calcul du facteur d'échelle
    scale = max_speed / max_coef

    # Appliquer l’échelle et clipper les vitesses minimales
    def scale_and_clip(w):
        if w == 0:
            return 0
        scaled = w * scale
        # appliquer vitesse min tout en gardant le signe
        if abs(scaled) < min_speed:
            return min_speed * (1 if scaled > 0 else -1)
        return scaled

    return (
        scale_and_clip(w1),
        scale_and_clip(w2),
        scale_and_clip(w3)
    )

if __name__ == '__main__':
    print(sys.argv)
    #app_init(sys.argv)
    

    # Créer un parseur d'arguments
    parser = argparse.ArgumentParser(description="Script pour différents environnements.")
    parser.add_argument(
        "--env", 
        choices=["raspberry", "development"], 
        required=True, 
        help="Spécifiez l'environnement : 'raspberry' pour la Raspberry Pi ou 'development' pour le PC."
    )
    args = parser.parse_args()

    # Utiliser l'argument pour conditionner l'importation
    if args.env == "raspberry":
        try:
            from hardware_control import *  # Importer tout depuis le module lié au hardware
            print("Mode Raspberry Pi : bibliothèque et script hardware_control importés.")
            configurationGpioFN()
            app.run(host='0.0.0.0', port=5000)
        except ImportError as e:
            print(f"Erreur : {e}")
            sys.exit("Impossible d'importer RPi.GPIO ou hardware_control sur cet environnement.")
    else:
        print("Mode développement : RPi.GPIO et hardware_control ignorés.")
        app.run(host='0.0.0.0', port=5000)