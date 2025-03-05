'''
    Code NON OFFICIEL
    Prétraitement des données
    Création de données factices en attendant du code IDS
'''

import pandas as pd
import numpy as np

# Nombre de ligne dataset
N = 1000

# Générateur de trame résea aléatoire
data = {
    "length": np.random.randint(40, 1500, N),
    "protocol": np.random.choice([1, 6, 17], N),  # ICMP, TCP, UDP
    "src_port": np.random.randint(1024, 65535, N),
    "dst_port": np.random.randint(1, 65535, N),
    "label": np.random.choice([0, 1], N, p=[0.85, 0.15])  # 15% d’intrusions
}

df = pd.DataFrame(data)

df.to_csv("data\processed_data.csv", index=False)

print("Données générées")