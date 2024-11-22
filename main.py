from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import numpy as np
import cv2
import tensorflow as tf

app = FastAPI()

# Load pre-trained model
model = tf.keras.models.load_model("path_to_your_model.h5")

@app.post("/upload")
async def upload_image(image: UploadFile = File(...)):
    # Save the uploaded image
    image_path = f"uploads/{image.filename}"
    with open(image_path, "wb") as buffer:
        buffer.write(image.file.read())

    # Process the image
    img = Image.open(image_path).resize((224, 224))  # Example resizing
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Run inference
    predictions = model.predict(img_array)
    label = "Cancerous" if predictions[0][0] > 0.5 else "Non-Cancerous"

    # Generate overlay for cancerous areas (Mock Implementation)
    overlay = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    if label == "Cancerous":
        cv2.rectangle(overlay, (50, 50), (200, 200), (0, 0, 255), 2)

    overlay_path = f"results/{image.filename}_overlay.png"
    cv2.imwrite(overlay_path, overlay)

    return JSONResponse({
        "originalImage": f"http://localhost:5000/uploads/{image.filename}",
        "cancerOverlay": f"http://localhost:5000/results/{image.filename}_overlay.png",
        "label": label
    })
