from scapy.all import sniff, conf, IP, TCP, UDP
import pandas as pd
import os
import time

# Détection automatique de l'interface réseau
INTERFACE = conf.iface
print(f"Interface détectée : {INTERFACE}")

# Création du dossier data s'il n'existe pas
data_dir = os.path.join(os.path.dirname(__file__), "../data")
os.makedirs(data_dir, exist_ok=True)

# Liste des flux capturés
captured_packets = []
flow_tracker = {}  # Suivi des flux réseau

def process_packet(packet):
    """Capture les informations réseau et met à jour les statistiques des flux."""
    if not packet.haslayer(IP):  # Vérifier que le paquet contient une couche IP
        return
    
    timestamp = time.time()  # Timestamp actuel
    src_ip = packet[IP].src
    dst_ip = packet[IP].dst
    protocol = packet[IP].proto
    length = len(packet)

    # Identification du port source et destination si TCP/UDP
    src_port, dst_port = (packet.sport, packet.dport) if packet.haslayer(TCP) or packet.haslayer(UDP) else (0, 0)

    # Extraction des flags TCP
    syn_flag = ack_flag = psh_flag = fin_flag = rst_flag = 0
    if packet.haslayer(TCP):
        syn_flag = int(packet[TCP].flags & 0x02 != 0)  # SYN
        ack_flag = int(packet[TCP].flags & 0x10 != 0)  # ACK
        psh_flag = int(packet[TCP].flags & 0x08 != 0)  # PSH
        fin_flag = int(packet[TCP].flags & 0x01 != 0)  # FIN
        rst_flag = int(packet[TCP].flags & 0x04 != 0)  # RST

    # Création d'une clé unique pour le flux
    flow_key = (src_ip, dst_ip, protocol, src_port, dst_port)
    reverse_flow_key = (dst_ip, src_ip, protocol, dst_port, src_port)

    # Vérifier si le flux existe déjà
    if flow_key in flow_tracker:
        flow = flow_tracker[flow_key]
        direction = "Fwd"
    elif reverse_flow_key in flow_tracker:
        flow = flow_tracker[reverse_flow_key]
        direction = "Bwd"
    else:
        # Nouvelle entrée pour un flux
        flow = {
            "Flow Start": timestamp,
            "Previous Timestamp": timestamp,
            "Flow Duration": 0,
            "Total Fwd Packets": 0,
            "Total Backward Packets": 0,
            "Total Length of Fwd Packets": 0,
            "Total Length of Bwd Packets": 0,
            "Min Packet Length": length,
            "Max Packet Length": length,
            "Flow IAT Sum": 0,  # Somme des IAT pour le calcul final
            "Fwd IAT Sum": 0,
            "Bwd IAT Sum": 0,
            "Fwd IAT Count": 0,
            "Bwd IAT Count": 0,
            "SYN Flag Count": 0,
            "ACK Flag Count": 0,
            "PSH Flag Count": 0,
            "FIN Flag Count": 0,
            "RST Flag Count": 0,
            "Flow Bytes/s": 0,
            "Flow Packets/s": 0,
            "Down/Up Ratio": 0,
            "Fwd Packets/s": 0,
            "Bwd Packets/s": 0
        }
        flow_tracker[flow_key] = flow
        direction = "Fwd"

    # Calcul des Inter-Arrival Times (IAT)
    inter_arrival_time = timestamp - flow["Previous Timestamp"]
    flow["Previous Timestamp"] = timestamp
    flow["Flow Duration"] = max(timestamp - flow["Flow Start"], 0.0001)

    # Mise à jour des statistiques
    if direction == "Fwd":
        flow["Total Fwd Packets"] += 1
        flow["Total Length of Fwd Packets"] += length
        flow["Fwd IAT Sum"] += inter_arrival_time
        flow["Fwd IAT Count"] += 1
    else:
        flow["Total Backward Packets"] += 1
        flow["Total Length of Bwd Packets"] += length
        flow["Bwd IAT Sum"] += inter_arrival_time
        flow["Bwd IAT Count"] += 1

    # Mise à jour des valeurs min/max de la taille des paquets
    flow["Min Packet Length"] = min(flow["Min Packet Length"], length)
    flow["Max Packet Length"] = max(flow["Max Packet Length"], length)

    # Mise à jour des flags TCP
    flow["SYN Flag Count"] += syn_flag
    flow["ACK Flag Count"] += ack_flag
    flow["PSH Flag Count"] += psh_flag
    flow["FIN Flag Count"] += fin_flag
    flow["RST Flag Count"] += rst_flag

    # Calcul des moyennes des IAT
    flow["Flow IAT Mean"] = flow["Flow IAT Sum"] / max(flow["Total Fwd Packets"] + flow["Total Backward Packets"], 1)
    flow["Fwd IAT Mean"] = flow["Fwd IAT Sum"] / max(flow["Fwd IAT Count"], 1)
    flow["Bwd IAT Mean"] = flow["Bwd IAT Sum"] / max(flow["Bwd IAT Count"], 1)

    # Calcul du débit et du nombre de paquets par seconde
    if flow["Flow Duration"] > 0:
        flow["Flow Bytes/s"] = (flow["Total Length of Fwd Packets"] + flow["Total Length of Bwd Packets"]) / flow["Flow Duration"]
        flow["Flow Packets/s"] = (flow["Total Fwd Packets"] + flow["Total Backward Packets"]) / flow["Flow Duration"]
        flow["Fwd Packets/s"] = flow["Total Fwd Packets"] / flow["Flow Duration"]
        flow["Bwd Packets/s"] = flow["Total Backward Packets"] / flow["Flow Duration"]

    # Calcul du Down/Up Ratio
    if flow["Total Fwd Packets"] > 0:
        flow["Down/Up Ratio"] = flow["Total Backward Packets"] / flow["Total Fwd Packets"]

    # Ajout du paquet capturé
    captured_packets.append(flow.copy())

# Capture en cours
sniff(iface=INTERFACE, prn=process_packet, store=False, count=50)

# Sauvegarde
df = pd.DataFrame(captured_packets)
df.to_csv(os.path.join(data_dir, "raw_data.csv"), index=False)
print("Données sauvegardées dans 'data/raw_data.csv'")