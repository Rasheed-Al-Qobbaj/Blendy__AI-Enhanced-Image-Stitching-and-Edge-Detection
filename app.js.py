from flask import Flask, render_template, request, session
from backend import stitch_images, canny_edge_detection, dog_edge_detection, human_segmentation
from werkzeug.utils import secure_filename
import os
import cv2

app = Flask(__name__)
app.secret_key = 'sk'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_images():
    # Step 1: Clear the uploads directory
    for filename in os.listdir('static/uploads'):
        os.remove('static/uploads/' + filename)

    # Step 2: Initialize lists to store the images and filenames
    images = []
    filenames = []

    # Step 3: Iterate over the files in the request
    for file in request.files.getlist('imageUpload'):
        # Secure the filename
        filename = secure_filename(file.filename)
        # Save the filename to the filenames list
        filenames.append(filename)
        # Define the filepath
        filepath = os.path.join('static/uploads', filename)
        # Save the file to the filepath
        file.save(filepath)
        # Read the image file and convert it to a numpy array
        image = cv2.imread(filepath)
        # Append the image to the images list
        images.append(image)

    # Step 4: Call the stitch_images function
    stitch_result = stitch_images(images)

    # Step 5: Check if the stitching was successful
    if stitch_result == 1:
        return render_template('upload.html', result='Stitching successful!', image='result/stitch_result.jpg', images=filenames)
    else:
        # Pass the status code and explanation to the template
        explanation = f"Stitching failed due to error code: {stitch_result}. Please ensure the images can be stitched together."
        return render_template('upload.html', result='Stitching failed!', image='', images=filenames,status_code=stitch_result, explanation=explanation)


@app.route('/edge')
def edge():
    stitched = cv2.imread('static/result/stitch_result.jpg')
    canny_edge_detection(stitched)
    dog_edge_detection(stitched, session.get('kernel_size', 19))
    return render_template('edge.html', canny_image='result/canny_edges.jpg', dog_image='result/dog_edges.jpg', kernel_size=session.get('kernel_size', 19))

@app.route('/edge_dog', methods=['POST'])
def edge_dog():
    kernel_size = int(request.form['dogKernelSize'])
    # Ensure the kernel size is odd
    if kernel_size % 2 == 0:
        kernel_size += 1
    session['kernel_size'] = kernel_size
    stitched = cv2.imread('static/result/stitch_result.jpg')
    dog_edge_detection(stitched, kernel_size)
    return render_template('edge.html', canny_image='result/canny_edges.jpg', dog_image='result/dog_edges.jpg', kernel_size=kernel_size)

@app.route('/human_seg')
def human_seg():
    stitched = cv2.imread('static/result/stitch_result.jpg')
    human_segmentation(stitched)
    return render_template('human_seg.html', human_image='result/human_seg.jpg')

if __name__ == '__main__':
    app.run(debug=True)