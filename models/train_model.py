import pandas as pd
import numpy as np
import os
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Définition des chemins
data_dir = os.path.join(os.path.dirname(__file__), "../data")
dataset_path = os.path.join(data_dir, "processed_data.csv")
model_path = os.path.join(os.path.dirname(__file__), "trained_model.pkl")

# Chargement du dataset
if not os.path.exists(dataset_path):
    raise FileNotFoundError(f"Le fichier '{dataset_path}' est introuvable. Lancez 'preprocess.py' d'abord.")

df = pd.read_csv(dataset_path)

# Sélection des colonnes d'entraînement (alignées avec preprocess.py)
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

# Création des labels (0 = normal, 1 = attaque)
df["Label"] = np.random.choice([0, 1], size=len(df))  # Remplace par les vrais labels si disponibles

# Séparation des données
X = df[expected_features]
y = df["Label"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entraînement du modèle
model = RandomForestClassifier(n_estimators=300, random_state=42)
model.fit(X_train, y_train)

# Évaluation du modèle
y_pred = model.predict(X_test)
print("\nAccuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Matrice de confusion
plt.figure(figsize=(6, 4))
sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt="d", cmap="Blues", xticklabels=["Normal", "Attack"], yticklabels=["Normal", "Attack"])
plt.xlabel("Prédit")
plt.ylabel("Réel")
plt.title("Matrice de confusion Random Forest")
plt.show()

# Sauvegarde du modèle
joblib.dump(model, model_path)
print(f"\nModèle sauvegardé dans : {model_path}")
