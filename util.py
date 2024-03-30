import numpy as np
import cv2
import os
from ultralytics import YOLO

# Load YOLO model for human segmentation
model = YOLO('yolov8n-seg.pt')

# Image Selection and Stitching
def select_images(Path):
    """
    This function selects all images from a given directory and reads them into a list.

    Parameters:
    Path (str): The path to the directory containing the images.

    Returns:
    list: A list of images read from the directory.
    """
    # Create a list of all image paths in the directory
    image_paths = [Path + '/' + f for f in os.listdir(path=Path)]

    # Initialize an empty list to store the images
    images = []

    # Loop through each image path
    for path in image_paths:
        # Read the image from the path
        image = cv2.imread(path)
        # Append the image to the list
        images.append(image)

    # Return the list of images
    return images


# Stitching
def stitch_images(images):
    """
    This function stitches together a list of images into a single panoramic image.

    Parameters:
    images (list): A list of images to be stitched together.

    Returns:
    int: Returns 1 if stitching is successful, otherwise returns the error status code.
    """
    # Create a Stitcher object
    stitcher = cv2.Stitcher_create()

    # Attempt to stitch the images together
    status, result = stitcher.stitch(images)

    # If the stitching was successful
    if status == cv2.Stitcher_OK:
        # Save the stitched image
        cv2.imwrite("static/result/stitch_result.jpg", result)
        print("Stitching successful!")
        return 1

    # If the stitching failed
    print("Stitching failed!")
    return status


# Edge Detection Implementation

# Apply Canny Edge Detection
def canny_edge_detection(image):
    """
    This function applies the Canny edge detection algorithm to an image.

    Parameters:
    image (numpy.ndarray): The input image on which edge detection will be performed.

    Returns:
    numpy.ndarray: The output image after applying Canny edge detection.
    """
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Calculate the median of the grayscale values
    v = np.median(gray)

    # Define the lower and upper thresholds for the Canny edge detection
    lower = int(0.68 * v)
    upper = int(1.32 * v)

    # Apply the Canny edge detection
    canny = cv2.Canny(gray, lower, upper)

    # Save the result to a file
    cv2.imwrite("static/result/canny_edges.jpg", canny)
    print("Canny Edge detection complete!")

    # Return the result
    return canny



# Implement Difference of Gaussians (DoG) edge detection followed by a morphological operation to clean the results
def dog_edge_detection(image, kernel_size=19):
    """
    This function applies the Difference of Gaussians (DoG) edge detection algorithm to an image.
    It first converts the image to grayscale, then applies a Gaussian blur to the grayscale image.
    It subtracts a more blurred version of the image from the less blurred version to get the DoG.
    Finally, it applies a morphological operation to clean up the edges.

    Parameters:
    image (numpy.ndarray): The input image on which edge detection will be performed.
    kernel_size (int, optional): The size of the kernel used for the Gaussian blur. Defaults to 19.

    Returns:
    numpy.ndarray: The output image after applying DoG edge detection.
    """
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply a Gaussian blur to the grayscale image
    blurred = cv2.GaussianBlur(gray, (7, 7), 1)

    # Subtract a more blurred version of the image from the less blurred version to get the DoG
    dog = cv2.subtract(blurred, cv2.GaussianBlur(blurred, (kernel_size, kernel_size), 3))

    # Define the kernel for the morphological operation
    kernel = np.array([[0, 1, 0],
                       [1, 1, 1],
                       [0, 1, 0]], np.uint8)

    # Apply a morphological operation to clean up the edges
    dog = cv2.morphologyEx(dog, cv2.MORPH_CLOSE, kernel)

    # Save the result to a file
    cv2.imwrite("static/result/dog_edges.jpg", dog)

    print("Difference of Gaussians (DoG) edge detection complete!")

    # Return the result
    return dog


# Human Segmentation
def human_segmentation(image):
    """
    This function applies human segmentation on an image using a pre-loaded YOLO model.
    The segmented image is then saved to a specified location.

    Parameters:
    image (numpy.ndarray): The input image on which human segmentation will be performed.

    Returns:
    None
    """
    # Apply the YOLO model to the image with a confidence threshold of 0.5 and class 0 (human)
    result = model(image, conf=0.5, classes=[0])

    # Loop through each result
    for r in result:
        # Save the result to a file
        r.save('static/result/human_seg.jpg')

    print("Human segmentation complete!")

# Main Function for Testing
if __name__ == '__main__':
    human_segmentation(cv2.imread('static/result/stitch_result.jpg'))

