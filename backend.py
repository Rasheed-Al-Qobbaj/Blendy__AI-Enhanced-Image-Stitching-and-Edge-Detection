import numpy as np
import cv2
import os

# Image Selection and Stitching
def select_images(Path):
    image_paths = [Path + '/' + f for f in os.listdir(path=Path)]
    images = []
    for path in image_paths:
        image = cv2.imread(path)
        images.append(image)
    return images


# Stitching
def stitch_images(images):
    stitcher = cv2.Stitcher_create()
    status, result = stitcher.stitch(images)
    if status == cv2.Stitcher_OK:
        cv2.imwrite("result/stitch_result.jpg", result)
        print("Stitching successful!")
        return 1
    return status


# Edge Detection Implementation

# Apply Canny Edge Detection
def canny_edge_detection(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    v = np.median(gray)
    lower = int(0.68 * v)
    upper = int(1.32 * v)
    canny = cv2.Canny(gray, lower, upper)
    cv2.imwrite("result/canny_edges.jpg", canny)
    print("Canny Edge detection complete!")
    return canny



# Implement Difference of Gaussians (DoG) edge detection followed by a morphological operation to clean the results
def dog_edge_detection(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 1)
    dog = cv2.subtract(blurred, cv2.GaussianBlur(blurred, (19, 19), 3))
    kernel = np.array([[0, 1, 0],
                          [1, 1, 1],
                          [0, 1, 0]], np.uint8)
    dog = cv2.morphologyEx(dog, cv2.MORPH_CLOSE, kernel)
    cv2.imwrite("result/dog_edges.jpg", dog)
    print("Difference of Gaussians (DoG) edge detection complete!")
    return dog

if __name__ == '__main__':
    images = select_images('input_image/parrington')
    result = stitch_images(images)
    if result == 1:
        stitched = cv2.imread("result/stitch_result.jpg")
        canny_edge_detection(stitched)
        dog_edge_detection(stitched)
    else:
        print("Stitching failed! Status code: ", result)

# Todo: 1- Implement AI human detection using YOLO
# Todo: 2- Start designing the frontend and backend using fastapi
# Todo: 3- Report the results
