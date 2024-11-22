from flask import Flask, request, jsonify, send_file
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import cv2
import os

app = Flask(__name__)

# Load pre-trained model
model = load_model("prostate_cancer_model.h5")

# Upload folder
UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER

# Preprocess image
def preprocess_image(image_path):
    img = Image.open(image_path).resize((224, 224))
    img_array = np.array(img) / 255.0
    return np.expand_dims(img_array, axis=0)

# Overlay cancerous region (mock implementation)
def generate_overlay(image_path, label):
    img = cv2.imread(image_path)
    if label == "Cancerous":
        cv2.rectangle(img, (50, 50), (200, 200), (0, 0, 255), 2)  # Mock cancer region
    overlay_path = os.path.join(RESULT_FOLDER, os.path.basename(image_path))
    cv2.imwrite(overlay_path, img)
    return overlay_path

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    image = request.files['image']
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
    image.save(image_path)

    # Preprocess and predict
    img_array = preprocess_image(image_path)
    prediction = model.predict(img_array)
    label = "Cancerous" if prediction[0][0] > 0.5 else "Non-Cancerous"

    # Generate overlay
    overlay_path = generate_overlay(image_path, label)

    return jsonify({
        "originalImage": f"http://localhost:5000/uploads/{image.filename}",
        "cancerOverlay": f"http://localhost:5000/results/{os.path.basename(overlay_path)}",
        "label": label
    })

@app.route('/uploads/<filename>')
def get_uploaded_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))

@app.route('/results/<filename>')
def get_result_file(filename):
    return send_file(os.path.join(app.config['RESULT_FOLDER'], filename))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
