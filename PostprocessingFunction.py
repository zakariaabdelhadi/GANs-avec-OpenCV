# read image as grayscale
# import cv2
#
# img = cv2.imread('C:\\Users\\ZAKARIA\\Desktop\\noise.jpg', cv2.IMREAD_GRAYSCALE)
#
# # threshold to binary
# thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY)[1]
#
# # apply morphology
# kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
# morph = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
#
# # find contours - write black over all small contours
# letter = morph.copy()
# cntrs = cv2.findContours(morph, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# cntrs = cntrs[0] if len(cntrs) == 2 else cntrs[1]
# for c in cntrs:
#     area = cv2.contourArea(c)
#     if area < 100:
#         cv2.drawContours(letter,[c],0,(0,0,0),-1)
#
# cv2.imshow('tiri berk',letter)
# cv2.waitKey()
#
# cv2.imshow('tiri berk',img)
#
# cv2.waitKey()
# # -----------------------
import cv2
import numpy as np

# load image
img = cv2.imread("C:\\Users\\ZAKARIA\\Desktop\\noise.jpg")

# convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# blur
blur = cv2.GaussianBlur(gray, (0,0), sigmaX=33, sigmaY=33)

# divide
divide = cv2.divide(gray, blur, scale=255)

# otsu threshold
thresh = cv2.threshold(divide, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]

# apply morphology
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

# write result to disk
# cv2.imwrite("hebrew_text_division.jpg", divide)
# cv2.imwrite("hebrew_text_division_threshold.jpg", thresh)
# cv2.imwrite("hebrew_text_division_morph.jpg", morph)

# display it
cv2.imshow("gray", gray)
cv2.imshow("divide", divide)
cv2.imshow("thresh", thresh)
cv2.imshow("morph", morph)
cv2.waitKey(0)
cv2.destroyAllWindows()

# #---------------
# # https://opencv.org/openvino-merging-pre-and-post-processing-into-the-model/