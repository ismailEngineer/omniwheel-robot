from flask import Flask, render_template, request, jsonify
import sys
import argparse
import sys

app = Flask(__name__)

led_pin = 18
output_pins = [led_pin] # 
button_pin = 17
input_pins = [button_pin] # 
bus = None

def configurationGpioFN():
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
    return render_template('refactor.html')

@app.route('/control', methods=['POST'])
def control():
    global value_to_display
    data, device, state = get_request()
    print(f"ARGS : {args.env}")
    
    if (device == 'motor1' or  device == 'motor2' or  device == 'motor3') and args.env == "raspberry":
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
    if args.env == "raspberry":
        # Lire l'état de la broche d'entrée
        input_state = get_input_value(button_pin)
        return jsonify({'input_state': input_state})
    else :
        return jsonify({'input_state': "-1"})

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