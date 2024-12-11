# 🛠️ **Anonymous Face Masking Tool by TRHACKNON** 🛠️

![GitHub Repo stars](https://img.shields.io/github/stars/tucommenceapousser/maskme?style=for-the-badge&logo=github)

 
![anonymous](https://img.shields.io/badge/anonymous-000000?style=for-the-badge&logo=ghost&logoColor=FF0000)

![TRHACKNON](https://img.shields.io/badge/TRHACKNON-000000?style=for-the-badge&logo=three.js&logoColor=FF0000)

![tucommenceapousser](https://img.shields.io/badge/tucommenceapousser-000000?style=for-the-badge&logo=github&logoColor=FF0000)


![Kali](https://img.shields.io/badge/Kali-000000?style=for-the-badge&logo=kalilinux&logoColor=FF0000)

![Modded By](https://img.shields.io/badge/Modded%20by-Trhacknon-ff69b4?style=for-the-badge&logo=github)

![Followers](https://img.shields.io/github/followers/tucommenceapousser?style=for-the-badge&color=ff0000)

![Trhacknon's GitHub Stats](https://github-readme-stats.vercel.app/api?username=tucommenceapousser&show_icons=true&count_private=true&hide=prs&theme=tokyonight&bg_color=000000&title_color=ff0000&text_color=ff0000&layout=compact&border_color=0099ff)

![Trhacknon's Top Languages](https://github-readme-stats.vercel.app/api/top-langs/?username=tucommenceapousser&layout=compact&theme=highcontrast&border_color=1b03a3)

Un outil simple mais puissant permettant d'ajouter un masque anonyme à des visages sur des images. Ce projet utilise **Flask** pour l'interface web, **OpenCV** pour le traitement d'image, et **MediaPipe** pour la détection et l'analyse des visages.

## 🚀 **Fonctionnalités**

- Téléchargez une photo.
- Appliquez un masque de style "anonymous" sur les visages détectés.
- Rotation et redimensionnement automatique du masque pour s'adapter à l'orientation et à la taille du visage.
- Visualisation du résultat avec un simple lien de téléchargement.

## 📝 **Versions du Projet**

J'ai volontairement laissé différentes versions du projet, chacune ayant des caractéristiques spécifiques. 

### 💡 **Version avec IA**
- **Fichier principal** : `main.py`
- Cette version intègre des fonctionnalités basées sur l'intelligence artificielle, permettant une interaction plus avancée et des résultats plus précis. 

Les autres versions sont simplifiées ou contiennent des configurations spécifiques pour des tests ou des démonstrations particulières.
Nous utilisons principalement numpy, mp, cv2, ...

### Explication :
#### Deux Solutions Possibles

- **`pip install --upgrade openai` et `openai migrate`** : Utilise la commande `migrate` pour mettre à jour automatiquement le projet vers la dernière version d'OpenAI, avec des ajustements nécessaires pour la compatibilité.

- **`pip install openai==0.28`** : Installe spécifiquement la version 0.28 de la bibliothèque OpenAI.

### Configuration de l'API OpenAI

Pour utiliser l'API OpenAI, vous devez ajouter votre clé API dans un fichier `.env` à la racine du projet.

#### Étapes :

1. Créez un fichier `.env` à la racine de votre projet (si ce n'est pas déjà fait).
2. Ajoutez la ligne suivante dans ce fichier :

   ```dotenv
   OPENAI_API_KEY=your-api-key-here
   ```
3. Remplacez your-api-key-here par votre propre clé API obtenue depuis OpenAI.



Exemple de contenu du fichier .env :

**`OPENAI_API_KEY=sk-XXXXXXXXXXXXXXXXXXXX`**

> Important : Assurez-vous que le fichier .env est ajouté à votre .gitignore pour éviter de partager votre clé API sur des dépôts publics.






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
