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

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULT_FOLDER'], exist_ok=True)

# Mediapipe configuration
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# Formulaire
class UploadForm(FlaskForm):
    photo = FileField('Upload Your Photo', validators=[DataRequired()])
    submit = SubmitField('Add Mask')

def add_mask_to_face(image_path, mask_path, result_path):
    # Charger l'image et le masque
    image = cv2.imread(image_path)
    mask = cv2.imread(mask_path, cv2.IMREAD_UNCHANGED)  # Conserver la transparence

    # Détecter les visages
    with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_detection.process(image_rgb)

        if results.detections:
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = image.shape
                x, y, w, h = (int(bboxC.xmin * iw), int(bboxC.ymin * ih),
                              int(bboxC.width * iw), int(bboxC.height * ih))

                # Redimensionner et positionner le masque
                resized_mask = cv2.resize(mask, (w, h))
                for i in range(h):
                    for j in range(w):
                        if resized_mask[i, j, 3] > 0:  # Transparence
                            image[y + i, x + j] = resized_mask[i, j, :3]

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