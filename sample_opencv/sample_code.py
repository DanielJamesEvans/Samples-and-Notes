import cv2
import numpy as np

# LOAD THE IMAGE.
# Flag options: cv2.IMREAD_COLOR, cv2.IMREAD_GRAYSCALE, and cv2.IMREAD_UNCHANGED.
# Note that cv2.IMREAD_UNCHANGED loads the alpha channel (which determines transparency).
img_color = cv2.imread("input_image.jpg", cv2.IMREAD_COLOR)


# RESIZE THE IMAGE SO THAT IT FITS ON THE SCREEN.
height, width, depth = img_color.shape
img_color_resized = cv2.resize(img_color, (int(width/5), int(height/5)))
cv2.imshow("Original Image (Resized)", img_color_resized)

# CONVERT THE IMAGE TO GRAYSCALE.
img_gray = cv2.cvtColor(img_color_resized, cv2.COLOR_BGR2GRAY)
cv2.imshow("Grayscale Image", img_gray)

# THRESHOLD THE IMAGE.
# Way #1: binary threshold.
# The second argument is the threshold value.  The third argument is
# the value that pixels above the threshold are set to.
ret_binary, img_thresh_binary = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)
cv2.imshow("Binary Threshold Image", img_thresh_binary)
# Way #2: Adaptive (useful if lighting changes throughout picture)
# The second-to-last argument is the size of the area being considered for the thresholding.
# The last argument is C, which is used by the algorithm.
# Note that the box size can vary dramatically from case to case.  Try lots of values!
img_thresh_adapt = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 33, 2)
cv2.imshow("Adaptive Threshold Image", img_thresh_adapt)

# OPENING (EROSION THEN DILATION) TO REMOVE SPOTS
kernel = np.ones((3, 3), np.uint8)
img_open = cv2.morphologyEx(img_thresh_adapt, cv2.MORPH_OPEN, kernel)
cv2.imshow("Opening Image", img_open)

# FIND THE CONTOURS.
# The second argument deals with contour hierarchies.  This only matters if contour hierarchies are necessary.
# The third argument allows the user to save memory by not storing all of the contour's points.
# It appears that img_cont_return is probably the same as the input image.
img_cont_return, contours, hierarchy = cv2.findContours(img_open, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
#img_cont_return, contours, hierarchy = cv2.findContours(img_thresh_adapt, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

# FIND AND DRAW THE LARGEST 2 CONTOURS.
contours_sorted = sorted(contours, key = lambda x: cv2.contourArea(x), reverse = True)
# The third argument is the index of the contour being drawn.  Pass -1 to draw all.
# The fourth argument is the color.
cv2.drawContours(img_color_resized, contours_sorted, 0, (0, 255, 0))
cv2.drawContours(img_color_resized, contours_sorted, 1, (0, 255, 0))

# draw circles around the contours.
(x,y),radius = cv2.minEnclosingCircle(contours_sorted[0])
center = (int(x),int(y))
radius = int(radius)
cv2.circle(img_color_resized, center, radius, (0, 0,255))

(x,y),radius = cv2.minEnclosingCircle(contours_sorted[1])
center = (int(x),int(y))
radius = int(radius)
cv2.circle(img_color_resized, center, radius, (0, 0,255))

cv2.imshow("Contours", img_color_resized)

cv2.waitKey(0)
cv2.destroyAllWindows()

