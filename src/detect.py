import pandas as pd
import joblib
import os

# Chemin
data_dir = os.path.join(os.path.dirname(__file__), "../data")
processed_data_path = os.path.join(data_dir, "processed_data.csv")
model_path = os.path.join(os.path.dirname(__file__), "../models/trained_model.pkl")

# Chargement du modèle
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Le modèle '{model_path}' est introuvable. Lancez 'train_model.py' d'abord.")

model = joblib.load(model_path)
print(f"\nModèle chargé depuis : {model_path}")

# Chargement des données
if not os.path.exists(processed_data_path):
    raise FileNotFoundError(f"Le fichier '{processed_data_path}' est introuvable. Lancez 'preprocess.py' d'abord.")

df = pd.read_csv(processed_data_path)

# Prédiction sur les données
predictions = model.predict(df)

# Résumé des résultats
df["Prediction"] = predictions
intrusions = (df["Prediction"] == 1).sum()
normaux = (df["Prediction"] == 0).sum()

print("\nRésumé de la détection :")
print(f"   - Trafic normal : {normaux}")
print(f"   - Intrusions détectées : {intrusions}")

# Sauvegarde des résultats
results_path = os.path.join(os.path.dirname(__file__), "../logs/detection_results.csv")
df.to_csv(results_path, index=False)
df.to_csv(processed_data_path, index=False)  # processed_data.csv
print(f"\nPrédictions ajoutées et sauvegardées dans : {processed_data_path}")
print(f"\nRésultats enregistrés dans : {results_path}")
