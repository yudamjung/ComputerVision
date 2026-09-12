"""
컴퓨터비전과 딥러닝 교재 68pg
[프로그래밍 2-7] 마우스로 클릭한 곳에 직사각형 그리기
"""
import cv2 as cv
import sys

img = cv.imread('girl_laughing.jpg')

if img is None:
    sys.exit('파일을 찾을 수 없습니다.')
    
def draw(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:                           # 마우스 왼쪽 버튼 클릭이면
        cv.rectangle(img, (x,y), (x+200,y+200), (0,0,255), 2)   # 빨간 (200,200) 네모 그리기
    elif event == cv.EVENT_RBUTTONDOWN:                         # 마우스 오른쪽 버튼 클릭이면
        cv.rectangle(img, (x,y), (x+100,y+100), (255,0,0), 2)   # 파란 (100,100) 네모 그리기
        
    cv.imshow('Drawing', img)
    
cv.namedWindow('Drawing')
cv.imshow('Drawing', img)

cv.setMouseCallback('Drawing', draw)    # Drawing 윈도우에 draw 콜백 함수 지정

while(True):                            # 마우스 이벤트가 언제 발생할지 모르므로 무한 반복
    if cv.waitKey(1)==ord('q'):
        cv.destroyAllWindows()
        break