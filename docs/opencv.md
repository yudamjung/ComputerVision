<a id="opencv-cv2-함수-레퍼런스"></a>
# OpenCV (`cv2`) 함수 레퍼런스

> 대상 버전: **opencv-python 5.0.0** (`import cv2 as cv`)
> 시그니처는 설치된 OpenCV의 공식 docstring(`help(cv.함수명)`)으로 확인했습니다. 이 docstring은 공식 문서(docs.opencv.org)와 같은 소스에서 생성됩니다.
> 표기법: `func(a, b[, c[, d]]) -> 반환값` 에서 `[ ]` 안은 생략 가능한 인자입니다.

[← 전체 목차로](README.md)

## 목차

1. [영상 입출력 (imgcodecs)](#1-영상-입출력-imgcodecs)
   - [cv.imread](#cv-imread) · [cv.imwrite](#cv-imwrite)
2. [창·키보드·마우스 (HighGUI)](#2-창키보드마우스-highgui)
   - [cv.imshow](#cv-imshow) · [cv.waitKey](#cv-waitkey) · [cv.destroyAllWindows](#cv-destroyallwindows) · [cv.destroyWindow](#cv-destroywindow) · [cv.namedWindow](#cv-namedwindow) · [cv.setMouseCallback](#cv-setmousecallback) · [마우스 이벤트 상수](#cv-mouse-events)
3. [색 변환·크기 변환](#3-색-변환크기-변환)
   - [cv.cvtColor](#cv-cvtcolor) · [cv.resize](#cv-resize)
4. [도형·글자 그리기](#4-도형글자-그리기)
   - [cv.rectangle](#cv-rectangle) · [cv.circle](#cv-circle) · [cv.putText](#cv-puttext)
5. [이진화·모폴로지](#5-이진화모폴로지)
   - [cv.threshold (오츄)](#cv-threshold) · [cv.dilate](#cv-dilate) · [cv.erode](#cv-erode) · [열림/닫힘 조합](#cv-morph-combo)
6. [히스토그램](#6-히스토그램)
   - [cv.calcHist](#cv-calchist) · [cv.equalizeHist](#cv-equalizehist)
7. [영역 분할](#7-영역-분할)
   - [cv.grabCut](#cv-grabcut)
8. [컨투어(외곽선)·모양 분석](#8-컨투어외곽선모양-분석)
   - [cv.findContours](#cv-findcontours) · [cv.drawContours](#cv-drawcontours) · [cv.moments](#cv-moments) · [cv.contourArea](#cv-contourarea) · [cv.arcLength](#cv-arclength) · [cv.approxPolyDP](#cv-approxpolydp) · [cv.convexHull](#cv-convexhull)
9. [코너·특징점·매칭](#9-코너특징점매칭)
   - [cv.cornerHarris](#cv-cornerharris) · [cv.SIFT_create](#cv-sift-create) · [detectAndCompute](#cv-detectandcompute) · [cv.drawKeypoints](#cv-drawkeypoints) · [cv.DescriptorMatcher_create](#cv-descriptormatcher-create) · [knnMatch](#cv-knnmatch) · [DMatch 객체](#cv-dmatch) · [cv.drawMatches](#cv-drawmatches)

---

<a id="1-영상-입출력-imgcodecs"></a>
## 1. 영상 입출력 (imgcodecs)

공식 문서: <https://docs.opencv.org/4.x/d4/da8/group__imgcodecs.html>

<a id="cv-imread"></a>
### `cv.imread` — 파일에서 영상 읽기

```python
cv.imread(filename[, flags]) -> retval
```

파일을 읽어 NumPy 배열(`ndarray`)로 돌려줍니다. **파일이 없거나 형식이 잘못되면 예외 대신 `None`을 반환**하므로 반드시 `None` 검사를 해야 합니다.

| 인자 | 의미 |
|---|---|
| `filename` | 읽을 파일 경로 (실행 위치 기준 상대 경로 주의) |
| `flags` | 읽기 방식. 기본값 `cv.IMREAD_COLOR`(BGR 3채널) |

자주 쓰는 `flags`

| 상수 | 결과 |
|---|---|
| `cv.IMREAD_COLOR` (기본) | 3채널 **B, G, R 순서** 컬러 영상 |
| `cv.IMREAD_GRAYSCALE` | 1채널 명암 영상 |
| `cv.IMREAD_UNCHANGED` | 원본 그대로(PNG의 **알파 채널 포함 4채널**) |

- 반환 배열 모양: 컬러 `(높이, 너비, 3)`, 명암 `(높이, 너비)`, dtype은 보통 `uint8`.
- 파일 형식은 확장자가 아니라 **파일 내용**으로 판단합니다.

**프로젝트 사용례**

```python
# Wk02/1_img_edit.py
img = cv.imread('soccer.jpg')
if img is None:
    sys.exit('파일을 찾을 수 없습니다.')

# Wk04/1.py — 4채널 PNG의 알파 채널까지 읽기
img = cv.imread('JohnHancocksSignature.png', cv.IMREAD_UNCHANGED)
print(img.shape)        # (높이, 너비, 4)

# Wk07/02_FLANN.py — 읽자마자 슬라이싱으로 일부 영역만 사용
img1 = cv.imread('mot_color70.jpg')[190:350, 440:560]
```

> 주의: `cv.imread(...)[190:350, ...]`처럼 바로 슬라이싱하면, 파일이 없을 때 `None[...]` 이 되어 `TypeError`가 납니다.

---

<a id="cv-imwrite"></a>
### `cv.imwrite` — 영상을 파일로 저장

```python
cv.imwrite(filename, img[, params]) -> retval
```

| 인자 | 의미 |
|---|---|
| `filename` | 저장 경로. **확장자로 저장 형식이 결정됨** (`.png`, `.jpg` …) |
| `img` | 저장할 배열 (8비트 1/3/4채널이 일반적) |
| `params` | 형식별 옵션. 예: `[cv.IMWRITE_JPEG_QUALITY, 90]` |

반환값: 성공하면 `True`. 확장자가 없거나 잘못된 경로면 예외 또는 `False`.

**프로젝트 사용례**

```python
# Wk02/1_img_edit.py
cv.imwrite('soccer_gray.png', gray)

# Wk09/01_Orim.py — 파일 대화상자로 받은 경로에 저장
fname = QFileDialog.getSaveFileName(self, '파일 저장', './')
cv.imwrite(fname[0], self.grabImg)
```

---

<a id="2-창키보드마우스-highgui"></a>
## 2. 창·키보드·마우스 (HighGUI)

공식 문서: <https://docs.opencv.org/4.x/d7/dfc/group__highgui.html>

<a id="cv-imshow"></a>
### `cv.imshow` — 창에 영상 표시

```python
cv.imshow(winname, mat) -> None
```

| 인자 | 의미 |
|---|---|
| `winname` | 창 이름(문자열). **같은 이름이면 같은 창을 갱신** |
| `mat` | 표시할 영상 |

공식 문서 요약:
- 창이 없으면 `WINDOW_AUTOSIZE` 창을 자동으로 만듭니다.
- 자료형에 따라 화면 값이 바뀝니다: `uint8`은 그대로, `uint16`은 256으로 나눔, **`float32/float64`는 255를 곱함**(즉 0~1 범위를 가정).
- **반드시 뒤에 `cv.waitKey()`(또는 `pollKey`)를 호출해야** 창이 실제로 그려지고 반응합니다.

**프로젝트 사용례**

```python
# Wk02/1_img_edit.py — 슬라이싱 결과를 바로 표시
cv.imshow('Center Half',
          img[img.shape[0]//4 : 3*img.shape[0]//4,
              img.shape[1]//4 : 3*img.shape[1]//4, :])

# Wk03/5_img_slicing.py — 채널 하나만 보면 명암 영상처럼 보임
cv.imshow('R Channel', img[:, :, 2])

# Wk05/01_slic.py — skimage 결과(RGB)는 BGR로 바꿔서 표시
cv.imshow('Coffee image', cv.cvtColor(img, cv.COLOR_RGB2BGR))
```

> 이 때문에 skimage의 `mark_boundaries` 결과(0~1 float)를 `np.uint8(x * 255.0)`으로 변환한 뒤 표시합니다. ([scikit-image 문서](scikit-image.md#sk-mark-boundaries) 참고)

---

<a id="cv-waitkey"></a>
### `cv.waitKey` — 키 입력 대기 + GUI 이벤트 처리

```python
cv.waitKey([, delay]) -> retval
```

| 인자 | 의미 |
|---|---|
| `delay` | 대기 시간(ms). **0 이하이면 키를 누를 때까지 무한 대기**, 양수면 그 시간만큼 대기 |

- 반환값: 눌린 키의 코드, 시간 안에 안 눌렸으면 **`-1`**.
- 공식 문서: `waitKey`/`pollKey`는 HighGUI에서 **GUI 이벤트를 처리하는 유일한 함수**이므로, 창을 띄운 프로그램은 주기적으로 호출해야 합니다.
- 창이 하나 이상 있고 활성화되어 있어야 동작합니다.

**프로젝트 사용례**

```python
# Wk02 — 아무 키나 누를 때까지 대기
cv.waitKey(0)

# Wk03/2_click_rectangle.py — 마우스 이벤트를 받기 위한 무한 루프, q 누르면 종료
while True:
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

# Wk05/03_grab_cut.py — 하위 8비트만 비교(플랫폼 호환), q 또는 'B'(66)로 종료
key = cv.waitKey(1) & 0xFF
if key in (ord('q'), 66):
    ...
```

> `& 0xFF`: 일부 환경에서 waitKey가 상위 비트가 섞인 값을 돌려주기 때문에 하위 8비트만 남기는 관용구입니다. `66`은 대문자 `'B'`의 코드입니다.

---

<a id="cv-destroyallwindows"></a>
### `cv.destroyAllWindows` — 모든 HighGUI 창 닫기

```python
cv.destroyAllWindows() -> None
```

모든 OpenCV 창을 닫습니다. macOS 등에서는 창이 바로 사라지지 않을 수 있어 `Wk02/1_img_edit.py`처럼 뒤에 `cv.waitKey(30)`을 한 번 더 호출해 이벤트를 처리하게 하기도 합니다.

```python
# Wk09/01_Orim.py — Qt 종료 버튼에서 OpenCV 창도 함께 정리
def quitFunction(self):
    cv.destroyAllWindows()
    self.close()
```

<a id="cv-destroywindow"></a>
### `cv.destroyWindow` — 특정 창 하나만 닫기

```python
cv.destroyWindow(winname) -> None
```

```python
# Wk05/03_grab_cut.py — 페인팅 창만 닫고 결과 창은 새로 띄움
cv.destroyWindow('Painting')
```

---

<a id="cv-namedwindow"></a>
### `cv.namedWindow` — 이름 있는 창 미리 만들기

```python
cv.namedWindow(winname[, flags]) -> None
```

| `flags` | 의미 |
|---|---|
| `cv.WINDOW_AUTOSIZE` (기본) | 영상 크기에 맞춰 고정, 사용자가 크기 조절 불가 |
| `cv.WINDOW_NORMAL` | 사용자가 크기 조절 가능 (화면보다 큰 영상 볼 때) |

`setMouseCallback`은 **이미 존재하는 창**에만 연결할 수 있으므로, 콜백 등록 전에 창을 만들어 두는 용도로 씁니다.

```python
# Wk03/2_click_rectangle.py
cv.namedWindow('Drawing')
cv.imshow('Drawing', img)
cv.setMouseCallback('Drawing', draw)
```

---

<a id="cv-setmousecallback"></a>
### `cv.setMouseCallback` — 창에 마우스 콜백 함수 연결

```python
cv.setMouseCallback(windowName, onMouse[, param]) -> None
```

| 인자 | 의미 |
|---|---|
| `windowName` | 콜백을 붙일 창 이름 |
| `onMouse` | `def f(event, x, y, flags, param)` 형태의 함수 |
| `param` | 콜백에 그대로 전달할 임의 데이터 (선택) |

콜백 인자:
- `event`: 무슨 일이 일어났는지 ([마우스 이벤트 상수](#cv-mouse-events))
- `x, y`: 창 안의 좌표 (x=열, y=행)
- `flags`: 이벤트 순간 눌려 있는 버튼/키 상태 (비트 플래그)
- `param`: 등록 시 넘긴 값

**프로젝트 사용례**

```python
# Wk03/3_drag_rectangle.py — 누른 위치를 기억했다가 뗄 때 사각형
def draw(event, x, y, flags, param):
    global ix, iy
    if event == cv.EVENT_LBUTTONDOWN:
        ix, iy = x, y
    elif event == cv.EVENT_LBUTTONUP:
        cv.rectangle(img, (ix, iy), (x, y), (0, 0, 255), 2)
    cv.imshow('Drawing', img)

cv.setMouseCallback('Drawing', draw)

# Wk09/01_Orim.py — 클래스의 메서드도 콜백으로 등록 가능 (self는 자동 바인딩)
cv.setMouseCallback('Painting', self.painting)
```

<a id="cv-mouse-events"></a>
#### 마우스 이벤트 / 플래그 상수

| `event` 상수 | 값 | 의미 |
|---|---|---|
| `cv.EVENT_MOUSEMOVE` | 0 | 마우스 이동 |
| `cv.EVENT_LBUTTONDOWN` | 1 | 왼쪽 버튼 누름 |
| `cv.EVENT_RBUTTONDOWN` | 2 | 오른쪽 버튼 누름 |
| `cv.EVENT_LBUTTONUP` | 4 | 왼쪽 버튼 뗌 |
| `cv.EVENT_RBUTTONUP` | 5 | 오른쪽 버튼 뗌 |
| `cv.EVENT_LBUTTONDBLCLK` | 7 | 왼쪽 더블클릭 |

| `flags` 상수 | 값 | 의미 |
|---|---|---|
| `cv.EVENT_FLAG_LBUTTON` | 1 | 왼쪽 버튼이 눌린 상태 |
| `cv.EVENT_FLAG_RBUTTON` | 2 | 오른쪽 버튼이 눌린 상태 |
| `cv.EVENT_FLAG_CTRLKEY` | 8 | Ctrl 누른 상태 |
| `cv.EVENT_FLAG_SHIFTKEY` | 16 | Shift 누른 상태 |

**드래그 = `MOUSEMOVE` + 버튼 플래그** 조합입니다.

```python
# Wk03/4_click_paint.py — 누른 채 움직이면 계속 칠하기
elif event == cv.EVENT_MOUSEMOVE and flags == cv.EVENT_FLAG_LBUTTON:
    cv.circle(img, (x, y), BrushSiz, LColor, -1)
```

> 팁: `flags`는 비트 조합이라 Ctrl을 같이 누르면 `1 | 8 = 9`가 되어 `==` 비교가 실패합니다. 더 견고하게 하려면 `flags & cv.EVENT_FLAG_LBUTTON`으로 검사하세요.

---

<a id="3-색-변환크기-변환"></a>
## 3. 색 변환·크기 변환

<a id="cv-cvtcolor"></a>
### `cv.cvtColor` — 색 공간 변환 (컬러 → 회색조 등)

공식 문서: <https://docs.opencv.org/4.x/d8/d01/group__imgproc__color__conversions.html>

```python
cv.cvtColor(src, code[, dst[, dstCn[, hint]]]) -> dst
```

| 인자 | 의미 |
|---|---|
| `src` | 입력 영상 |
| `code` | 변환 코드 `cv.COLOR_<원본>2<대상>` |
| `dstCn` | 출력 채널 수 (0이면 자동) |

이 프로젝트에서 쓴 변환 코드

| 코드 | 용도 | 사용 파일 |
|---|---|---|
| `cv.COLOR_BGR2GRAY` | **컬러 → 회색조(명암)**. 3채널 → 1채널 | Wk02, Wk04/3, Wk06/02, Wk07, Wk09/02 |
| `cv.COLOR_RGB2BGR` | skimage(RGB) 영상을 OpenCV 표시용(BGR)으로 | Wk05/01, Wk05/02 |
| `cv.COLOR_GRAY2BGR` | 회색조 → 3채널. **컬러 선을 그리기 위해** | Wk06/01 |

회색조 변환 공식(공식 문서): `Y = 0.299·R + 0.587·G + 0.114·B`

**프로젝트 사용례**

```python
# Wk02/1_img_edit.py — 컬러 영상을 명암 영상으로
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
print(gray.shape)          # (948, 1434)  ← 채널 축이 사라짐

# Wk06/01_contours.py — 흑백 영상에 분홍색 컨투어를 그리려면 3채널이 필요
img2 = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
cv.drawContours(img2, contours, -1, (255, 0, 255), 2)
```

> OpenCV는 **BGR**, matplotlib·scikit-image는 **RGB** 순서입니다. 라이브러리 사이를 오갈 때 색이 파랗게/빨갛게 뒤바뀌면 이 변환을 빠뜨린 것입니다.

---

<a id="cv-resize"></a>
### `cv.resize` — 영상 크기 변경 (확대/축소)

공식 문서: <https://docs.opencv.org/4.x/da/d54/group__imgproc__transform.html>

```python
cv.resize(src, dsize[, dst[, fx[, fy[, interpolation]]]]) -> dst
```

| 인자 | 의미 |
|---|---|
| `dsize` | 출력 크기 **`(너비, 높이)`** 순서. `(0,0)`/`None`이면 `fx`, `fy`로 계산 |
| `fx`, `fy` | 가로/세로 배율 |
| `interpolation` | 보간법. 축소엔 `cv.INTER_AREA`, 확대엔 `cv.INTER_CUBIC`(느림)/`cv.INTER_LINEAR`(기본) 권장 |

`dsize`와 (`fx`,`fy`) 중 하나는 0이 아니어야 합니다.

```python
# Wk02/1_img_edit.py — 가로·세로 절반으로 축소
gray_resize = cv.resize(gray, dsize=(0, 0), fx=0.5, fy=0.5)
# (948, 1434) → (474, 717)

# 확장 예: 정확한 크기로 지정 (너비 640, 높이 480)
small = cv.resize(img, (640, 480), interpolation=cv.INTER_AREA)
```

> 주의: `shape`는 `(높이, 너비)`인데 `dsize`는 `(너비, 높이)`입니다.

---

<a id="4-도형글자-그리기"></a>
## 4. 도형·글자 그리기

공식 문서: <https://docs.opencv.org/4.x/d6/d6e/group__imgproc__draw.html>

> 그리기 함수는 모두 **입력 영상을 직접 수정(in-place)** 합니다. 원본을 보존하려면 `np.copy(img)`로 복사본에 그리세요. (Wk05·Wk09에서 `img_show = np.copy(img)` 사용)
> 좌표는 `(x, y)` = `(열, 행)`, 색은 `(B, G, R)` 입니다.

<a id="cv-rectangle"></a>
### `cv.rectangle` — 직사각형 그리기

```python
cv.rectangle(img, pt1, pt2, color[, thickness[, lineType[, shift]]]) -> img
```

| 인자 | 의미 |
|---|---|
| `pt1`, `pt2` | 마주보는 두 꼭짓점 (왼쪽 위, 오른쪽 아래) |
| `color` | `(B, G, R)` |
| `thickness` | 선 두께. **음수(-1 또는 `cv.FILLED`)면 내부를 채움** |
| `lineType` | `cv.LINE_8`(기본), `cv.LINE_AA`(안티앨리어싱) |

```python
# Wk03/1_rectangle_text.py — 빨간 테두리 2px
cv.rectangle(img, (830, 30), (1000, 200), (0, 0, 255), 2)

# Wk03/2_click_rectangle.py — 클릭 위치에서 200x200 사각형
cv.rectangle(img, (x, y), (x+200, y+200), (0, 0, 255), 2)
```

<a id="cv-circle"></a>
### `cv.circle` — 원 그리기

```python
cv.circle(img, center, radius, color[, thickness[, lineType[, shift]]]) -> img
```

| 인자 | 의미 |
|---|---|
| `center` | 중심 `(x, y)` |
| `radius` | 반지름(픽셀) |
| `color` | 컬러 영상이면 `(B,G,R)`, **1채널 영상이면 숫자 하나** |
| `thickness` | `-1`이면 속이 찬 원 → **붓질 효과** |

```python
# Wk03/4_click_paint.py — 붓으로 칠하기
cv.circle(img, (x, y), BrushSiz, LColor, -1)

# Wk05/03_grab_cut.py, Wk09/01_Orim.py — 같은 위치를 마스크에도 칠함
# 1채널 mask에 '색' 대신 GrabCut 레이블 값을 그려 넣는 트릭
cv.circle(img_show, (x, y), BrushSize, LColor, -1)      # 화면용
cv.circle(mask,     (x, y), BrushSize, cv.GC_FGD, -1)    # 알고리즘용 (값 1)
```

<a id="cv-puttext"></a>
### `cv.putText` — 글자 쓰기

```python
cv.putText(img, text, org, fontFace, fontScale, color[, thickness[, lineType[, bottomLeftOrigin]]]) -> img
```

| 인자 | 의미 |
|---|---|
| `text` | 문자열 (**Hershey 폰트는 한글 미지원** → 한글은 `?`로 깨짐) |
| `org` | 글자열의 **왼쪽 아래** 좌표 |
| `fontFace` | `cv.FONT_HERSHEY_SIMPLEX`, `cv.FONT_HERSHEY_PLAIN` 등 |
| `fontScale` | 기본 크기 대비 배율 |
| `thickness` | 획 두께 |

```python
# Wk03/1_rectangle_text.py — 사각형 바로 위에 파란 글자
cv.putText(img, 'laugh', (830, 24), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
```

---

<a id="5-이진화모폴로지"></a>
## 5. 이진화·모폴로지

<a id="cv-threshold"></a>
### `cv.threshold` — 임계값 이진화 (오츄 알고리즘 포함)

공식 문서: <https://docs.opencv.org/4.x/d7/d1b/group__imgproc__misc.html>

```python
cv.threshold(src, thresh, maxval, type[, dst]) -> retval, dst
```

| 인자 | 의미 |
|---|---|
| `src` | 입력 (오츄는 **8비트/16비트 1채널만** 지원) |
| `thresh` | 임계값. 오츄 사용 시 무시되므로 보통 0 |
| `maxval` | 조건을 만족한 화소에 넣을 값 (보통 255) |
| `type` | `cv.THRESH_BINARY`, `cv.THRESH_BINARY_INV` … + 선택적으로 `cv.THRESH_OTSU` |

반환값: `(실제 사용된 임계값, 이진 영상)` — **튜플 두 개를 받아야** 합니다.

`THRESH_BINARY`: `dst = maxval if src > thresh else 0`
`THRESH_OTSU`를 더하면 임계값을 **자동으로 최적화**해 그 값을 `retval`로 돌려줍니다.

**프로젝트 사용례**

```python
# Wk03/6_otsu_algorithm.py — R 채널(인덱스 2)을 오츄로 이진화
t, bin_img = cv.threshold(img[:, :, 2], 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
print('OTSU 알고리즘이 찾은 최적의 임곗값 =', t)

# Wk04/1.py — PNG 알파 채널(인덱스 3)로 서명 부분만 추출
t, bin_img = cv.threshold(img[:, :, 3], 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
```

> 컬러 영상 전체(3채널)에 오츄를 쓰면 에러가 납니다. 채널 하나를 슬라이싱하거나 `cvtColor`로 회색조를 만든 뒤 사용하세요.

---

<a id="cv-dilate"></a>
### `cv.dilate` — 팽창 (흰 영역 넓히기)

공식 문서: <https://docs.opencv.org/4.x/d4/d86/group__imgproc__filter.html>

```python
cv.dilate(src, kernel[, dst[, anchor[, iterations[, borderType[, borderValue]]]]]) -> dst
```

| 인자 | 의미 |
|---|---|
| `kernel` | 구조 요소(structuring element). 1인 위치가 이웃으로 쓰임 |
| `iterations` | 반복 횟수 |

이웃 중 **최댓값**을 취하므로 흰(255) 물체가 두꺼워지고 작은 구멍·틈이 메워집니다.

```python
# Wk04/1.py — 다이아몬드 모양 구조 요소
se = np.uint8([[0,0,1,0,0],
               [0,1,1,1,0],
               [1,1,1,1,1],
               [0,1,1,1,0],
               [0,0,1,0,0]])
b_dilation = cv.dilate(b, se, iterations=1)
```

> 구조 요소는 `cv.getStructuringElement(cv.MORPH_ELLIPSE, (5,5))`로도 만들 수 있습니다.

<a id="cv-erode"></a>
### `cv.erode` — 침식 (흰 영역 깎기)

```python
cv.erode(src, kernel[, dst[, anchor[, iterations[, borderType[, borderValue]]]]]) -> dst
```

이웃 중 **최솟값**을 취하므로 흰 물체가 얇아지고 작은 흰 잡음이 사라집니다.

```python
# Wk04/2.py — 3x3 구조 요소로 4번 침식
se = np.uint8([[1,1,1],[1,1,1],[1,1,1]])
b = cv.erode(bin_img, se, iterations=4)
```

<a id="cv-morph-combo"></a>
### 열림(opening) / 닫힘(closing) 조합

| 연산 | 순서 | 효과 | 프로젝트 |
|---|---|---|---|
| 열림 | 침식 → 팽창 | 작은 흰 잡음 제거 | Wk04/2.py (erode 4 → dilate 2) |
| 닫힘 | 팽창 → 침식 | 작은 검은 구멍 메우기 | Wk04/1.py, Wk04/2.py |

```python
# Wk04/1.py — 닫힘을 직접 조합
b_closing = cv.erode(cv.dilate(b, se, iterations=1), se, iterations=1)

# 같은 결과를 한 번에 (공식 함수)
b_closing = cv.morphologyEx(b, cv.MORPH_CLOSE, se)
```

---

<a id="6-히스토그램"></a>
## 6. 히스토그램

공식 문서: <https://docs.opencv.org/4.x/d6/dc7/group__imgproc__hist.html>

<a id="cv-calchist"></a>
### `cv.calcHist` — 히스토그램 계산

```python
cv.calcHist(images, channels, mask, histSize, ranges[, hist[, accumulate]]) -> hist
```

| 인자 | 의미 |
|---|---|
| `images` | **리스트**로 감싼 영상 `[gray]` |
| `channels` | 계산할 채널 인덱스 리스트 `[0]` |
| `mask` | 일부 영역만 계산할 때 마스크, 전체면 `None` |
| `histSize` | 빈(bin) 개수 리스트 `[256]` |
| `ranges` | 값 범위 `[0, 256]` (**상한 256은 포함 안 됨**) |

반환값: `float32` 배열. 설치된 **OpenCV 5.0.0에서는 모양이 `(256,)`** 입니다(OpenCV 4.x 자료에서는 `(256, 1)`로 나옴 — 직접 확인함). 어느 쪽이든 `plt.plot(h)`로 바로 그릴 수 있습니다.

```python
# Wk04/3.py
h = cv.calcHist([gray], [0], None, [256], [0, 256])
plt.plot(h, color='r', linewidth=1)
```

<a id="cv-equalizehist"></a>
### `cv.equalizeHist` — 히스토그램 평활화 (명암 대비 향상)

```python
cv.equalizeHist(src[, dst]) -> dst
```

**8비트 1채널** 영상의 히스토그램을 고르게 펴서 대비를 높입니다. 안개 낀 영상처럼 명암이 좁은 범위에 몰린 영상에 효과적입니다.

```python
# Wk04/3.py — 안개 낀 도로 영상
gray  = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
equal = cv.equalizeHist(gray)
```

> 컬러 영상은 직접 넣을 수 없습니다. 회색조로 바꾸거나, YCrCb로 변환해 Y 채널만 평활화하세요.

---

<a id="7-영역-분할"></a>
## 7. 영역 분할

<a id="cv-grabcut"></a>
### `cv.grabCut` — 사용자 힌트 기반 전경/배경 분리 (오려내기)

공식 문서: <https://docs.opencv.org/4.x/d3/d47/group__imgproc__segmentation.html>

```python
cv.grabCut(img, mask, rect, bgdModel, fgdModel, iterCount[, mode]) -> mask, bgdModel, fgdModel
```

| 인자 | 의미 |
|---|---|
| `img` | **8비트 3채널** 입력 영상 |
| `mask` | 8비트 1채널 입출력 마스크. **함수가 직접 갱신** |
| `rect` | 물체를 감싸는 사각형 `(x,y,w,h)`. `GC_INIT_WITH_RECT`일 때만 사용, 마스크 모드면 `None` |
| `bgdModel`, `fgdModel` | 내부 모델용 임시 배열. `np.zeros((1,65), np.float64)` |
| `iterCount` | 반복 횟수 |
| `mode` | `cv.GC_INIT_WITH_RECT` / `cv.GC_INIT_WITH_MASK` / `cv.GC_EVAL` |

마스크 레이블 값 (GrabCutClasses)

| 상수 | 값 | 의미 |
|---|---|---|
| `cv.GC_BGD` | 0 | 확실한 배경 |
| `cv.GC_FGD` | 1 | 확실한 전경(물체) |
| `cv.GC_PR_BGD` | 2 | 아마 배경 |
| `cv.GC_PR_FGD` | 3 | 아마 전경 |

**전체 흐름 (Wk05/03_grab_cut.py, Wk09/01_Orim.py)**

```python
# 1) 마스크 전체를 '아마 배경'으로 초기화
mask = np.zeros((img.shape[0], img.shape[1]), np.uint8)
mask[:, :] = cv.GC_PR_BGD

# 2) 마우스로 물체(GC_FGD)/배경(GC_BGD)을 칠함  → cv.circle(mask, ..., cv.GC_FGD, -1)

# 3) 마스크 모드로 GrabCut 실행 (mask가 제자리에서 갱신됨)
background = np.zeros((1, 65), np.float64)
foreground = np.zeros((1, 65), np.float64)
cv.grabCut(img, mask, None, background, foreground, 5, cv.GC_INIT_WITH_MASK)

# 4) 배경(0, 2)은 0, 전경(1, 3)은 1로 바꿔 원본에 곱함
mask2 = np.where((mask == cv.GC_BGD) | (mask == cv.GC_PR_BGD), 0, 1).astype('uint8')
grab = img * mask2[:, :, np.newaxis]
```

> 주의: 마스크 모드에서는 **전경·배경을 둘 다 최소 한 번씩** 칠해야 합니다. 한쪽만 있으면 모델을 학습할 수 없어 에러가 납니다.
> `Wk09/01_Orim.py`의 `(self.mask == 2) | (self.mask == 0)`은 위 표의 숫자 값을 그대로 쓴 것으로, `GC_PR_BGD`/`GC_BGD`와 같습니다.

---

<a id="8-컨투어외곽선모양-분석"></a>
## 8. 컨투어(외곽선)·모양 분석

공식 문서: <https://docs.opencv.org/4.x/d3/dc0/group__imgproc__shape.html>

<a id="cv-findcontours"></a>
### `cv.findContours` — 이진 영상에서 외곽선 찾기

```python
cv.findContours(image, mode, method[, contours[, hierarchy[, offset]]]) -> contours, hierarchy
```

| 인자 | 의미 |
|---|---|
| `image` | **8비트 1채널**. 0이 아닌 화소를 물체(1)로 봄 |
| `mode` | 검출 방식 (아래 표) |
| `method` | 점 저장 방식 (아래 표) |

| `mode` | 의미 |
|---|---|
| `cv.RETR_EXTERNAL` | 가장 바깥 외곽선만 |
| `cv.RETR_LIST` | 모든 외곽선, 계층 없음 |
| `cv.RETR_CCOMP` | 2단계 계층 |
| `cv.RETR_TREE` | 전체 계층 트리 |

| `method` | 의미 |
|---|---|
| `cv.CHAIN_APPROX_NONE` | 경계의 모든 점 저장 |
| `cv.CHAIN_APPROX_SIMPLE` | 직선 구간은 끝점만 저장 (메모리 절약) |

반환값
- `contours`: 외곽선들의 튜플. 각 원소는 `(점 개수, 1, 2)` 모양 배열
- `hierarchy`: `(1, N, 4)` 배열 — 각 외곽선의 `[다음, 이전, 첫 자식, 부모]` 인덱스 (없으면 -1)

```python
# Wk06/01_contours.py — skimage 말 영상(bool)을 0/255로 바꿔 사용
original = skimage.data.horse()
img = 255 - np.uint8(original) * 255
contours, hierarchy = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
contour = contours[0]
```

<a id="cv-drawcontours"></a>
### `cv.drawContours` — 외곽선 그리기

```python
cv.drawContours(image, contours, contourIdx, color[, thickness[, lineType[, hierarchy[, maxLevel[, offset]]]]]) -> image
```

| 인자 | 의미 |
|---|---|
| `contours` | 외곽선 **리스트** (하나만 그릴 때도 `[c]`로 감쌈) |
| `contourIdx` | 그릴 인덱스. **-1이면 전부** |
| `thickness` | 두께, -1이면 내부 채움 |

```python
# Wk06/01_contours.py
cv.drawContours(img2, contours, -1, (255, 0, 255), 2)          # 모든 외곽선
cv.drawContours(img3, [contour_approx], -1, (0, 255, 0), 2)    # 근사 다각형 하나
```

<a id="cv-moments"></a>
### `cv.moments` — 모멘트 계산 (면적·무게중심)

```python
cv.moments(array[, binaryImage]) -> retval
```

딕셔너리를 반환합니다. 주요 키: `m00`(면적), `m10`, `m01`(1차 모멘트), `mu20`… (중심 모멘트), `nu20`… (정규화 중심 모멘트).

```python
# Wk06/01_contours.py — 무게중심
m = cv.moments(contour)
cx, cy = m['m10'] / m['m00'], m['m01'] / m['m00']
```

> `m00`이 0이면(점·선 형태) 0으로 나누기 에러가 납니다.

<a id="cv-contourarea"></a>
### `cv.contourArea` — 외곽선 내부 면적

```python
cv.contourArea(contour[, oriented]) -> retval
```

`oriented=True`면 방향(시계/반시계)에 따라 부호가 있는 면적을 돌려줍니다.

```python
area = cv.contourArea(contour)      # Wk06/01_contours.py
```

<a id="cv-arclength"></a>
### `cv.arcLength` — 외곽선 둘레 길이

```python
cv.arcLength(curve, closed) -> retval
```

`closed=True`면 마지막 점과 첫 점을 잇는 길이까지 포함(폐곡선).

```python
# Wk06/01_contours.py — 둘레와 원형도(roundness)
perimeter = cv.arcLength(contour, True)
roundness = (4.0 * np.pi * area) / (perimeter * perimeter)   # 1에 가까울수록 원
```

<a id="cv-approxpolydp"></a>
### `cv.approxPolyDP` — 외곽선을 다각형으로 근사 (단순화)

```python
cv.approxPolyDP(curve, epsilon, closed[, approxCurve]) -> approxCurve
```

| 인자 | 의미 |
|---|---|
| `epsilon` | 원래 곡선과 근사 다각형 사이 **최대 허용 거리**. 클수록 꼭짓점이 적어짐 |
| `closed` | 폐곡선 여부 |

Douglas-Peucker 알고리즘을 사용합니다. 흔히 `epsilon = 0.01 * cv.arcLength(c, True)`처럼 둘레에 비례해 정합니다.

```python
contour_approx = cv.approxPolyDP(contour, 8, True)   # Wk06/01_contours.py
```

<a id="cv-convexhull"></a>
### `cv.convexHull` — 볼록 껍질

```python
cv.convexHull(points[, hull[, clockwise[, returnPoints]]]) -> hull
```

모든 점을 포함하는 **가장 작은 볼록 다각형**을 구합니다. 반환 모양은 `(점 개수, 1, 2)`.

```python
# Wk06/01_contours.py
hull = cv.convexHull(contour)
hull = hull.reshape(1, hull.shape[0], hull.shape[2])   # (1, N, 2): 외곽선 1개짜리 묶음으로
cv.drawContours(img3, hull, -1, (0, 0, 255), 2)

# 같은 결과를 더 간단히
cv.drawContours(img3, [cv.convexHull(contour)], -1, (0, 0, 255), 2)
```

---

<a id="9-코너특징점매칭"></a>
## 9. 코너·특징점·매칭

<a id="cv-cornerharris"></a>
### `cv.cornerHarris` — 해리스 코너 검출

공식 문서: <https://docs.opencv.org/4.x/dd/d1a/group__imgproc__feature.html>

```python
cv.cornerHarris(src, blockSize, ksize, k[, dst[, borderType]]) -> dst
```

| 인자 | 의미 |
|---|---|
| `src` | **1채널** 8비트 또는 float 영상 |
| `blockSize` | 공분산 행렬을 계산할 이웃 크기 |
| `ksize` | 미분에 쓸 Sobel 커널 크기 (3, 5, 7 …) |
| `k` | 해리스 상수 (보통 0.04 ~ 0.06) |

반환값: 입력과 같은 크기의 `float32` 응답 지도. `R = det(M) − k·(trace M)²` 이며, **값이 클수록 코너**입니다.

```python
# Wk06/02_Harris_Corner.py — 최댓값의 5%보다 큰 곳을 빨간색으로
gray = np.float32(cv.cvtColor(img, cv.COLOR_BGR2GRAY))
dist = cv.cornerHarris(gray, 3, 3, 0.04)
img[dist > 0.05 * dist.max()] = [0, 0, 255]
```

---

<a id="cv-sift-create"></a>
### `cv.SIFT_create` — SIFT 검출기 생성

공식 문서: <https://docs.opencv.org/4.x/d7/d60/classcv_1_1SIFT.html>

```python
cv.SIFT_create([, nfeatures[, nOctaveLayers[, contrastThreshold[, edgeThreshold[, sigma[, enable_precise_upscale]]]]]]) -> retval
```

| 인자 | 기본값 | 의미 |
|---|---|---|
| `nfeatures` | 0 | 상위 몇 개만 남길지 (0 = 전부) |
| `nOctaveLayers` | 3 | 옥타브당 층 수 |
| `contrastThreshold` | 0.04 | 클수록 약한 특징점 제거 → 개수 감소 |
| `edgeThreshold` | 10 | 클수록 에지성 특징점을 덜 걸러냄 |
| `sigma` | 1.6 | 첫 옥타브 가우시안 σ |

크기·회전에 불변인 특징점을 찾는 SIFT 객체를 만듭니다. (특허 만료로 OpenCV 4.4부터 기본 패키지에 포함)

```python
sift = cv.SIFT_create()         # Wk07/01_sift.py, Wk07/02_FLANN.py, Wk09/02_VisionAgent02.py
```

<a id="cv-detectandcompute"></a>
### `Feature2D.detectAndCompute` — 특징점 검출 + 기술자 계산

공식 문서: <https://docs.opencv.org/4.x/d0/d13/classcv_1_1Feature2D.html>

```python
sift.detectAndCompute(image, mask[, descriptors[, useProvidedKeypoints]]) -> keypoints, descriptors
```

| 반환값 | 의미 |
|---|---|
| `keypoints` | `cv.KeyPoint` 튜플. 속성 `pt`(x,y), `size`, `angle`, `response`, `octave` |
| `descriptors` | `(특징점 개수, 128)` `float32` 배열 (SIFT 기준). 특징점이 없으면 `None` |

```python
# Wk07/02_FLANN.py
kp1, des1 = sift.detectAndCompute(gray1, None)
kp2, des2 = sift.detectAndCompute(gray2, None)
print(f'특징점 개수: {len(kp1)}, {len(kp2)}')
```

> 검출만 필요하면 `sift.detect(img, None)`, 기존 특징점의 기술자만 필요하면 `sift.compute(img, kp)`.

<a id="cv-drawkeypoints"></a>
### `cv.drawKeypoints` — 특징점 그리기

공식 문서: <https://docs.opencv.org/4.x/d4/d5d/group__features2d__draw.html>

```python
cv.drawKeypoints(image, keypoints, outImage[, color[, flags]]) -> outImage
```

| `flags` | 의미 |
|---|---|
| `cv.DRAW_MATCHES_FLAGS_DEFAULT` | 작은 원으로 위치만 |
| `cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS` | **크기(원 반지름)와 방향(선)** 까지 표시 |

```python
# Wk07/01_sift.py — outImage에 None을 주면 새 영상을 만들어 반환
gray = cv.drawKeypoints(gray, kp, None, flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
```

<a id="cv-descriptormatcher-create"></a>
### `cv.DescriptorMatcher_create` — 매처 생성 (FLANN / 전수조사)

공식 문서: <https://docs.opencv.org/4.x/db/d39/classcv_1_1DescriptorMatcher.html>

```python
cv.DescriptorMatcher_create(descriptorMatcherType) -> retval
```

| 타입 상수 | 의미 |
|---|---|
| `cv.DescriptorMatcher_FLANNBASED` | FLANN 근사 최근접 탐색. **빠름**, float 기술자(SIFT)용 |
| `cv.DescriptorMatcher_BRUTEFORCE` | 전수조사(L2). 정확하지만 느림 |
| `cv.DescriptorMatcher_BRUTEFORCE_HAMMING` | 이진 기술자(ORB 등)용 |

```python
flann_matcher = cv.DescriptorMatcher_create(cv.DescriptorMatcher_FLANNBASED)   # Wk07/02, Wk09/02
```

<a id="cv-knnmatch"></a>
### `DescriptorMatcher.knnMatch` — k개 최근접 매칭

```python
matcher.knnMatch(queryDescriptors, trainDescriptors, k[, mask[, compactResult]]) -> matches
```

각 query 기술자마다 가장 가까운 train 기술자 **k개**를 `DMatch` 리스트로 돌려줍니다. 결과는 `[[DMatch, DMatch], ...]` 형태(리스트의 리스트).

**최근접 거리 비율 검사 (Lowe's ratio test)** — 1등과 2등의 거리 비율이 작을 때만 신뢰합니다.

```python
# Wk07/02_FLANN.py
knn_match = flann_matcher.knnMatch(des1, des2, 2)
T = 0.7
good_match = []
for nearest1, nearest2 in knn_match:
    if nearest1.distance / nearest2.distance < T:
        good_match.append(nearest1)
```

> `T`를 작게(0.5~0.6) 하면 잘못된 매칭(FP)이 줄고, 크게 하면 매칭 수가 늘어납니다.
> 드물게 후보가 2개 미만인 원소가 있으면 `for a, b in ...` 언패킹이 실패할 수 있으니, 견고하게 하려면 `if len(m) == 2:` 검사를 추가하세요.

<a id="cv-dmatch"></a>
#### `cv.DMatch` 객체 속성

공식 문서: <https://docs.opencv.org/4.x/d4/de0/classcv_1_1DMatch.html>

| 속성 | 의미 |
|---|---|
| `queryIdx` | query 쪽 특징점 인덱스 (`kp1[m.queryIdx]`) |
| `trainIdx` | train 쪽 특징점 인덱스 (`kp2[m.trainIdx]`) |
| `distance` | 기술자 간 거리 (작을수록 유사) |

```python
# 매칭된 좌표 꺼내기 (호모그래피 계산 등에 사용)
src_pts = np.float32([kp1[m.queryIdx].pt for m in good_match])
dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_match])
```

<a id="cv-drawmatches"></a>
### `cv.drawMatches` — 두 영상의 매칭 결과 그리기

```python
cv.drawMatches(img1, keypoints1, img2, keypoints2, matches1to2, outImg[, matchColor[, singlePointColor[, matchesMask[, flags]]]]) -> outImg
```

| 인자 | 의미 |
|---|---|
| `img1`, `keypoints1` | 왼쪽에 놓일 영상과 특징점 (query) |
| `img2`, `keypoints2` | 오른쪽 영상과 특징점 (train) |
| `matches1to2` | `DMatch` 리스트 |
| `outImg` | 출력 영상 (미리 만들어 두거나 `None`) |
| `flags` | `cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS` → 매칭 안 된 점은 안 그림 |

```python
# Wk07/02_FLANN.py — 두 영상을 나란히 놓을 캔버스를 미리 생성
img_match = np.empty((max(img1.shape[0], img2.shape[0]),
                      img1.shape[1] + img2.shape[1], 3), dtype=np.uint8)
cv.drawMatches(img1, kp1, img2, kp2, good_match, img_match,
               flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
cv.imshow('Good Matches', img_match)

# 간단한 대안: outImg에 None을 주고 반환값을 사용
img_match = cv.drawMatches(img1, kp1, img2, kp2, good_match, None,
                           flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
```

[↑ 맨 위로](#opencv-cv2-함수-레퍼런스) · [← 전체 목차로](README.md)
