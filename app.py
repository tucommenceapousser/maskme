import os
import cv2
import numpy as np
import mediapipe as mp
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
from PIL import Image

# Configuration Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['RESULT_FOLDER'] = 'static/results'

# Création des dossiers pour les images téléchargées et les résultats
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULT_FOLDER'], exist_ok=True)

# Configuration de Mediapipe
mp_face_detection = mp.solutions.face_detection
mp_face_mesh = mp.solutions.face_mesh  # Pour les landmarks du visage
mp_drawing = mp.solutions.drawing_utils

# Formulaire Flask
class UploadForm(FlaskForm):
    photo = FileField('Upload Your Photo', validators=[DataRequired()])
    submit = SubmitField('Add Mask')

def calculate_face_rotation(face_landmarks, image_width, image_height):
    """
    Calcule l'angle de rotation du visage en fonction des points de repère du visage.
    Retourne l'angle de rotation pour ajuster le masque.
    """
    left_eye = face_landmarks[33]
    right_eye = face_landmarks[133]

    dx = right_eye[0] - left_eye[0]
    dy = right_eye[1] - left_eye[1]
    angle = np.degrees(np.arctan2(dy, dx))  # Convertir en degrés

    return angle

def add_mask_to_face(image_path, mask_path, result_path):
    # Charger l'image et le masque
    image = cv2.imread(image_path)
    mask = cv2.imread(mask_path, cv2.IMREAD_UNCHANGED)  # Conserver la transparence

    # Détecter les visages avec Mediapipe
    with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection, \
         mp_face_mesh.FaceMesh(min_detection_confidence=0.5) as face_mesh:
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_detection.process(image_rgb)

        if results.detections:
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = image.shape
                x, y, w, h = (int(bboxC.xmin * iw), int(bboxC.ymin * ih),
                              int(bboxC.width * iw), int(bboxC.height * ih))

                # Extraire les points de repère du visage pour calculer la rotation
                face_landmarks = face_mesh.process(image_rgb).multi_face_landmarks
                if face_landmarks:
                    landmarks = face_landmarks[0].landmark
                    face_points = [(lm.x * iw, lm.y * ih) for lm in landmarks]

                    # Calculer l'angle de rotation
                    angle = calculate_face_rotation(face_points, iw, ih)

                    # Ajuster la taille du masque
                    mask_width = w
                    mask_height = h
                    resized_mask = cv2.resize(mask, (mask_width, mask_height))

                    # Appliquer la rotation au masque
                    center = (mask_width // 2, mask_height // 2)
                    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
                    rotated_mask = cv2.warpAffine(resized_mask, rotation_matrix, (mask_width, mask_height))

                    # Appliquer le masque avec transparence
                    for i in range(mask_height):
                        for j in range(mask_width):
                            if rotated_mask[i, j, 3] > 0:  # Transparence
                                image[y + i, x + j] = rotated_mask[i, j, :3]

    # Sauvegarder le résultat
    cv2.imwrite(result_path, image)

@app.route('/', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        file = form.photo.data
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        output_path = os.path.join(app.config['RESULT_FOLDER'], 'result_' + filename)

        # Sauvegarder l'image uploadée
        file.save(input_path)

        # Appliquer le masque
        mask_path = 'mask.png'  # Chemin vers le masque
        add_mask_to_face(input_path, mask_path, output_path)

        return redirect(url_for('result', filename='result_' + filename))
    return render_template('upload.html', form=form)

@app.route('/result/<filename>')
def result(filename):
    result_url = url_for('static', filename=f'results/{filename}')
    return render_template('result.html', result_url=result_url)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)