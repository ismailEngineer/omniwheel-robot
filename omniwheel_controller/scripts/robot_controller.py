import numpy as np
import serial
import time


# Distance du centre du robot aux roues (m)
L = 0.13  # 13 cm
sqrt3 = np.sqrt(3)


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

menu = {
    "1": ("Avancer", avancer),
    "2": ("Reculer", reculer),
    "3": ("Droite", aller_droite),
    "4": ("Gauche", aller_gauche),
    "5": ("Tourner à gauche", rotation_gauche),
    "6": ("Tourner à droite", rotation_droite),
    "0": ("Stop", arret),
}

def afficher_menu():
    print("\n--- Commandes disponibles ---")
    for key, (desc, _) in menu.items():
        print(f"{key} - {desc}")
    print("q - Quitter")

ser = init_serial_arduino()
enabe_motor_arduino(ser=ser)
while True:
    afficher_menu()
    choix = input("Entrez votre commande : ").strip().lower()

    if choix in ("q", "quit"):
        print("Fermeture...")
        break

    if choix in menu:
        nom, fonction = menu[choix]
        commande = fonction()
        print(f"> Commande {nom} : {commande}")
        send_message(ser,commande)
        # ser.write((commande + '\n').encode('utf-8'))  # décommente pour envoyer en série
    else:
        print("Commande non reconnue.")

# # Exemple d’utilisation
# if __name__ == "__main__":
#     ser = init_serial_arduino()
#     print("Commande avancer :", send_message(ser,avancer()))
#     print("Commande droite :", send_message(ser,aller_droite()))
#     print("Commande gauche :", send_message(ser,aller_gauche()))
#     print("Commande rotation gauche :", send_message(ser,rotation_gauche()))
#     print("Commande rotation droite :", send_message(ser,rotation_droite()))
#     print("Commande stop :", send_message(ser,arret()))
