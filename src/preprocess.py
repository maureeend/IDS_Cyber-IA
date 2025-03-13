import pandas as pd
import numpy as np
import os

# Définir les chemins des fichiers
data_dir = os.path.join(os.path.dirname(__file__), "../data")
raw_data_path = os.path.join(data_dir, "raw_data.csv")
processed_data_path = os.path.join(data_dir, "processed_data.csv")

# Vérifier si le fichier raw_data.csv existe
if not os.path.exists(raw_data_path):
    raise FileNotFoundError(f"Le fichier '{raw_data_path}' est introuvable. Lancez 'capture.py' d'abord.")

# Charger les données
df = pd.read_csv(raw_data_path)

# Vérifier que le fichier n'est pas vide
if df.empty:
    raise ValueError("Le fichier de données est vide. Vérifiez la capture.")

print("Aperçu des données brutes :")
print(df.head())

# ======== Nettoyage des Données ======== #

# Remplacement des valeurs nulles par la médiane (évite les -1 inutiles)
df.fillna(df.median(numeric_only=True), inplace=True)

# Encodage des adresses IP en entiers
def ip_to_int(ip):
    """Convertit une adresse IP en entier."""
    try:
        return int("".join(f"{int(x):03d}" for x in ip.split(".")))
    except:
        return -1  # Valeur pour les IPs invalides ou vides

df["src_ip"] = df["src_ip"].astype(str).apply(ip_to_int)
df["dst_ip"] = df["dst_ip"].astype(str).apply(ip_to_int)

# Filtrer les flux avec un Flow Duration trop faible (évite les erreurs)
df = df[df["Flow Duration"] > 0.001]  

# Normalisation des valeurs numériques (évite les biais)
columns_to_normalize = ["Flow Duration", "Total Fwd Packets", "Total Backward Packets",
                        "Total Length of Fwd Packets", "Total Length of Bwd Packets",
                        "Min Packet Length", "Max Packet Length", "Flow Bytes/s",
                        "Flow Packets/s", "Fwd Packets/s", "Bwd Packets/s"]

for col in columns_to_normalize:
    if col in df.columns:
        df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())

# Remplacement des valeurs aberrantes (Flow Bytes/s, Packets/s)
for col in ["Flow Bytes/s", "Flow Packets/s", "Fwd Packets/s", "Bwd Packets/s", "Down/Up Ratio"]:
    if col in df.columns:
        df[col] = df[col].replace(0, df[col].median())

# Encodage des protocoles (TCP, UDP, ICMP)
protocol_map = {1: "ICMP", 6: "TCP", 17: "UDP"}
df["protocol_name"] = df["protocol"].map(protocol_map).fillna("OTHER")

# ======== Sauvegarde des Données ======== #
df.to_csv(processed_data_path, index=False)

print("\nDonnées prétraitées sauvegardées dans 'data/processed_data.csv'")
print(df.head())  # Affichage des premières lignes après prétraitement