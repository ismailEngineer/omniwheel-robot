# client_pc.py
import socket
import numpy as np 
import math
import matplotlib.pyplot as plt

# Distance du centre du robot aux roues (m)
L = 0.13  # 13 cm
sqrt3 = np.sqrt(3)


def plot_robot_trajectory(x, y, theta, step=10, arrow_length=0.1):
    """
    Affiche la trajectoire (x, y) du robot avec des flèches indiquant l'orientation.

    Arguments :
        x : tableau des positions en x
        y : tableau des positions en y
        theta : tableau des orientations en radians
        step : espacement entre les flèches (par défaut 10)
        arrow_length : taille des flèches (par défaut 0.1)
    """
    x = np.array(x)
    y = np.array(y)
    theta = np.array(theta)

    plt.figure(figsize=(8, 8))
    plt.plot(x, y, label='Trajectoire', color='blue')

    # Ajout des flèches pour montrer l'orientation
    for i in range(0, len(x), step):
        dx = arrow_length * np.cos(theta[i])
        dy = arrow_length * np.sin(theta[i])
        plt.arrow(x[i], y[i], dx, dy, head_width=0.05, head_length=0.05, color='red')

    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.title("Trajectoire du robot avec orientation")
    plt.axis('equal')
    plt.grid(True)
    plt.legend()
    plt.show()

def Kinematic_direct(V1,V2,V3): 
    Vx = -0.5 * V3 - 0.5 * V2 + V1
    Vy = sqrt3 * V3 - sqrt3 * V2 
    Wz = (1/L) * V3 + (1/L) * V2 + (1/L) * V1
    return (Vx,Vy,Wz)

def Kinematic_reverse(Vx,Vy,Wz): 
    V1 = Vx + (Wz * L)
    V2 = -0.5 * Vx - (sqrt3 / 2) * Vy + (Wz * L)
    V3 = -0.5 * Vx + (sqrt3 / 2) * Vy + (Wz * L)
    return V1, V2, V3

def update_odometry(x,y,theta,Vx,Vy,Wz,dt):
    dx = math.cos(theta) * Vx - math.sin(theta) * Vy
    dy = math.sin(theta) * Vx + math.cos(theta) * Vy

    x_new = x + dx * dt
    y_new = y + dy *dt 
    theta_new = theta + Wz * dt

    return (x_new,y_new,theta_new)

RASPBERRY_IP = '192.168.1.167'  # ← Remplace avec l'adresse IP réelle de la Raspberry
PORT = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((RASPBERRY_IP, PORT))

print("Connecté au serveur Raspberry.")
first_timestamp = False
x,y,theta = 0.0,0.0,0.0

x_table = []
y_table = []
theta_table = []



try:
    while True:
        data = client_socket.recv(1024).decode().strip()
        if data:
            now_t, v1, v2, v3 = map(float, data.split(","))
            if not first_timestamp : 
                prec_t = now_t
                first_timestamp = True
                
            delta_t = now_t - prec_t
            prec_t = now_t

            vx,vy,wz = Kinematic_direct(v1,v2,v3)
            x,y,theta = update_odometry(x,y,theta,vx,vy,wz,delta_t)
            x_table.append(x)
            y_table.append(y)
            theta_table.append(theta)

            print(f"Réception → V1={v1}, V2={v2}, V3={v3}")
except KeyboardInterrupt:
    print("Déconnexion...")
    client_socket.close()

plot_robot_trajectory(x_table,y_table,theta_table)
