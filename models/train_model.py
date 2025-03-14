import kagglehub
import pandas as pd
import numpy as np
import os
import glob
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

# Dataset CIC-IDS 2017 depuis Kaggle
dataset_path = kagglehub.dataset_download("chethuhn/network-intrusion-dataset")
csv_files = glob.glob(os.path.join(dataset_path, "*.csv"))
if not csv_files:
    raise FileNotFoundError("Aucun fichier CSV trouvé")

# Lire et fusion de des fichiers CVS
df_list = [pd.read_csv(file, low_memory=False) for file in csv_files]
df = pd.concat(df_list, ignore_index=True)

print("Dataset chargé")
print("Colonnes:", df.columns.tolist())

# Nettoyage des noms de colonnes (suppression des espaces)
df.columns = df.columns.str.strip()
df.replace([np.inf, -np.inf], np.nan, inplace=True)
print("Nettoyage Ok:")
df = df.sample(frac=0.5, random_state=42)
print("good 1.2")
print("Nombre total de NaN AVANT remplissage :", df.isna().sum().sum())
print("Colonnes des NaN  :")
print(df.isna().sum()[df.isna().sum() > 0])
df.dropna(axis=1, thresh=int(0.1 * len(df)), inplace=True)  # Supprime les colonnes avec plus de 90% de NaN
print("Suppression des colonnes avec trop de NaN")
for col in df.select_dtypes(include=[np.number]).columns:
    df[col].fillna(df[col].mean(), inplace=True)

print("Remplacement des NaN terminé !")
print("good 1.3")


columns_to_keep = [
    "Destination Port", "Flow Duration", "Total Fwd Packets", "Total Backward Packets",
    "Total Length of Fwd Packets", "Total Length of Bwd Packets",
    "Fwd Packet Length Mean", "Bwd Packet Length Mean",
    "Flow IAT Mean", "Fwd IAT Mean", "Bwd IAT Mean",
    "Fwd Packets/s", "Bwd Packets/s",
    "SYN Flag Count", "ACK Flag Count", "PSH Flag Count", "FIN Flag Count",
    "Packet Length Mean", "Min Packet Length", "Max Packet Length",
    "Flow Bytes/s", "Flow Packets/s", "Down/Up Ratio",
    "Label"
]


columns_to_keep = [col for col in columns_to_keep if col in df.columns]
print("Colonnes sélectionnées :", columns_to_keep)


df = df[columns_to_keep]
print("good 1") 

df["Label"] = df["Label"].apply(lambda x: 0 if x.strip() == "BENIGN" else 1)
print("good 2")

df.fillna(df.mean(), inplace=True)
print("good 3")

X = df.drop(columns=["Label"])
y = df["Label"]
print("good 1")

# train (80%) et test (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print("good 2")

# modèle Random Forest
rf_model = RandomForestClassifier(n_estimators=300, random_state=42)
rf_model.fit(X_train, y_train)
print("Entraînement terminé !")

# Prédictionévaluation du modèle
y_pred = rf_model.predict(X_test)
print("Test terminé !")


print("\nAccuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Matrice de confusion
plt.figure(figsize=(6, 4))
sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt="d", cmap="Blues", xticklabels=["Normal", "Attack"], yticklabels=["Normal", "Attack"])
plt.xlabel("Prédit")
plt.ylabel("Réel")
plt.title("Matrice de confusion Random Forest")
plt.show()

# Sauvegarde du modèle entraîné
model_path = "models/trained_model.pkl"
joblib.dump(rf_model, model_path)
print(f"Modèle sauvegardé : {model_path}")
