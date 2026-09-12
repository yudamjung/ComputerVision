"""
컴퓨터비전과 딥러닝 교재 70pg
[프로그래밍 2-8] 마우스 드래그로 직사각형 그리기
"""
import cv2 as cv
import sys

img=cv.imread('girl_laughing.jpg')

if img is None:
    sys.exit('파일을 찾을 수 없습니다.')
    
def draw (event, x, y, flags, param):
    global ix, iy
    
    if event == cv.EVENT_LBUTTONDOWN:
        ix, iy = x, y                                   # 마우스 왼쪽 버튼 클릭 시 초기 위치 저장
    elif event == cv.EVENT_LBUTTONUP:
        cv.rectangle(img, (ix,iy), (x,y), (0,0,255), 2) # 마우스 왼쪽 버튼 놓았을 때 직사각형 그리기
        
    cv. imshow('Drawing', img)
    
cv.namedWindow('Drawing')
cv.imshow('Drawing', img)

cv.setMouseCallback('Drawing', draw)

while(True):
    if cv.waitKey(1)==ord('q'):
        cv.destroyAllWindows()
        break