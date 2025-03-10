from scapy.all import sniff, conf
import pandas as pd
import os

# Trouver automatiquement la meilleure interface réseau
INTERFACE= conf.iface
print(f"Interface détectée : {INTERFACE}")

# Création du dossier data s'il n'existe pas
data_dir=os.path.join(os.path.dirname(__file__), "../data")
os.makedirs(data_dir, exist_ok=True)

#Stocker les paquets capturés dans cette liste
captured_packets= []

def process_packet(packet):
    """Extraire les informations utiles du paquet."""
    if packet.haslayer("IP"): # Vérifier si le paquet contient une couche IP
        packet_info = {
            "src_ip": packet["IP"].src,
            "dst_ip": packet["IP"].dst,
            "protocol": packet["IP"].proto,
            "length": len(packet),
        }
        if packet.haslayer("TCP") or packet.haslayer("UDP"):
            packet_info["src_port"]= packet.sport
            packet_info["dst_port"]=packet.dport
        else:
            packet_info["src_port"] =None
            packet_info["dst_port"]= None

        print("Paquet capturé :", packet_info) # Vérifier

        captured_packets.append(packet_info)

#Lancer la capture 
print(f"Capture en cours sur {INTERFACE}...")
try:
    sniff(iface=INTERFACE, prn=process_packet, store=False, count=50)  # Capture 50 paquets
except KeyboardInterrupt:
    print("\n Capture arrêtée.")

# Convertir et sauvegarder
df=pd.DataFrame(captured_packets)

if not df.empty:
    df.to_csv(os.path.join(data_dir, "raw_data.csv"), index=False)
    print("Données sauvegardées dans 'data/raw_data.csv'")
else:
    print("Aucune donnée capturée. Vérifier l'interface réseau.")
