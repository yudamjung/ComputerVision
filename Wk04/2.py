import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import sys

img = cv.imread('computervision_img.png', cv.IMREAD_UNCHANGED)
img2 = cv.imread('computervision_img2.png', cv.IMREAD_UNCHANGED)

if img is None:
    sys.exit('파일을 찾을 수 없습니다.')
    
if img2 is None:
    sys.exit('파일을 찾을 수 없습니다.')
    
t, bin_img = cv.threshold(img[:,:,0], 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
plt.imshow(bin_img,cmap='gray'), plt.xticks([]), plt.yticks([])
plt.show()


tt, bin_img2 = cv.threshold(img2[:,:,0], 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
plt.imshow(bin_img,cmap='gray'), plt.xticks([]), plt.yticks([])
plt.show()

"""
# 구조 요소
se = np.uint8([[0,0,1,0,0],
               [0,1,1,1,0],
               [1,1,1,1,1],
               [0,1,1,1,0],
               [0,0,1,0,0]])
"""

"""
se = np.uint8([[1,1,1,1,1],
               [1,1,1,1,1],
               [1,1,1,1,1],
               [1,1,1,1,1],
               [1,1,1,1,1]])
"""

se = np.uint8([[1,1,1],
               [1,1,1],
               [1,1,1]])

b = cv.erode(bin_img, se, iterations=2)
b = cv.dilate(b, se, iterations=2)

plt.imshow(b, cmap='gray'), plt.xticks([]), plt.yticks([])
plt.show()


b2 = cv.dilate(bin_img2, se, iterations=1)
b2 = cv.erode(b2, se, iterations=1)

plt.imshow(b2, cmap='gray'), plt.xticks([]), plt.yticks([])
plt.show()
"""
img_erosion = cv.erode(img, se, iterations=3)
img_erosion = cv.dilate(img_erosion, se, iterations=2)
plt.imshow(img_erosion, cmap='gray'), plt.xticks([]), plt.yticks([])
plt.show()

img2_dilation = cv.dilate(img2, se, iterations=1)
img2_erosion = cv.erode(img2_dilation, se, iterations=1)
plt.imshow(img2_erosion, cmap='gray'), plt.xticks([]), plt.yticks([])
plt.show()
"""

cv.waitKey()
cv.destroyAllWindows()