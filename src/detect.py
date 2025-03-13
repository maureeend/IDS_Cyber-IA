""" Capture un paquet réseau et le classe avec le modèle dans trained_model.pkl """

""" Capture un paquet réseau et le classe avec le modèle dans trained_model.pkl """

import joblib
import pandas as pd
import scapy.all as scapy

# Charger le modèle
model = joblib.load("models/trained_model.pkl")

# Définir les features utilisées dans l'entraînement
columns_to_keep = [
    "Destination Port", "Flow Duration", "Total Fwd Packets", "Total Backward Packets",
    "Total Length of Fwd Packets", "Total Length of Bwd Packets",
    "Fwd Packet Length Mean", "Bwd Packet Length Mean",
    "Flow IAT Mean", "Fwd IAT Mean", "Bwd IAT Mean",
    "Fwd Packets/s", "Bwd Packets/s",
    "SYN Flag Count", "ACK Flag Count", "PSH Flag Count", "FINFlag Count",
    "Packet Length Mean", "Min Packet Length", "Max Packet Length",
    "Flow Bytes/s", "Flow Packets/s", "Down/Up Ratio"
]

def extract_features(packet):
    """ Extrait les features d'un paquet réseau pour la détection d'intrusion """

    try:
        features = {
            "Destination Port": packet.dport if packet.haslayer(scapy.TCP) or packet.haslayer(scapy.UDP) else 0,
            "Flow Duration": packet.time,
            "Total Fwd Packets": 1 if packet.haslayer(scapy.IP) else 0,
            "Total Backward Packets": 1 if packet.haslayer(scapy.TCP) else 0,
            "Total Length of Fwd Packets": len(packet),
            "Total Length of Bwd Packets": len(packet),
            "Fwd Packet Length Mean": len(packet),
            "Bwd Packet Length Mean": len(packet),
            "Flow IAT Mean": packet.time if packet.time else 0,
            "Fwd IAT Mean": packet.time if packet.time else 0,
            "Bwd IAT Mean": packet.time if packet.time else 0,
            "Fwd Packets/s": 1 / (packet.time if packet.time > 0 else 1),
            "Bwd Packets/s": 1 / (packet.time if packet.time > 0 else 1),
            "SYN Flag Count": 1 if packet.haslayer(scapy.TCP) and packet[scapy.TCP].flags & 0x02 else 0,
            "ACK Flag Count": 1 if packet.haslayer(scapy.TCP) and packet[scapy.TCP].flags & 0x10 else 0,
            "PSH Flag Count": 1 if packet.haslayer(scapy.TCP) and packet[scapy.TCP].flags & 0x08 else 0,
            "FINFlag Count": 1 if packet.haslayer(scapy.TCP) and packet[scapy.TCP].flags & 0x01 else 0,
            "Packet Length Mean": len(packet),
            "Min Packet Length": len(packet),
            "Max Packet Length": len(packet),
            "Flow Bytes/s": len(packet) / (packet.time if packet.time > 0 else 1),
            "Flow Packets/s": 1 / (packet.time if packet.time > 0 else 1),
            "Down/Up Ratio": 1
        }

        return pd.DataFrame([features])
    
    except Exception as e:
        print(f"Erreur lors de l'extraction des features : {e}")
        return None

def packet_callback(packet):
    """ Analyse un paquet réseau et détecte une intrusion """

    df_packet = extract_features(packet)

    if df_packet is not None:
        # Colonne même que celle de la dataset ?
        df_packet = df_packet.reindex(columns=columns_to_keep, fill_value=0)

        # Prédire intrusion
        proba = model.predict_proba(df_packet)[:, 1][0] 
        threshold = 0.5

        if proba >= threshold:
            print(f"ALERTE : Intrusion avec Score: {proba:.2f}) - {packet.summary()}")
