from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
import numpy as np
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ASCII_CHARS = "@%#*+=-:. "

def image_to_ascii(image_path):
    image = Image.open(image_path)
    grayscale_image = image.convert('L')
    aspect_ratio = grayscale_image.width / grayscale_image.height
    new_width = 100
    new_height = int(new_width / aspect_ratio)
    grayscale_image = grayscale_image.resize((new_width, new_height))
    image_array = np.array(grayscale_image)
    normalized_pixels = (image_array / 255.0) * (len(ASCII_CHARS) - 1)
    normalized_pixels = normalized_pixels.astype(int)
    ascii_art = ""
    for row in normalized_pixels:
        for pixel in row:
            ascii_art += ASCII_CHARS[pixel]
        ascii_art += "\n"
    return ascii_art

@app.route('/', methods=['GET', 'POST'])
def index():
    ascii_art = ""
    file = None
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            ascii_art = image_to_ascii(file_path)
    return render_template('ascii index.html', ascii_art=ascii_art, file=file)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
