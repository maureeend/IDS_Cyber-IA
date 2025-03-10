import pandas as pd
import numpy as np
import os

#Définir les chemins des fichiers
data_dir=os.path.join(os.path.dirname(__file__), "../data")
raw_data_path= os.path.join(data_dir, "raw_data.csv")
processed_data_path=os.path.join(data_dir, "processed_data.csv")

# Vérifier si le fichier raw_data.csv existe
if not os.path.exists(raw_data_path):
    raise FileNotFoundError(f"Le fichier '{raw_data_path}' est introuvable. Lancer 'capture.py' d'abord.")

# Charger les données
df=pd.read_csv(raw_data_path)

#Vérifier que le fichier n'est pas vide
if df.empty:
    raise ValueError("Le fichier de données est vide. Vérifier la capture.")

print("Aperçu des données brutes :")
print(df.head())

# Nettoyage des données
# Remplacement des valeurs NaN par -1
df.fillna(-1, inplace=True)

#Encodage des adresses IP en entiers
def ip_to_int(ip):
    """Convertir une adresse IP en entier."""
    try:
        return int("".join(f"{int(x):03d}" for x in ip.split(".")))
    except:
        return -1  # Valeur IPs invalides

df["src_ip"]=df["src_ip"].apply(ip_to_int)
df["dst_ip"] =df["dst_ip"].apply(ip_to_int)

#Normalisation des valeurs numériques
if "length" in df.columns:
    df["length"]=(df["length"] - df["length"].min()) / (df["length"].max() - df["length"].min())

#Encodage des protocoles
# Mapping des protocoles connus : TCP=6, UDP=17, ICMP=1 (autres=-1)
protocol_map = {1: "ICMP", 6: "TCP", 17: "UDP"}
df["protocol_name"] = df["protocol"].map(protocol_map).fillna("OTHER")

#Sauvegarde des données prétraitées
df.to_csv(processed_data_path, index=False)

print("\nDonnées prétraitées sauvegardées dans 'data/processed_data.csv'")
print(df.head())  #Affichage des premières lignes après prétraitement