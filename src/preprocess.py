import pandas as pd
import numpy as np
import os

# Définition des chemins de fichiers
data_dir = os.path.join(os.path.dirname(__file__), "../data")
raw_data_path = os.path.join(data_dir, "raw_data.csv")
processed_data_path = os.path.join(data_dir, "processed_data.csv")

# Vérification de l'existence du fichier brut
if not os.path.exists(raw_data_path):
    raise FileNotFoundError(f"Le fichier '{raw_data_path}' est introuvable. Lancez 'capture.py' d'abord.")

# Chargement des données
df = pd.read_csv(raw_data_path)

print("\nColonnes disponibles dans raw_data.csv :", df.columns.tolist())

# Vérification si le fichier est vide
if df.empty:
    raise ValueError("Le fichier de données est vide. Vérifiez la capture.")

print("\nAperçu des premières lignes :")
print(df.head())

# Liste des features attendues (Doit correspondre à train_model.py)
expected_features = [
    "Destination Port", "Flow Duration", "Total Fwd Packets", "Total Backward Packets",
    "Total Length of Fwd Packets", "Total Length of Bwd Packets",
    "Fwd Packet Length Mean", "Bwd Packet Length Mean",
    "Flow IAT Mean", "Fwd IAT Mean", "Bwd IAT Mean",
    "Fwd Packets/s", "Bwd Packets/s",
    "SYN Flag Count", "ACK Flag Count", "PSH Flag Count", "FIN Flag Count",
    "Packet Length Mean", "Min Packet Length", "Max Packet Length",
    "Flow Bytes/s", "Flow Packets/s", "Down/Up Ratio"
]

# Suppression des colonnes inutiles
columns_to_drop = ["src_ip", "dst_ip", "Flow Start", "Previous Timestamp", "protocol", "protocol_name"]
df.drop(columns=[col for col in columns_to_drop if col in df.columns], inplace=True, errors='ignore')

# Ajout des colonnes manquantes (remplies avec 0)
for col in expected_features:
    if col not in df.columns:
        print(f"Colonne manquante ajoutée : {col}")
        df[col] = 0

# Réorganisation des colonnes pour correspondre au modèle
df = df[expected_features]

# Normalisation des données (Min-Max Scaling)
for col in df.columns:
    if df[col].dtype in [np.float64, np.int64]:  # Vérifier que la colonne est numérique
        min_val, max_val = df[col].min(), df[col].max()
        if min_val != max_val:
            df[col] = (df[col] - min_val) / (max_val - min_val)

# Sauvegarde des données prétraitées
df.to_csv(processed_data_path, index=False)

print("\nDonnées prétraitées alignées avec le modèle et sauvegardées dans 'data/processed_data.csv' !")
print(df.head())
