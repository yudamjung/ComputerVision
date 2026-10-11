import cv2 as cv
import numpy as np

img = cv.imread('building.jpg')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
gray = np.float32(gray)
dist = cv.cornerHarris(gray, 3, 3, 0.04)
img[dist > 0.05 * dist.max()] = [0, 0, 255]
cv.imshow('dist', img)
cv.waitKey()
cv.destroyAllWindows()

"""
Harris corner detector.

The function runs the Harris corner detector on the image. Similarly to cornerMinEigenVal and cornerEigenValsAndVecs , for each pixel 
 it calculates a gradient covariance matrix over a neighborhood. Then, it computes the following characteristic:

Corners in the image can be found as the local maxima of this response map.

Parameters

src — Input single-channel 8-bit or floating-point image.

dst — Image to store the Harris detector responses. It has the type CV_32FC1 and the same size as src .

blockSize — Neighborhood size (see the details on cornerEigenValsAndVecs ).

ksize — Aperture parameter for the Sobel operator.

k — Harris detector free parameter. See the formula above.

borderType — Pixel extrapolation method. See BorderTypes. BORDER_WRAP is not supported.
"""