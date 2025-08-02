import serial
import time

# Ouvre le port série (ajuste si nécessaire)
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
time.sleep(2)
ser.flush()

# Fichier pour stocker les données
fichier = open("donnees_vitesse.txt", "a")

print("Le script est prêt. Taper 'yes' pour démarrer la séquence.")
demarrage = input("Démarrer ? (yes/no) > ")

if demarrage.lower() != "yes":
    print("Arrêt du script.")
    fichier.close()
    ser.close()
    exit()

# Étape 1 : envoie du caractère 'z' pour dire à l'Arduino de commencer
ser.write(b'z')
print("Commande 'z' envoyée à l'Arduino pour commencer.")

# Étape 2 : demande des vitesses
try:
    m1 = float(input("Vitesse moteur 1 (M1) : "))
    m2 = float(input("Vitesse moteur 2 (M2) : "))
    m3 = float(input("Vitesse moteur 3 (M3) : "))

    # Formate la chaîne : M1:10;M2:-10;M3:30\n
    commande = f"M1:{m1};M2:{m2};M3:{m3}\n"
    ser.write(commande.encode())
    print("Commande envoyée :", commande.strip())

except ValueError:
    print("Entrée invalide, vérifie les vitesses.")
    fichier.close()
    ser.close()
    exit()

# === Lecture et enregistrement des vitesses reçues de l'Arduino ===
print("\nDémarrage de la lecture série et enregistrement...\n")

try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8',errors='ignore').strip()
            print("Ligne brute :", line)

            try:
                parts = line.split("|")
                v1 = float(parts[0].split(":")[1].strip())
                v2 = float(parts[1].split(":")[1].strip())
                v3 = float(parts[2].split(":")[1].strip())

                timestamp = time.time()
                print(f"[{timestamp:.2f}] v1={v1}, v2={v2}, v3={v3}")

                ligne_txt = f"{timestamp:.2f}, {v1}, {v2}, {v3}\n"
                fichier.write(ligne_txt)
                fichier.flush()

            except Exception as e:
                print("Erreur parsing :", e)

except KeyboardInterrupt:
    print("\nArrêt manuel par l'utilisateur.")
    fichier.close()
    ser.close()
