# AI-Based Intrusion Detection System (IDS)

**Ce projet a été réalisé dans le cadre d'un cours et a pour but éducatif. Il vise à illustrer les concepts de cybersécurité et d'intelligence artificielle appliqués à la détection d'intrusions.**

## Description
La cybersécurité est un enjeu majeur dans les systèmes informatiques modernes. Ce projet vise à concevoir un système de détection d'intrusions (IDS) en exploitant des techniques d’intelligence artificielle et de machine learning.  

L'objectif principal est d'analyser le trafic réseau, d’identifier des comportements suspects et de générer des alertes en temps réel en cas d’intrusion.  

🔹 Capture du trafic réseau via Scapy  
🔹 Prétraitement des données pour les rendre exploitables par l’IA  
🔹 Détection des intrusions grâce à un modèle IA  
🔹 Visualisation et alertes en temps réel 

## Prérequis
Avant d’exécuter ce projet, assurez-vous d’avoir installé les outils suivants :  
✔ Python (>=3.8)  

✔ Git

✔ Un environnement virtuel Python (recommandé)

✔ Bibliothèques nécessaires (voir `requirements.txt`)

✔ Modèle à télécharger sur HuggingFace (voir lien plus bas)

## Installation

## Utilisation
1️. Capture du trafic réseau
Le script capture.py permet d'enregistrer les paquets réseau dans un fichier exploitable.
Commande : python src/capture.py

📍 Résultat attendu : Création du fichier data/raw_data.csv contenant les paquets capturés.

2️. Prétraitement des données
Le script preprocess.py nettoie et normalise les données pour les rendre exploitables par l’IA.
Commande : python src/preprocess.py

📍 Résultat attendu : Génération de data/processed_data.csv contenant les données transformées.



## Architecture du projet


## Lien
Modèle Sur HuggingFace: https://huggingface.co/Maureeendr/CyberIA-model-IDS/tree/main

Une vidéo explicative du projet est disponible ici : https://youtu.be/hH2h3r6dQXk


## Auteurs et collaboration
Reizène – Capture du trafic et prétraitement des données

Maureen – Développement du modèle IA et visualisation

**Projet réalisé dans le cadre d’un cours académique en cybersécurité et intelligence artificielle.**
