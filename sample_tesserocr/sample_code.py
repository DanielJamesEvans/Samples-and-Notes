import cv2
import locale
locale.setlocale(locale.LC_ALL, 'C')
import tesserocr
from tesserocr import PyTessBaseAPI
import numpy as np
from PIL import Image

"""Part 1: OpenCV preprocessing"""

img_color = cv2.imread("test_image.JPG", cv2.IMREAD_COLOR)
height, width, depth = img_color.shape
img_color_resized = cv2.resize(img_color, (int(width/5), int(height/5)))
cv2.imshow("Original Image (Resized)", img_color_resized)

# CONVERT THE IMAGE TO GRAYSCALE.
img_gray = cv2.cvtColor(img_color_resized, cv2.COLOR_BGR2GRAY)
cv2.imshow("Grayscale Image", img_gray)

ret_binary, img_thresh_binary = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)
cv2.imshow("Binary Threshold Image", img_thresh_binary)

img_thresh_adapt = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 33, 2)
cv2.imshow("Adaptive Threshold Image", img_thresh_adapt)

kernel = np.ones((3, 3), np.uint8)
img_close = cv2.morphologyEx(img_thresh_adapt, cv2.MORPH_CLOSE, kernel)
cv2.imshow("Closing Image", img_close)

"""Part 2: tesserocr"""
# I think that tesserocr only accepts files or PIL objects.  So I converted from OpenCV to PIL.
img_pil = Image.fromarray(img_close)
print(tesserocr.image_to_text(img_pil))


cv2.waitKey(0)
cv2.destroyAllWindows()
