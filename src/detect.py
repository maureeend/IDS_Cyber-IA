import joblib
import pandas as pd
import os
import logging

# Définition des chemins
model_path = "models/trained_model.pkl"
data_path = "data/processed_data.csv"
log_path = "logs/detection.log"

# Configuration du logging
logging.basicConfig(filename=log_path, level=logging.INFO, format="%(asctime)s - %(message)s")

# Vérification des fichiers
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Modèle non trouvé : {model_path}. Entraînez-le avant d'exécuter detect.py.")

if not os.path.exists(data_path):
    raise FileNotFoundError(f"Données prétraitées introuvables : {data_path}. Exécutez preprocess.py.")

# Charger le modèle entraîné
model = joblib.load(model_path)
print(f"Modèle chargé depuis : {model_path}")


# Charger les données prétraitées
df = pd.read_csv(data_path)

if df.empty:
    raise ValueError("Le fichier de données prétraitées est vide.")

# Supprimer la colonne Label si elle est présente
if "Label" in df.columns:
    df.drop(columns=["Label"], inplace=True)

# Prédire les intrusions
predictions = model.predict(df)
df["Prediction"] = predictions

# Enregistrer les résultats
df.to_csv("logs/detection_results.csv", index=False)
print(" Résultats enregistrés dans logs/detection_results.csv")

# Affichage des statistiques
num_attacks = df["Prediction"].sum()
num_normal = len(df) - num_attacks

print(f"Résumé de la détection :")
print(f"   - Trafic normal : {num_normal}")
print(f"   - Intrusions détectées : {num_attacks}")

# Logger les intrusions détectées
if num_attacks > 0:
    logging.info(f"{num_attacks} intrusion(s) détectée(s) ! Vérifiez logs/detection_results.csv.")
    print("\n [ALERTE] Des intrusions ont été détectées ! ")

print("\nDétection terminée.")
