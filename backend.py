import numpy as np
import cv2

# Image Selection and Stitching
left = cv2.imread("photos/stitch_left.jpg")
right = cv2.imread("photos/stitch_right.jpg")

stitcher = cv2.Stitcher_create()

status, result = stitcher.stitch([left, right])

if status == cv2.Stitcher_OK:
    cv2.imwrite("photos/stitch_result.jpg", result)
    print("Stitching successful!")
else:
    print("Stitching failed!")


# Edge Detection Implementation

stitched = cv2.imread("photos/stitch_result.jpg")

# Apply Canny Edge Detection
gray = cv2.cvtColor(stitched, cv2.COLOR_BGR2GRAY)
v = np.median(gray)
lower = int(0.68 * v)
upper = int(1.32 * v)

# Apply automatic Canny edge detection using the computed thresholds
canny = cv2.Canny(gray, lower, upper)

cv2.imwrite("photos/canny_edges.jpg", canny)

print("Canny Edge detection complete!")

# Implement Difference of Gaussians (DoG) edge detection followed by a morphological operation to clean the results
# Apply GaussianBlur
blurred = cv2.GaussianBlur(gray, (7, 7), 1)

# Apply Difference of Gaussians
dog = cv2.subtract(blurred, cv2.GaussianBlur(blurred, (19, 19), 3))

# Apply morphological operation
kernel = np.array([[0, 1, 0],
                          [1, 1, 1],
                          [0, 1, 0]], np.uint8)
dog = cv2.morphologyEx(dog, cv2.MORPH_CLOSE, kernel)

cv2.imwrite("photos/dog_edges.jpg", dog)

print("Difference of Gaussians (DoG) edge detection complete!")