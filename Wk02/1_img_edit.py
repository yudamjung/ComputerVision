import cv2 as cv
import sys

img=cv.imread('soccer.jpg')

if img is None:
    sys.exit('파일을 찾을 수 없습니다.')
    
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)  #BGR 컬러 영상을 명암 영상으로 변환
gray_resize = cv.resize(gray, dsize=(0,0), fx=0.5, fy=0.5)  # 반으로 축소

cv.imwrite('soccer_gray.png', gray) # 영상을 파일에 저장
cv.imwrite('soccer_gray_resize.png', gray_resize)

cv.imshow('Color image', img)
cv.imshow('Gray image', gray)
cv.imshow('Gray image small', gray_resize)

cv.waitKey(0)
cv.destroyAllWindows()
cv.waitKey(30)


"""
2차원 회색조 이미지
gray.shape
Out[10]: (948, 1434)

gray_resize.shape
Out[11]: (474, 717) -> 절반으로 줄어듦을 확인 ☑️

print(gray[0,0])
109
"""