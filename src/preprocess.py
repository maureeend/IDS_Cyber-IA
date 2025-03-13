import pandas as pd
import numpy as np
import os

data_dir = os.path.join(os.path.dirname(_file_), "../data")
raw_data_path = os.path.join(data_dir, "raw_data.csv")
processed_data_path = os.path.join(data_dir, "processed_data.csv")

if not os.path.exists(raw_data_path):
    raise FileNotFoundError(f"Le fichier '{raw_data_path}' est introuvable. Lancez 'capture.py' d'abord.")

df = pd.read_csv(raw_data_path)

print("\nColonnes disponibles dans raw_data.csv :", df.columns.tolist())

if df.empty:
    raise ValueError("Le fichier de données est vide. Vérifiez la capture.")

print("Aperçu des données brutes :")
print(df.head())

expected_features = [
    "Destination Port", "Flow Duration", "Total Fwd Packets", "Total Backward Packets",
    "Total Length of Fwd Packets", "Total Length of Bwd Packets",
    "Fwd Packet Length Mean", "Bwd Packet Length Mean",
    "Flow IAT Mean", "Fwd IAT Mean", "Bwd IAT Mean",
    "Fwd Packets/s", "Bwd Packets/s",
    "SYN Flag Count", "ACK Flag Count", "PSH Flag Count", "Packet Length Mean",
    "Min Packet Length", "Max Packet Length",
    "Flow Bytes/s", "Flow Packets/s", "Down/Up Ratio"
]

columns_to_drop = ["src_ip", "dst_ip", "Flow Start", "protocol", "Previous Timestamp", "protocol_name"]
df.drop(columns=[col for col in columns_to_drop if col in df.columns], inplace=True)

for col in expected_features:
    if col not in df.columns:
        print(f"Colonne manquante ajoutée : {col}")
        df[col] = 0

df = df[expected_features]

for col in df.columns:
    if df[col].max() > df[col].min():
        df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())

df.to_csv(processed_data_path, index=False)

print("\nDonnées prétraitées alignées avec le modèle et sauvegardées dans 'data/processed_data.csv' !")
print(df.head())