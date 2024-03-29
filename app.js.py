from flask import Flask, render_template, request
from backend import stitch_images
from werkzeug.utils import secure_filename
import os
import cv2

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_images():
    # Create a list to store the images
    images = []

    # Iterate over the files in the request
    for file in request.files.getlist('imageUpload'):
        # Use the secure_filename function to ensure a safe filename
        filename = secure_filename(file.filename)
        # Save the file to a directory
        filepath = os.path.join('uploads', filename)
        file.save(filepath)
        # Read the image file and convert it to a numpy array
        image = cv2.imread(filepath)
        # Append the image to the images list
        images.append(image)

    # Call the stitch_images function
    stitch_result = stitch_images(images)

    # Code to handle the stitch_result

    return render_template('upload.html')

@app.route('/edge')
def edge():
    return render_template('edge.html')

if __name__ == '__main__':
    app.run(debug=True)