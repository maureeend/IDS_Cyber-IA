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
    title = '''
 _   _                      _____ _     _      _     _ 
| \ | |                    /  ___| |   (_)    | |   | |
|  \| | ___ _   _ _ __ ___ \ `--.| |__  _  ___| | __| |
| . ` |/ _ \ | | | '__/ _ \ `--. \ '_ \| |/ _ \ |/ _` |
| |\  |  __/ |_| | | | (_) /\__/ / | | | |  __/ | (_| |
\_| \_/\___|\__,_|_|  \___/\____/|_| |_|_|\___|_|\__,_|
                                                       
                                                       
'''

    print(title)
    print("\nBienvenue sur NeuroShield.")
    print("Ce projet a été réalisé dans le cadre d'un cours et a pour but éducatif.")
    print("Il vise à illustrer les concepts de cybersécurité et d'intelligence artificielle appliqués à la détection d'intrusions.")
    print("\n===  DÉMARRAGE DE LA SURVEILLANCE EN TEMPS RÉEL  ===")

    
    # 1. Capture du trafic réseau
    run_script(capture_script)
    
    # 2. Prétraitement des données
    run_script(preprocess_script)

    # 3. Détection des intrusions avec le modèle IA
    run_script(detect_script)

    print("\n Analyse terminée !")
