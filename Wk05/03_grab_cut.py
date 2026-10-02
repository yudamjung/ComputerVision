import cv2 as cv
import numpy as np
import sys


img = cv.imread('soccer.jpg')

if img is None:
    sys.exit('파일을 찾을 수 없습니다.')

img_show = np.copy(img)

mask = np.zeros((img.shape[0], img.shape[1]), np.uint8)
mask[:,:] = cv.GC_PR_BGD

BrushSize = 9
LColor = (255,0,0)      # 마우스 좌클릭 시 파란 붓 (물체)
RColor = (0,0,255)      # 마우스 우클릭 시 빨간 붓 (배경)

def painting (e, x, y, flags, param):
    if e == cv.EVENT_LBUTTONDOWN:
        cv.circle(img_show, (x, y), BrushSize, LColor, -1)      # 좌클릭 시 파란 붓
        cv.circle(mask, (x, y), BrushSize, cv.GC_FGD, -1)

    elif e == cv.EVENT_MOUSEMOVE and flags == cv.EVENT_FLAG_LBUTTON:
        cv.circle(img_show, (x, y), BrushSize, LColor, -1)
        cv.circle(mask, (x, y), BrushSize, cv.GC_FGD, -1)

    elif e == cv.EVENT_RBUTTONDOWN:
        cv.circle(img_show, (x, y), BrushSize, RColor, -1)
        cv.circle(mask, (x, y), BrushSize, cv.GC_BGD, -1)

    elif e == cv.EVENT_MOUSEMOVE and flags == cv.EVENT_FLAG_RBUTTON:
        cv.circle(img_show, (x, y), BrushSize, RColor, -1)
        cv.circle(mask, (x, y), BrushSize, cv.GC_BGD, -1)

    cv.imshow('Painting', img_show)

cv.namedWindow('Painting')
cv.imshow('Painting', img_show)
cv.setMouseCallback('Painting', painting)

while(True):
    """
    if cv.waitKey(1) & 0xFF == ord('q'):
        cv.destroyWindow('Painting')
        break
    """
    key = cv.waitKey(1) & 0xFF
    if key in (ord('q'), 66):
        cv.destroyWindow('Painting')
        break

background = np.zeros((1,65), np.float64)
foreground = np.zeros((1,65), np.float64)

cv.grabCut(img, mask, None, background, foreground, 5, cv.GC_INIT_WITH_MASK)
# 수정: assert np.any(mask == cv.GC_FGD) and np.any(mask == cv.GC_BGD), "좌클릭(물체)과 우클릭(배경)을 각각 표시한 뒤 q를 누르세요"; cv.grabCut(img, mask, None, background, foreground, 5, cv.GC_INIT_WITH_MASK)
mask2 = np.where((mask == cv.GC_BGD) | (mask == cv.GC_PR_BGD), 0, 1). astype('uint8')
grab = img * mask2[:,:,np.newaxis]
cv.imshow('Grab Cut Image', grab)

cv.waitKey()
cv.destroyAllWindows()
