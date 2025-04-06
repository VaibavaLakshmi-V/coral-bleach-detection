import os
from flask import Flask, render_template, request
import cv2
import numpy as np

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def analyze_image(image_path):
    image = cv2.imread(image_path)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (0, 0, 180), (180, 80, 255))
    white_area = cv2.countNonZero(mask)
    total_area = image.shape[0] * image.shape[1]
    white_ratio = white_area / total_area
    result = "Bleaching likely detected." if white_ratio > 0.15 else "Coral appears healthy."
    return result

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    image_url = None
    if request.method == 'POST':
        file = request.files['image']
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            result = analyze_image(filepath)
            image_url = filepath
    return render_template('index.html', result=result, image=image_url)

if __name__ == '__main__':
    app.run(debug=True)
