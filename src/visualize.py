import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Définition des chemins de fichiers
data_dir = os.path.join(os.path.dirname(__file__), "../data")
processed_data_path = os.path.join(data_dir, "processed_data.csv")

# Vérification de l'existence du fichier
if not os.path.exists(processed_data_path):
    raise FileNotFoundError(f"Le fichier '{processed_data_path}' est introuvable. Lancez 'preprocess.py' d'abord.")

# Chargement des données
df = pd.read_csv(processed_data_path)

# Vérification si la colonne 'Prediction' existe
if "Prediction" not in df.columns:
    raise ValueError("Le fichier ne contient pas la colonne 'Prediction'. Assurez-vous d'avoir exécuté detect.py")

# Affichage du nombre d'intrusions détectées
plt.figure(figsize=(6,4))
sns.countplot(x=df["Prediction"], palette="coolwarm")
plt.xticks([0, 1], ["Normal", "Intrusion"])
plt.xlabel("Type de trafic")
plt.ylabel("Nombre de flux détectés")
plt.title("Répartition des flux normaux et malveillants")
plt.show()

# Visualisation de l'augmentation des paquets SYN
df["SYN Flag Count"].hist(bins=50, color='red', alpha=0.7)
plt.xlabel("Nombre de paquets SYN par flux")
plt.ylabel("Nombre d'observations")
plt.title("Distribution des paquets SYN détectés")
plt.show()

# Courbe du nombre d'intrusions au fil du temps
if "Flow Start" in df.columns:
    df["Flow Start"] = pd.to_datetime(df["Flow Start"], unit='s')
    df.set_index("Flow Start", inplace=True)
    df["Prediction"].resample("1S").sum().plot(figsize=(10,5), marker="o", linestyle="-")
    plt.xlabel("Temps")
    plt.ylabel("Nombre d'intrusions détectées")
    plt.title("Évolution des intrusions détectées dans le temps")
    plt.show()
