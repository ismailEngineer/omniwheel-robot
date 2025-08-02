import matplotlib.pyplot as plt

# Chemin du fichier
nom_fichier = "donnees_vitesse.txt"

# Listes pour stocker les données
timestamps_raw = []
v1_list = []
v2_list = []
v3_list = []

# Lecture du fichier
with open(nom_fichier, "r") as f:
    for ligne in f:
        try:
            t, v1, v2, v3 = map(float, ligne.strip().split(","))
            timestamps_raw.append(t)  # Temps relatif
            v1_list.append(v1)
            v2_list.append(v2)
            v3_list.append(v3)
        except ValueError:
            continue  # Ignore les lignes corrompues


# Recalage du temps : temps relatif (en secondes)
if timestamps_raw:
    t0 = timestamps_raw[0]
    timestamps = [t - t0 for t in timestamps_raw]
else:
    timestamps = []

# Fonction pour créer un graphique
def plot_single_curve(t, v, label, color):
    plt.figure(figsize=(8, 4))
    plt.plot(t, v, label=label, color=color)
    plt.xlabel("Temps (s)")
    plt.ylabel("Vitesse")
    plt.title(f"Évolution de la {label}")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


# Tracer chaque vitesse dans un graphe séparé
plot_single_curve(timestamps, v1_list, "vitesse moteur 1", "red")
plot_single_curve(timestamps, v2_list, "vitesse moteur 2", "green")
plot_single_curve(timestamps, v3_list, "vitesse moteur 3", "blue")
