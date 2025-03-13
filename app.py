''' Fichier principal '''

import os
import subprocess
import sys


capture_script = "src/capture.py"
preprocess_script = "src/preprocess.py"
detect_script = "src/detect.py"

def run_script(script_path):

    if os.path.exists(script_path):
        print(f" Exécution de {script_path}...\n")
        subprocess.run([sys.executable, script_path], check=True)
    else:
        print(f"Error : {script_path} introuvable.")

if __name__ == "__main__":
    print("=== DÉMARRAGE DU SYSTÈME DE DÉTECTION D'INTRUSION ===")
    
    # 1. Capture du trafic réseau
    run_script(capture_script)
    
    # 2. Prétraitement des données
    run_script(preprocess_script)

    # 3. Détection des intrusions avec le modèle IA
    run_script(detect_script)

    print("\n Analyse terminée !")
