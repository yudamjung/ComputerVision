import cv2 as cv
import sys

img = cv.imread('soccer.jpg')

if img is None:
    sys.exit('파일을 찾을 수 없습니다.')

cv.imshow('original_RGB', img)
cv.imshow('Upper left half', img[0:img.shape[0]//2, :img.shape[1]//2, :]) # 4분의 1지점 slicing
cv.imshow('Center half', img[img.shape[0]//4 : 3*img.shape[0]//4, # 3 * 4분의 1지점
img.shape[1]//4 : 3*img.shape[1]//4, :])

cv.imshow('R Channel', img[:,:,2])
cv.imshow('G Channel', img[:,:,1])
cv.imshow('B Channel', img[:,:,0])

cv.waitKey()
cv.destroyAllWindows()