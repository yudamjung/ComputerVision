"""
컴퓨터비전과 딥러닝 교재 71pg
[프로그래밍 2-9] 빨간색 붓과 파란색 붓으로 페인팅하기
"""
import cv2 as cv
import sys

img = cv.imread('soccer.jpg')

if img is None:
    sys.exit('파일을 찾을 수 없습니다.')
    
BrushSiz = 5                            # 붓의 크기
LColor, RColor = (255,0,0), (0,0,255)   # 파랑, 빨강

def painting (event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        cv.circle(img, (x,y), BrushSiz, LColor, -1)                         # 왼쪽 버튼 클릭하면 파랑
    elif event == cv.EVENT_RBUTTONDOWN:
        cv.circle(img, (x,y), BrushSiz, RColor, -1)                         # 오른쪽 버튼 클릭하면 빨강
    elif event == cv.EVENT_MOUSEMOVE and flags == cv.EVENT_FLAG_LBUTTON:
        cv.circle(img, (x,y), BrushSiz, LColor, -1)                         # 왼쪽 버튼 클릭하고 이동하면 파랑
    elif event == cv.EVENT_MOUSEMOVE and flags == cv.EVENT_FLAG_RBUTTON:
        cv.circle(img, (x,y), BrushSiz, RColor, -1)                         # 오른쪽 버튼 클릭하고 이동하면 빨강
        
    cv.imshow('Painting', img)                                              # 수정된 영상을 다시 그림
    
cv.namedWindow('Painting')
cv.imshow('Painting', img)

cv.setMouseCallback('Painting', painting)

while(True):
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break