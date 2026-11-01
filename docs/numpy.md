<a id="numpy-함수-레퍼런스"></a>
# NumPy 함수 레퍼런스

> 대상 버전: **NumPy 2.4.6** (`import numpy as np`)
> 공식 문서: <https://numpy.org/doc/stable/reference/>
> OpenCV 영상은 모두 NumPy 배열(`ndarray`)이라, 영상을 자르고 만들고 고치는 일은 대부분 NumPy로 합니다.

[← 전체 목차로](README.md)

## 목차

- [배열 인덱싱·슬라이싱 (영상 자르기, 채널 분리)](#np-ndarray-slicing)
- [`.shape` — 영상 크기 확인](#np-shape)
- [`np.uint8` / `np.float32` / `np.float64` — 자료형 변환](#np-uint8)
- [`np.zeros` — 0으로 채운 배열 (마스크·모델 배열)](#np-zeros)
- [`np.empty` — 초기화 안 된 배열 (캔버스)](#np-empty)
- [`np.copy` — 영상 복사](#np-copy)
- [`np.where` — 조건으로 값 고르기](#np-where)
- [`.astype` — 자료형 바꾸기](#np-astype)
- [`np.newaxis` — 축 추가 (마스크 브로드캐스팅)](#np-newaxis)
- [`np.unique` — 고유값 (영역 개수 세기)](#np-unique)
- [`.reshape` — 모양 바꾸기](#np-reshape)
- [`.max()` — 최댓값](#np-max)
- [불리언 인덱싱 — 조건에 맞는 화소만 바꾸기](#np-boolean-index)
- [`np.pi`](#np-pi)

---

<a id="np-ndarray-slicing"></a>
## 배열 인덱싱·슬라이싱 (영상 자르기, 채널 분리)

공식 문서: <https://numpy.org/doc/stable/user/basics.indexing.html>

```python
img[행_시작:행_끝, 열_시작:열_끝, 채널]
```

- 영상 배열의 축 순서는 **(행=y, 열=x, 채널)** 입니다. `[y, x]` 순서임에 주의 (OpenCV 함수의 좌표 `(x, y)`와 반대).
- 슬라이싱 결과는 **복사본이 아니라 뷰(view)** 입니다. 잘라낸 영역에 그리면 원본도 바뀝니다.
- `img[:, :, 0]` = B, `img[:, :, 1]` = G, `img[:, :, 2]` = R (OpenCV는 BGR), PNG를 `IMREAD_UNCHANGED`로 읽으면 `[:, :, 3]` = 알파.

**프로젝트 사용례**

```python
# Wk03/5_img_slicing.py — 왼쪽 위 1/4, 가운데 절반
img[0:img.shape[0]//2, :img.shape[1]//2, :]
img[img.shape[0]//4 : 3*img.shape[0]//4, img.shape[1]//4 : 3*img.shape[1]//4, :]

# Wk03/5_img_slicing.py — 채널 분리
cv.imshow('R Channel', img[:, :, 2])

# Wk04/1.py — 알파 채널로 이진화
cv.threshold(img[:, :, 3], 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

# Wk07/02_FLANN.py — 관심 영역(ROI)만 잘라 매칭에 사용
img1 = cv.imread('mot_color70.jpg')[190:350, 440:560]
```

<a id="np-shape"></a>
## `.shape` — 영상 크기 확인

공식 문서: <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.shape.html>

```python
img.shape   # 컬러: (높이, 너비, 채널), 회색조: (높이, 너비)
```

```python
# Wk02/1_img_edit.py
gray.shape          # (948, 1434)
gray_resize.shape   # (474, 717)

# Wk09/02_VisionAgent02.py
h1, w1 = self.signImgs[best].shape[0], self.signImgs[best].shape[1]
```

<a id="np-uint8"></a>
## `np.uint8` / `np.float32` / `np.float64` — 자료형 변환

공식 문서: <https://numpy.org/doc/stable/user/basics.types.html>

`np.uint8(x)`처럼 자료형 이름을 함수처럼 호출하면 그 자료형의 배열로 변환합니다.

| 자료형 | 범위 | 용도 |
|---|---|---|
| `uint8` | 0 ~ 255 정수 | 일반 영상, 마스크, 구조 요소 |
| `float32` | 실수 | `cornerHarris` 입력, SIFT 기술자 |
| `float64` | 실수 | `grabCut` 모델 배열 |

```python
# Wk04/1.py — 구조 요소
se = np.uint8([[0,0,1,0,0], [0,1,1,1,0], [1,1,1,1,1], [0,1,1,1,0], [0,0,1,0,0]])

# Wk05/01_slic.py — skimage의 0~1 실수 결과를 0~255 영상으로
sp_img1 = np.uint8(sp_img1 * 255.0)

# Wk06/01_contours.py — bool 영상 → 0/1 → 0/255 → 반전
img = 255 - np.uint8(original) * 255

# Wk06/02_Harris_Corner.py
gray = np.float32(gray)
```

> `uint8`은 범위를 넘으면 **잘리지 않고 순환(overflow)** 합니다: `np.uint8(250) + np.uint8(10) == 4`. 밝기 덧셈은 `cv.add`(포화 연산)를 쓰거나 `np.clip`으로 처리하세요.

<a id="np-zeros"></a>
## `np.zeros` — 0으로 채운 배열

공식 문서: <https://numpy.org/doc/stable/reference/generated/numpy.zeros.html>

```python
np.zeros(shape, dtype=float, order='C') -> ndarray
```

```python
# Wk05/03_grab_cut.py, Wk09/01_Orim.py — 영상과 같은 크기의 1채널 마스크
mask = np.zeros((img.shape[0], img.shape[1]), np.uint8)
mask[:, :] = cv.GC_PR_BGD          # 전체 값을 2로

# grabCut 내부 모델용 배열 (크기 1x65 고정)
background = np.zeros((1, 65), np.float64)
```

> 같은 모양을 간단히: `np.zeros(img.shape[:2], np.uint8)` 또는 `np.full(img.shape[:2], cv.GC_PR_BGD, np.uint8)`.

<a id="np-empty"></a>
## `np.empty` — 초기화하지 않은 배열

공식 문서: <https://numpy.org/doc/stable/reference/generated/numpy.empty.html>

```python
np.empty(shape, dtype=float, order='C') -> ndarray
```

값을 0으로 채우지 않아 빠르지만 **쓰레기 값**이 들어 있습니다. 곧바로 전부 덮어쓸 배열에만 사용하세요.

```python
# Wk07/02_FLANN.py — drawMatches가 그려 넣을 캔버스 (두 영상을 가로로 이어 붙인 크기)
img_match = np.empty((max(img1.shape[0], img2.shape[0]),
                      img1.shape[1] + img2.shape[1], 3), dtype=np.uint8)
```

<a id="np-copy"></a>
## `np.copy` — 배열 복사

공식 문서: <https://numpy.org/doc/stable/reference/generated/numpy.copy.html>

```python
np.copy(a) -> ndarray      # img.copy() 와 같음
```

OpenCV 그리기 함수는 영상을 직접 수정하므로, **원본을 지키려면 복사본에 그려야** 합니다.

```python
# Wk05/03_grab_cut.py, Wk09/01_Orim.py — 붓질은 복사본에, grabCut은 깨끗한 원본으로
img_show = np.copy(img)
```

<a id="np-where"></a>
## `np.where` — 조건으로 값 고르기

공식 문서: <https://numpy.org/doc/stable/reference/generated/numpy.where.html>

```python
np.where(condition, x, y) -> ndarray     # 조건이 참이면 x, 거짓이면 y
```

```python
# Wk05/03_grab_cut.py — 배경(0, 2)은 0, 전경(1, 3)은 1
mask2 = np.where((mask == cv.GC_BGD) | (mask == cv.GC_PR_BGD), 0, 1).astype('uint8')
```

> 여러 조건은 `and/or`가 아니라 **`&`, `|`** 를 쓰고 각 조건을 **괄호로 감싸야** 합니다.

<a id="np-astype"></a>
## `.astype` — 자료형 바꾸기

공식 문서: <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.astype.html>

```python
arr.astype(dtype) -> ndarray     # 새 배열 반환
```

```python
mask2 = np.where(..., 0, 1).astype('uint8')   # 정수(int64) → uint8
```

<a id="np-newaxis"></a>
## `np.newaxis` — 축 추가

공식 문서: <https://numpy.org/doc/stable/reference/constants.html#numpy.newaxis>

`None`과 같으며, 인덱싱 자리에 넣으면 길이 1인 축이 생깁니다. 브로드캐스팅으로 **2차원 마스크를 3채널 영상에 곱할 때** 사용합니다.

```python
# Wk05/03_grab_cut.py — (H, W) 마스크 → (H, W, 1) → (H, W, 3) 영상과 곱셈 가능
grab = img * mask2[:, :, np.newaxis]
```

<a id="np-unique"></a>
## `np.unique` — 고유값

공식 문서: <https://numpy.org/doc/stable/reference/generated/numpy.unique.html>

```python
np.unique(ar, return_counts=False, ...) -> ndarray
```

```python
# Wk05/02_normalized_cut.py — 정규화 절단으로 나뉜 영역 개수
print('분리된 영역의 개수: ', np.unique(ncut).size)
```

<a id="np-reshape"></a>
## `.reshape` — 모양 바꾸기

공식 문서: <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.reshape.html>

```python
# Wk06/01_contours.py — convexHull 결과 (N,1,2) → (1,N,2)
hull = hull.reshape(1, hull.shape[0], hull.shape[2])
```

<a id="np-max"></a>
## `.max()` — 최댓값

공식 문서: <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.max.html>

```python
# Wk06/02_Harris_Corner.py — 최대 응답의 5%를 임계값으로
img[dist > 0.05 * dist.max()] = [0, 0, 255]
```

<a id="np-boolean-index"></a>
## 불리언 인덱싱 — 조건에 맞는 화소만 바꾸기

공식 문서: <https://numpy.org/doc/stable/user/basics.indexing.html#boolean-array-indexing>

같은 모양의 불리언 배열로 인덱싱하면 `True`인 위치만 선택됩니다.

```python
# Wk06/02_Harris_Corner.py — 코너 응답이 큰 화소를 빨간색(BGR)으로 칠하기
img[dist > 0.05 * dist.max()] = [0, 0, 255]
```

<a id="np-pi"></a>
## `np.pi`

원주율 상수 π.

```python
roundness = (4.0 * np.pi * area) / (perimeter * perimeter)   # Wk06/01_contours.py
```

[↑ 맨 위로](#numpy-함수-레퍼런스) · [← 전체 목차로](README.md)
