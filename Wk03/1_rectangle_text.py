"""
컴퓨터비전과 딥러닝 교재 66pg
[프로그래밍 2-6] 영상에 도형을 그리고 글자 쓰기
"""
import cv2 as cv
import sys

img = cv.imread('girl_laughing.jpg')

if img is None:
    sys.exit('파일을 찾을 수 없습니다.')
    
"""
print(help(cv.rectangle))
print()
print(help(cv.putText))
print()
"""

cv.rectangle(img, (830,30), (1000,200), (0,0,255), 2)  # 직사각형 그리기
"""
img : 직사각형을 그릴 영상
(830,30), (1000,200) : 직사각형의 왼쪽 위, 오른쪽 아래 좌표 (x좌표, y좌표)
(0,0,255) : (B, G, R) 빨간색
2 : 선의 두께
"""
cv.putText(img, 'laugh', (830,24), cv.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
"""
img — Image
text — Text string to be drawn.
org — Bottom-left/Top-left corner of the text string in the image.
fontHeight — Drawing font size by pixel unit.
color — Text color.
thickness — Thickness of the lines used to draw a text when negative, the glyph is filled. Otherwise, the glyph is drawn with this thickness.
line_type — Line type.
bottomLeftOrigin — When true, the image data origin is at the bottom-left corner. Otherwise, it is at the top-left corner.
"""

cv.imshow('Draw', img)

cv.waitKey()
cv.destroyAllWindows()