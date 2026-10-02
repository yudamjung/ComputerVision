import skimage
import numpy as np
import cv2 as cv
import time

coffee = skimage.data.coffee()

start = time.time()
slic = skimage.segmentation.slic(coffee, compactness=20, n_segments=600, start_label=1)
g = skimage.graph.rag_mean_color(coffee, slic, mode='similarity')

"""
`rag_mean_color` -> 영역 인접 그래프를 만들고
평균 색상이 비슷한 인접 영역들을 병합하여
이미지 분할(segmentation) 수행하는 데 사용
"""

# 정규화 절단 알고리즘 수행 부분 👇
ncut = skimage.graph.cut_normalized(slic, g)

# 정규화 절단 알고리즘 수행 소요시간 계산
print(coffee.shape, 'Coffee 영상을 분할하는 데 ', time.time() - start, '초 소요')

marking = skimage.segmentation.mark_boundaries(coffee, ncut)
ncut_coffee = np.uint8(marking * 255.0)

cv.imshow('Normalized Cut', cv.cvtColor(ncut_coffee, cv.COLOR_RGB2BGR))

# 결과 : 다소 과잉 분해된 모습.

# 몇 개의 영역으로 분할되었는지 확인하기
print('분리된 영역의 개수: ', np.unique(ncut).size)

cv.waitKey()
cv.destroyAllWindows()