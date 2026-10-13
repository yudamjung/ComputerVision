import cv2 as cv

img = cv.imread("mot_color70.jpg")
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

sift = cv.SIFT_create()
kp, des = sift.detectAndCompute(gray, None)
"""
특징점을 detect 하고
기술자를 Compute 해서 반환
cv.Feature2D.detectAndCompute(image, mask[, descriptors[, useProvidedKeypoints]]) -> keypoints, descriptors
Detects keypoints and computes the descriptors
"""

gray = cv.drawKeypoints(gray, kp, None, flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
"""
Python:

cv.drawKeypoints(image, keypoints, outImage[, color[, flags]]) -> outImage
Draws keypoints.

Params:
image — Source image.
keypoints — Keypoints from the source image.
outImage — Output image. Its content depends on the flags value defining what is drawn in the output image. See possible flags bit values below.
color — Color of keypoints.
flags — Flags setting drawing features. Possible flags bit values are defined by DrawMatchesFlags. See details above in drawMatches .

cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
=> For each keypoint the circle around keypoint with keypoint size and orientation will be drawn.
"""
cv.imshow("sift", gray)

k = cv.waitKey()
cv.destroyAllWindows()