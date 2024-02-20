from flask import Flask, jsonify, request, render_template
import cv2
import easyocr
import numpy as np
import os
import json
from flask import make_response
app = Flask(__name__)

#from flask import Flask
from flask_cors import CORS
#app = Flask(__name__)
CORS(app)

# Function to preprocess the license plate image
def preprocess_license_plate(image_path):
    # Check if the image file exists
    if not os.path.exists(image_path):
        return None, "Error: Image file not found."

    # Read the image in BGR color
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to convert to binary image
    _, binary_image = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)

    # Apply morphological operations for noise removal and feature enhancement
    kernel = np.ones((5, 13), np.uint8)
    morph = cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, kernel, iterations=3)

    return image, morph


# Function to extract license plate text using OCR
def extract_license_plate_text(plate_img):
    # Check if the plate image is None
    if plate_img is None:
        return "Error: Failed to preprocess the license plate image."

    # Convert the plate image to RGB format
    plate_img_rgb = cv2.cvtColor(plate_img, cv2.COLOR_BGR2RGB)

    # Initialize the OCR reader for Korean language
    reader = easyocr.Reader(['ko'])

    # Use OCR to extract text from the plate image
    results = reader.readtext(plate_img_rgb)

    # Check if OCR results are available
    if results:
        plate_text = results[0][1]
        return plate_text
    else:
        return "Error: Failed to extract license plate text."


@app.route('/')
def upload_form():
    return render_template('apphtml.html')

# Route to upload image and extract license plate text
@app.route('/upload_and_extract_license_plate_text', methods=['POST'])

def upload_and_extract_license_plate_text():
    try:
        # Check if the POST request has the file part
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']

        # Check if the file is empty
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if file:
            # Save the uploaded file
            filename = file.filename
            file_path = os.path.join('uploaded_images', filename)
            file.save(file_path)

            # Preprocess the license plate image
            plate_img, _ = preprocess_license_plate(file_path)

            # Extract license plate text
            plate_text = extract_license_plate_text(plate_img)


            # Decode Unicode escape sequences


            # Return extracted license plate text as JSON response
            response = {'filename': filename, 'plate_text': plate_text}

            result = json.dumps(response, ensure_ascii=False)
            res = make_response(result)
            return res
            #return jsonify(res), 200, {'Content-Type': 'application/json; charset=utf-8'}
    except Exception as e:
        # Handle exceptions and return error message
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # Run the Flask app
    #app.run(port=5001)
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=5001)