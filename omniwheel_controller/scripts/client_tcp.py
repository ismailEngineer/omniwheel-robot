# client_pc.py
import socket

RASPBERRY_IP = '192.168.1.167'  # ← Remplace avec l'adresse IP réelle de la Raspberry
PORT = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((RASPBERRY_IP, PORT))

print("Connecté au serveur Raspberry.")

try:
    while True:
        data = client_socket.recv(1024).decode().strip()
        if data:
            v1, v2, v3 = map(float, data.split(","))
            print(f"Réception → V1={v1}, V2={v2}, V3={v3}")
except KeyboardInterrupt:
    print("Déconnexion...")
    client_socket.close()