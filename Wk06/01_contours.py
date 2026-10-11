import skimage
import numpy as np
import cv2 as cv

original = skimage.data.horse()
img = 255 - np.uint8(original) * 255
cv.imshow('Horse', img)

contours, hierarchy = cv.findContours(
	img,
	cv.RETR_EXTERNAL,
	cv.CHAIN_APPROX_NONE
)
"""
contours : 검출된 모든 컨투어의 좌표 정보 저장
hierarchy : 컨투어 사이의 계층 관계를 나타내는 배열

cv.findContours()는 이진 이미지에서 물체의 외곽선을 찾아 반환
cv.findContours(imgae, mode, method)

cv.RETR_EXTERNAL : 가장 바깥쪽 컨투어만 검출
cv.CHAIN_APPROX_NONE : 컨투어를 구성하는 경계점들을 모두 저장
"""

# 흑백 이미지를 BGR로 변환
img2 = cv.cvtColor(img, cv.COLOR_GRAY2BGR)

# 컨투어 그리기
# cv.drawContours(이미지, 물체테두리, contourIdx, 선 색상, 선 굵기)
# contourIdx == -1 => 모든 컨투어 선택
# 2px의 분홍색 선이 그려질 것
cv.drawContours(img2, contours, -1, (255, 0, 255), 2)
cv.imshow('Horse with contour', img2)

# 검출된 컨투어 중 첫 번째 컨투어
contour = contours[0]

# 물체의 면적/무게중심 같은 기하학적 특징을 계산하는데 필요한 값들의 집합
# 계산 결과는 딕셔너리 형태로 반환
"""
m00 : 물체의 면적에 해당하는 0차 공간 모멘트
m10 : x좌표에 대한 1차 공간 모멘트
m01 : y좌표에 대한 1차 공간 모멘트
-> 이 값들을 이용하면 물체의 무게중심 계산이 가능하다.
"""
m = cv.moments(contour)

# 컨투어가 둘러싸고 있는 영역의 면적 계산
area = cv.contourArea(contour)

# 무게 중심 (Centroid)
cx, cy = m['m10']/m['m00'], m['m01']/m['m00']

# 둘레
# cv.arcLength(curve, closed)
# cv.arcLength(길이를 계산할 컨투어, 폐곡선 여부)
# closed=True 면 마지막 점과 첫번재 점을 연결하는 길이까지 포함하여 계산
perimeter = cv.arcLength(contour, True)

# 원형도 - 물체가 얼마나 원에 가까운 형태인지 계산
# 원형도 계산법 : 4 * 물체 면적 * 파이 / (둘레)^2
# 원형도가 1에 가까울수록 원에 가깝다
roundness = (4.0 * np.pi * area) / (perimeter * perimeter)
print(f'면적 = {area} \n중점 = ({cx}, {cy}) \n둘레 = {perimeter} \n둥근 정도 = {roundness}')

# 컬러 디스플레이용 영상
img3 = cv.cvtColor(img, cv.COLOR_GRAY2BGR)

# 다각형 근사
contour_approx = cv.approxPolyDP(contour, 8, True)
# aPDP(curve, epsilon, closed)
# curve -> 단순화할 원본 컨투어
# epsilon -> 근사 오차의 최대 허용 거리 (외곽선을 얼마나 단순하게 바꿔도 괜찮은지 결정)
# closed -> 폐곡선 True / 뚫린 곡선 False
cv.drawContours(img3, [contour_approx], -1, (0, 255, 0), 2)

# Convex Hull
# 물체를 구성하는 모든 점을 포함하는 가장 작은 볼록 다각형
# cv.convexHull(points)
# 입력 : 컨투어의 점 좌표
# 반환 : 볼록 껍질을 구성하는 점 좌표 배열 -> (점의 개수, 1, 2)
hull = cv.convexHull(contour)
hull = hull.reshape(1, hull.shape[0], hull.shape[2])
"""
hull.reshape(
	첫번째 차원 크기를 1로 지정, 
	볼록 껍질 구성 점의 개수, 
	x,y좌표개수인 2
)
"""
# 볼록 껍질 그리기
cv.drawContours(img3, hull, -1, (0, 0, 255), 2)

cv.imshow('Horse with line segments and convex hull', img3)

cv.waitKey()
cv.destroyAllWindows()