""" Apply
Median
blur
3
"""
# medianBlur() is used to apply Median blur to image
# ksize is the kernel size
import cv2
import numpy as np
image='C:\\Users\\ZAKARIA\\Desktop\\New folder\\CFD Version 3.0\\Images\\blur.jpg'
img = cv2.imread(cv2.samples.findFile(image))

dim = (600, 600)
# resize image
img_r = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)


median = cv2.medianBlur(src=img_r, ksize=5)
#blur_fct = cv2.blur(src=img_r, ksize=(5,5)) # Using the blur function to blur an image where ksize is the kernel size
gray = cv2.cvtColor(median, cv2.COLOR_BGR2GRAY)
(thresh, blackAndWhiteImage) = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
cv2.imshow('black_white', blackAndWhiteImage)

cv2.imshow('Original', gray)
cv2.imshow('Median Blurred', median)



cv2.waitKey()

#cv2.imwrite('median_blur.jpg', median)

cv2.destroyAllWindows()
