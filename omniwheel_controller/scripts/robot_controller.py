import numpy as np
import threading
import serial
import time
import socket


# Distance du centre du robot aux roues (m)
L = 0.13  # 13 cm
sqrt3 = np.sqrt(3)

# Threading : 
lock = threading.Lock()
    # Variables partagées
v1, v2, v3 = 0.0, 0.0, 0.0
    # Signal d'arrêt
stop_event = threading.Event()


# Socket config
HOST = '0.0.0.0'  # Pour écouter sur toutes les IP de la Raspberry
PORT = 5000

def init_serial_arduino():
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    time.sleep(2)
    ser.flush()
    return ser

def enabe_motor_arduino(ser):
    # Étape 1 : envoie du caractère 'z' pour dire à l'Arduino de commencer
    ser.write(b'z')
    print("Commande 'z' envoyée à l'Arduino pour commencer.")

def send_message(ser,commande):
    ser.write(commande.encode())
    return commande

def calcul_vitesses_moteurs(Vx, Vy, W):
    """
    À partir de Vx, Vy (m/s) et W (rad/s), calcule V1, V2, V3
    """
    V1 = Vx + (W * L)
    V2 = -0.5 * Vx - (sqrt3 / 2) * Vy + (W * L)
    V3 = -0.5 * Vx + (sqrt3 / 2) * Vy + (W * L)
    return V1, V2, V3

def generer_commande(V1, V2, V3):
    """
    Formate les vitesses pour l'envoi série
    """
    return f"M1:{(V1*100):.2f};M2:{(V2*100):.2f};M3:{(V3*100):.2f}\n"

# Commandes de mouvement
def avancer(v=0.4):  # m/s
    return generer_commande(*calcul_vitesses_moteurs(0, v, 0))

def reculer(v=0.4):
    return generer_commande(*calcul_vitesses_moteurs(0, -v, 0))

def aller_droite(v=0.4):
    return generer_commande(*calcul_vitesses_moteurs(v, 0, 0))

def aller_gauche(v=0.4):
    return generer_commande(*calcul_vitesses_moteurs(-v, 0, 0))

def rotation_gauche(w=1.5):  # rad/s
    return generer_commande(*calcul_vitesses_moteurs(0, 0, w))

def rotation_droite(w=1.5):
    return generer_commande(*calcul_vitesses_moteurs(0, 0, -w))

def arret():
    return generer_commande(0, 0, 0)

# Initialisation Serial
ser = init_serial_arduino()
# Enable motor (SEND UART MESSAGE TO ARDUINO)
enabe_motor_arduino(ser=ser)



# Socket serveur
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(1)


print(f"Serveur en attente de connexion sur {HOST}:{PORT}...")
conn, addr = server_socket.accept()
print(f"Client connecté depuis {addr}")


menu = {
    "1": ("Avancer", avancer),
    "2": ("Reculer", reculer),
    "3": ("Droite", aller_droite),
    "4": ("Gauche", aller_gauche),
    "5": ("Tourner à gauche", rotation_gauche),
    "6": ("Tourner à droite", rotation_droite),
    "0": ("Stop", arret),
}

def lecture_vitesse_legacy():
    global v1, v2, v3
    while not stop_event.is_set():
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            try:
                parts = line.split("|")
                v1_new = float(parts[0].split(":")[1].strip())
                v2_new = float(parts[1].split(":")[1].strip())
                v3_new = float(parts[2].split(":")[1].strip())
                timestamp = time.time()
                with lock:
                    v1, v2, v3 = v1_new, v2_new, v3_new
                    msg = f"{timestamp:.2f},{v1:.2f},{v2:.2f},{v3:.2f}\n"
                conn.sendall(msg.encode())
            except Exception as e:
                print("Erreur parsing:", e)

        
        #time.sleep(0.1)  # 10 Hz
def lecture_vitesse():
    global v1, v2, v3, conn
    serial_buffer = ""

    while not stop_event.is_set():
        try:
            if ser.in_waiting > 0:
                # Lire tous les caractères disponibles
                chunk = ser.read(ser.in_waiting or 1).decode('utf-8', errors='ignore')
                serial_buffer += chunk

                # Tant qu'il y a une ligne complète
                while '\n' in serial_buffer:
                    line, serial_buffer = serial_buffer.split('\n', 1)
                    line = line.strip()

                    try:
                        parts = line.split("|")
                        if len(parts) < 3:
                            print("⚠️ Ligne incomplète :", line)
                            continue

                        v1_new = float(parts[0].split(":")[1].strip())
                        v2_new = float(parts[1].split(":")[1].strip())
                        v3_new = float(parts[2].split(":")[1].strip())
                        timestamp = time.time()

                        with lock:
                            v1, v2, v3 = v1_new, v2_new, v3_new
                            msg = f"{timestamp:.2f},{v1:.2f},{v2:.2f},{v3:.2f}\n"

                        try:
                            conn.sendall(msg.encode())
                        except BrokenPipeError:
                            print("❌ Connexion TCP perdue (Broken Pipe)")
                            stop_event.set()
                            break

                    except (IndexError, ValueError) as e:
                        print("⚠️ Erreur de parsing:", e, "dans la ligne :", line)

        except Exception as e:
            print("❌ Erreur dans lecture_vitesse:", e)
            stop_event.set()
            break
# Lancement du thread
thread = threading.Thread(target=lecture_vitesse)
thread.start() 

def afficher_menu():
    print("\n--- Commandes disponibles ---")
    for key, (desc, _) in menu.items():
        print(f"{key} - {desc}")
    print("q - Quitter")



try : 
    while True:
        afficher_menu()
        choix = input("Entrez votre commande : ").strip().lower()

        if choix in ("q", "quit"):
            print("Fermeture...")
            stop_event.set()
            thread.join()
            ser.close()
            conn.close()
            server_socket.close()
            break

        # with lock:
        #     msg = f"{v1:.2f},{v2:.2f},{v3:.2f}\n"
        # conn.sendall(msg.encode())
        # time.sleep(0.1)  # 10 Hz

        if choix in menu:
            nom, fonction = menu[choix]
            commande = fonction()
            print(f"> Commande {nom} : {commande}")
            send_message(ser,commande)

        else:
            print("Commande non reconnue.")

except KeyboardInterrupt:
    print("Arrêt demandé par l'utilisateur.")
    stop_event.set()
    thread.join()
    ser.close()
    conn.close()
    server_socket.close()
    print("Fermeture propre terminée.")
