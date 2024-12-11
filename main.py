import os
import cv2
import numpy as np
import mediapipe as mp
import openai
import requests
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import time

# Configuration Flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['RESULT_FOLDER'] = 'static/results'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULT_FOLDER'], exist_ok=True)

# Mediapipe pour la détection de visages
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# OpenAI API Configuration
openai.api_key = os.environ['OPENAI_API_KEY']

# Délai d'attente personnalisé pour OpenAI
class CustomTransportAdapter(requests.adapters.HTTPAdapter):
    def __init__(self, timeout=None, *args, **kwargs):
        self.timeout = timeout
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        kwargs['timeout'] = self.timeout
        return super().send(request, **kwargs)

def configure_openai_timeout(timeout):
    session = requests.Session()
    adapter = CustomTransportAdapter(timeout=timeout)
    session.mount('https://', adapter)
    session.mount('http://', adapter)
    openai.requestssession = session

# Configurer le délai d'attente (par exemple, 60 secondes)
configure_openai_timeout(timeout=60)

def generate_mask_with_dalle():
    """
    Utilise OpenAI DALL·E pour générer un masque dynamique.
    """
    try:
        response = openai.Image.create(
            prompt="A realistic image of a mask to be applied on a human face, black with green neon borders, optimized for facial detection.",
            n=1,
            size="512x512",
        )
        image_url = response['data'][0]['url']
        return image_url
    except openai.OpenAIError as e:  # Catches all OpenAI API errors
        print(f"Erreur OpenAI : {str(e)}")
        return None
    except openai.APIConnectionError as e:  # Catches API connection errors
        print(f"Erreur de connexion à l'API OpenAI : {str(e)}")
        return None
    except openai.Timeout as e:  # Catches timeout errors
        print(f"Erreur de timeout avec OpenAI : {str(e)}")
        return None
    except Exception as e:  # Catches any other exceptions
        print(f"Erreur inattendue : {str(e)}")
        return None

def add_masks_to_faces(image_path, mask_path, result_path):
    """
    Détecte plusieurs visages, applique un masque à chaque visage détecté.
    """
    image = cv2.imread(image_path)
    mask = cv2.imread(mask_path, cv2.IMREAD_UNCHANGED)  # Charge le masque avec transparence
    ih, iw, _ = image.shape

    # Détection de visages
    with mp_face_detection.FaceDetection(min_detection_confidence=0.6) as face_detection:
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_detection.process(image_rgb)

        if results.detections:
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)

                # Redimensionner le masque pour chaque visage
                mask_resized = cv2.resize(mask, (w, h), interpolation=cv2.INTER_AREA)

                # Appliquer le masque avec transparence
                for i in range(h):
                    for j in range(w):
                        if 0 <= y + i < ih and 0 <= x + j < iw:
                            alpha = mask_resized[i, j, 3] / 255.0  # Transparence
                            image[y + i, x + j] = alpha * mask_resized[i, j, :3] + (1 - alpha) * image[y + i, x + j]

    # Sauvegarder l'image
    cv2.imwrite(result_path, image)

@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Gestion du fichier uploadé
        file = request.files['photo']
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        output_path = os.path.join(app.config['RESULT_FOLDER'], 'result_' + filename)

        # Sauvegarder l'image
        file.save(input_path)

        # Générer un masque avec DALL·E (optionnel)
        dalle_mask_url = generate_mask_with_dalle()

        if dalle_mask_url:
            mask_path = "static/mask.png"
            os.system(f"wget {dalle_mask_url} -O {mask_path}")
        else:
            mask_path = "static/default_mask.png"  # Utiliser un masque par défaut en cas d'erreur

        # Ajouter les masques
        add_masks_to_faces(input_path, mask_path, output_path)

        return redirect(url_for('result', filename='result_' + filename))
    return render_template('upload.html')

@app.route('/result/<filename>')
def result(filename):
    result_url = url_for('static', filename=f'results/{filename}')
    return render_template('result.html', result_url=result_url)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)