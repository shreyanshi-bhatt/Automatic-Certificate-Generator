from flask import Flask, render_template, request, send_file
from PIL import ImageFont, ImageDraw, Image
import cv2
import numpy as np
from datetime import date
import os
from werkzeug.utils import secure_filename
import zipfile

app = Flask(__name__)

# Ensure the upload folder exists
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# Function to resize the image to fit within a specific width
def resize_image(img, max_width=800):
    height, width = img.shape[:2]
    if width > max_width:
        scale = max_width / width
        new_width = int(width * scale)
        new_height = int(height * scale)
        img = cv2.resize(img, (new_width, new_height))
    return img

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    # Check if the post request has the file part
    if 'names_file' not in request.files:
        return 'No file part'
    file = request.files['names_file']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        # Read names from uploaded file
        with open(file_path, "r") as f:
            names_list = f.read().strip().split("\n")

        # Read coordinates from file
        with open("coords.txt", "r") as f:
            coordinates = f.read().strip().split("\n")

        font_path = './fonts/OLDENGL.TTF'
        font1_path = './fonts/MATURASC.TTF'

        # Clear the output folder
        for file in os.listdir(OUTPUT_FOLDER):
            os.remove(os.path.join(OUTPUT_FOLDER, file))

        for name in names_list:
            image = cv2.imread("static/ce1.png")
            image = resize_image(image)
            cv2_im_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            pil_im = Image.fromarray(cv2_im_rgb)
            draw = ImageDraw.Draw(pil_im)
            font = ImageFont.truetype(font_path, 30)
            font1 = ImageFont.truetype(font1_path, 20)
            draw.text((int(coordinates[0]), int(coordinates[1])), name, font=font, fill='red')
            draw.text((int(coordinates[2]), int(coordinates[3])), str(date.today()), font=font1, fill='#283361')
            draw.text((int(coordinates[4]), int(coordinates[5])), 'Shreyanshi Bhatt', font=font1, fill='#283361')
            cv2_im_processed = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)
            cv2.imwrite(f'{OUTPUT_FOLDER}/{name}.png', cv2_im_processed)

        # Create a zip file of the output folder
        zip_filename = 'output.zip'
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            for root, dirs, files in os.walk(OUTPUT_FOLDER):
                for file in files:
                    zipf.write(os.path.join(root, file), file)

        # Delete the uploaded file
        os.remove(file_path)

        return send_file(zip_filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
