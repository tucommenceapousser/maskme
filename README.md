# 🛠️ **Anonymous Face Masking Tool by TRHACKNON** 🛠️

Un outil simple mais puissant permettant d'ajouter un masque anonyme à des visages sur des images. Ce projet utilise **Flask** pour l'interface web, **OpenCV** pour le traitement d'image, et **MediaPipe** pour la détection et l'analyse des visages.

## 🚀 **Fonctionnalités**

- Téléchargez une photo.
- Appliquez un masque de style "anonymous" sur les visages détectés.
- Rotation et redimensionnement automatique du masque pour s'adapter à l'orientation et à la taille du visage.
- Visualisation du résultat avec un simple lien de téléchargement.

## 🚀 **Démo Déployée**

Découvrez la démo en ligne de l'application en cliquant sur le lien ci-dessous :

[**Voir la démo déployée**](https://maskme-trkn.replit.app/)

## 🛠️ **Prérequis**

Avant d'exécuter ce projet, assurez-vous d'avoir installé les dépendances nécessaires :

- Python 3.x
- pip (Python Package Installer)

## 📦 **Installation**

1. Clonez le dépôt sur votre machine :

   ```ruby
   git clone https://github.com/tucommenceapousser/maskme.git
   cd anonymous-mask-tool
   ```

2. Créez un environnement virtuel (optionnel mais recommandé) :

   ```ruby
   python3 -m venv venv
   source venv/bin/activate  # Pour Linux/Mac
   venv\Scripts\activate
   ```

3. Installez les dépendances :

   ```ruby
   pip install -r requirements.txt
   ```


🖥️ Démarrage du Serveur

1. Exécutez l'application Flask :

   ```ruby
   python app.py
   ```

2. Accédez à l'application via votre navigateur à l'adresse suivante :

http://127.0.0.1:8080


3. Téléchargez une image, et le masque sera ajouté automatiquement.



🎭 Comment ça marche

Le processus de l'ajout du masque sur le visage se déroule en trois étapes principales :

1. Détection du visage : Utilisation de MediaPipe pour localiser les visages dans l'image.


2. Calcul de la rotation : L'angle de rotation du visage est déterminé en utilisant les repères des yeux.


3. Application du masque : Le masque est redimensionné et tourné pour s'adapter au visage et est ensuite appliqué à l'image originale.



Le résultat final est une image avec le masque ajouté sur les visages détectés.

🔧 Technologies Utilisées

Flask : Framework web pour la création de l'interface.

OpenCV : Bibliothèque de traitement d'image pour le redimensionnement et la rotation des masques.

MediaPipe : Pour la détection des visages et le calcul de la rotation.

WTForms : Pour gérer les formulaires de téléchargement d'image.

Werkzeug : Pour sécuriser les fichiers téléchargés.


## 📁 **Structure des Dossiers**

   ```ruby
/anonymous-mask-tool
├── /static
│   ├── /uploads             # Dossier pour stocker les images téléchargées
│   └── /results             # Dossier pour stocker les résultats générés
├── /templates
│   ├── upload.html          # Formulaire de téléchargement d'image
│   └── result.html          # Page affichant le résultat après traitement
├── app.py                   # Script principal de l'application
├── requirements.txt         # Liste des dépendances
└── README.md
   ```

📌 **Remarques** :  
- **Werkzeug** est utilisé pour sécuriser les fichiers téléchargés dans l'application.


Le masque utilisé est une image PNG transparente (mask.png). Vous pouvez personnaliser ce masque en fonction de vos préférences.

Le serveur Flask est configuré pour exécuter l'application en mode debug=False pour la production. Vous pouvez changer ce paramètre à debug=True pour les tests en local.


🔒 Sécurité

Le projet utilise Flask-WTF pour gérer les formulaires, ce qui permet de valider les fichiers téléchargés et d'éviter les attaques comme l'injection de fichiers malveillants.

📄 Licence

Ce projet est sous licence MIT. Consultez le fichier LICENSE pour plus de détails.
