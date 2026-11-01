# 컴퓨터비전 실습 함수 레퍼런스 (Wk02 ~ Wk09)

이 폴더는 `Wk02` ~ `Wk09` 실습 코드에서 사용한 **모든 라이브러리 함수**의 사용법과 프로젝트 내 사용례를 정리한 문서입니다.
각 함수 설명은 라이브러리 공식 문서 기준이며, 시그니처는 이 프로젝트 가상환경(`.venv`)에 설치된 버전에서 직접 확인했습니다.

| 라이브러리 | 버전 | 문서 |
|---|---|---|
| OpenCV (`cv2`) | 5.0.0 | [opencv.md](opencv.md) |
| **PyQt5 (GUI, Wk09 중점)** | 5.15.11 (Qt 5.15.14) | [**pyqt5_gui.md**](pyqt5_gui.md) |
| NumPy | 2.4.6 | [numpy.md](numpy.md) |
| Matplotlib | 3.11.2 | [matplotlib.md](matplotlib.md) |
| scikit-image | 0.26.0 | [scikit-image.md](scikit-image.md) |
| 파이썬 표준 라이브러리 | ≥ 3.11 | [python_stdlib.md](python_stdlib.md) |

> 참고: docs.opencv.org는 자동 조회가 차단(403)되어, OpenCV는 설치된 패키지의 공식 docstring(`help(cv.함수)` — 공식 문서와 같은 소스에서 생성)으로 시그니처·설명을 확인했고, 문서 링크는 OpenCV 4.x 공식 문서의 해당 모듈 페이지로 연결했습니다.

---

## 목차

1. [🔎 하고 싶은 일로 찾기 (목적별 빠른 색인)](#하고-싶은-일로-찾기)
2. [📅 주차별 사용 함수](#주차별-사용-함수)
3. [🔤 함수 이름으로 찾기 (가나다/알파벳순)](#함수-이름으로-찾기)

---

<a id="하고-싶은-일로-찾기"></a>
## 🔎 하고 싶은 일로 찾기

"이걸 하려면 무슨 함수를 쓰지?" 할 때 보는 표입니다. 함수 이름을 누르면 해당 설명으로 바로 이동합니다.

### 영상 읽기·저장·보기

| 하고 싶은 일 | 함수 |
|---|---|
| 파일에서 영상 읽기 | [`cv.imread`](opencv.md#cv-imread) |
| PNG의 투명(알파) 채널까지 읽기 | [`cv.imread(..., cv.IMREAD_UNCHANGED)`](opencv.md#cv-imread) |
| 영상을 파일로 저장 | [`cv.imwrite`](opencv.md#cv-imwrite) |
| 영상을 창에 띄우기 | [`cv.imshow`](opencv.md#cv-imshow) |
| 키를 누를 때까지 창 유지 / 키 입력 받기 | [`cv.waitKey`](opencv.md#cv-waitkey) |
| 특정 키(q)로 종료하기 | [`cv.waitKey`](opencv.md#cv-waitkey) + [`ord`](python_stdlib.md#py-ord) |
| 창 모두 닫기 / 하나만 닫기 | [`cv.destroyAllWindows`](opencv.md#cv-destroyallwindows) / [`cv.destroyWindow`](opencv.md#cv-destroywindow) |
| 제목·한글이 들어간 그림으로 보기 | [`plt.imshow`](matplotlib.md#plt-imshow) + [`plt.title`](matplotlib.md#plt-title) + [한글 폰트](matplotlib.md#mpl-korean-font) |
| 그림의 축 눈금 없애기 | [`plt.xticks([])`](matplotlib.md#plt-xticks) |
| 파일이 없을 때 프로그램 끝내기 | [`sys.exit`](python_stdlib.md#py-sys-exit) |
| 예제 영상을 파일 없이 바로 쓰기 | [`skimage.data.coffee / horse`](scikit-image.md#sk-data) |

### 색·크기·영역 바꾸기

| 하고 싶은 일 | 함수 |
|---|---|
| **컬러 영상을 회색조(명암) 영상으로 바꾸기** | [`cv.cvtColor(img, cv.COLOR_BGR2GRAY)`](opencv.md#cv-cvtcolor) |
| 회색조 영상을 3채널로 (컬러 선 그리기용) | [`cv.cvtColor(img, cv.COLOR_GRAY2BGR)`](opencv.md#cv-cvtcolor) |
| RGB(skimage/matplotlib) ↔ BGR(OpenCV) 바꾸기 | [`cv.cvtColor(img, cv.COLOR_RGB2BGR)`](opencv.md#cv-cvtcolor) |
| 영상 크기 줄이기/늘리기 | [`cv.resize`](opencv.md#cv-resize) |
| 영상 일부 잘라내기 (ROI) | [NumPy 슬라이싱](numpy.md#np-ndarray-slicing) |
| R/G/B 채널 하나만 꺼내기 | [NumPy 슬라이싱 `img[:,:,2]`](numpy.md#np-ndarray-slicing) |
| 영상 크기(높이·너비) 알아내기 | [`.shape`](numpy.md#np-shape) |
| 원본 보존용 복사본 만들기 | [`np.copy`](numpy.md#np-copy) |
| 실수 결과(0~1)를 0~255 영상으로 | [`np.uint8(x * 255)`](numpy.md#np-uint8) |
| 조건에 맞는 화소만 색 바꾸기 | [불리언 인덱싱](numpy.md#np-boolean-index) |

### 그리기·마우스

| 하고 싶은 일 | 함수 |
|---|---|
| 사각형 그리기 | [`cv.rectangle`](opencv.md#cv-rectangle) |
| 원 그리기 / 붓으로 칠하기 | [`cv.circle(..., -1)`](opencv.md#cv-circle) |
| 영상에 글자 쓰기 | [`cv.putText`](opencv.md#cv-puttext) |
| 마우스 클릭·드래그에 반응하기 | [`cv.setMouseCallback`](opencv.md#cv-setmousecallback) + [이벤트 상수](opencv.md#cv-mouse-events) |
| 콜백 등록 전에 창 만들기 | [`cv.namedWindow`](opencv.md#cv-namedwindow) |

### 이진화·잡음 제거·명암 개선

| 하고 싶은 일 | 함수 |
|---|---|
| 흑백(이진) 영상 만들기 / 임계값 자동으로 찾기(오츄) | [`cv.threshold(..., THRESH_BINARY + THRESH_OTSU)`](opencv.md#cv-threshold) |
| 흰 영역 넓히기 (구멍 메우기) | [`cv.dilate`](opencv.md#cv-dilate) |
| 흰 영역 깎기 (작은 잡음 제거) | [`cv.erode`](opencv.md#cv-erode) |
| 열림/닫힘 연산 | [조합 방법](opencv.md#cv-morph-combo) |
| 구조 요소(커널) 만들기 | [`np.uint8([[...]])`](numpy.md#np-uint8) |
| 밝기 히스토그램 구하기 | [`cv.calcHist`](opencv.md#cv-calchist) |
| 히스토그램 그래프로 그리기 | [`plt.plot`](matplotlib.md#plt-plot) |
| 흐릿한(안개 낀) 영상의 대비 높이기 | [`cv.equalizeHist`](opencv.md#cv-equalizehist) |

### 영역 분할

| 하고 싶은 일 | 함수 |
|---|---|
| 슈퍼화소로 잘게 나누기 | [`skimage.segmentation.slic`](scikit-image.md#sk-slic) |
| 영역 경계선 그려 보기 | [`skimage.segmentation.mark_boundaries`](scikit-image.md#sk-mark-boundaries) |
| 영역 인접 그래프 만들기 | [`skimage.graph.rag_mean_color`](scikit-image.md#sk-rag-mean-color) |
| 정규화 절단으로 큰 영역 합치기 | [`skimage.graph.cut_normalized`](scikit-image.md#sk-cut-normalized) |
| 분할된 영역 개수 세기 | [`np.unique(...).size`](numpy.md#np-unique) |
| 마우스로 칠한 힌트로 물체 오려내기 | [`cv.grabCut`](opencv.md#cv-grabcut) |
| 마스크를 0/1로 바꾸기 | [`np.where`](numpy.md#np-where) + [`.astype`](numpy.md#np-astype) |
| 2D 마스크를 컬러 영상에 곱하기 | [`np.newaxis`](numpy.md#np-newaxis) |
| 마스크용 빈 배열 만들기 | [`np.zeros`](numpy.md#np-zeros) |

### 외곽선·모양 분석

| 하고 싶은 일 | 함수 |
|---|---|
| 물체의 외곽선 찾기 | [`cv.findContours`](opencv.md#cv-findcontours) |
| 외곽선 그리기 | [`cv.drawContours`](opencv.md#cv-drawcontours) |
| 물체 면적 구하기 | [`cv.contourArea`](opencv.md#cv-contourarea) |
| 무게중심 구하기 | [`cv.moments`](opencv.md#cv-moments) |
| 둘레 길이 구하기 | [`cv.arcLength`](opencv.md#cv-arclength) |
| 얼마나 둥근지(원형도) 계산 | [`cv.arcLength`](opencv.md#cv-arclength) + [`np.pi`](numpy.md#np-pi) |
| 외곽선을 단순한 다각형으로 | [`cv.approxPolyDP`](opencv.md#cv-approxpolydp) |
| 볼록 껍질 구하기 | [`cv.convexHull`](opencv.md#cv-convexhull) + [`.reshape`](numpy.md#np-reshape) |

### 특징점·매칭

| 하고 싶은 일 | 함수 |
|---|---|
| 코너(모서리) 찾기 | [`cv.cornerHarris`](opencv.md#cv-cornerharris) |
| SIFT 특징점 검출기 만들기 | [`cv.SIFT_create`](opencv.md#cv-sift-create) |
| 특징점 + 기술자 한 번에 구하기 | [`detectAndCompute`](opencv.md#cv-detectandcompute) |
| 특징점을 크기·방향과 함께 그리기 | [`cv.drawKeypoints`](opencv.md#cv-drawkeypoints) |
| 빠른 매처(FLANN) 만들기 | [`cv.DescriptorMatcher_create`](opencv.md#cv-descriptormatcher-create) |
| 가장 가까운 2개 찾기 + 비율 검사 | [`knnMatch`](opencv.md#cv-knnmatch) |
| 매칭 결과의 거리·인덱스 읽기 | [`DMatch`](opencv.md#cv-dmatch) |
| 두 영상의 매칭을 나란히 그리기 | [`cv.drawMatches`](opencv.md#cv-drawmatches) + [`np.empty`](numpy.md#np-empty) |
| 처리 시간 재기 | [`time.time`](python_stdlib.md#py-time) |
| 매칭이 가장 많은 후보 고르기 | [`max(key=len)` / `index`](python_stdlib.md#py-max-key) |

### ⭐ GUI 만들기 (Wk09)

| 하고 싶은 일 | 함수 / 문서 위치 |
|---|---|
| PyQt5 프로그램 기본 구조 알기 | [프로그램 뼈대](pyqt5_gui.md#qt-structure) |
| GUI 앱 시작하기 | [`QApplication`](pyqt5_gui.md#qt-qapplication) + [`app.exec_()`](pyqt5_gui.md#qt-exec) |
| 메인 창 만들기 | [`QMainWindow`](pyqt5_gui.md#qt-qmainwindow) |
| 창 제목 바꾸기 | [`setWindowTitle`](pyqt5_gui.md#qt-setwindowtitle) |
| 창/버튼의 위치·크기 지정 | [`setGeometry`](pyqt5_gui.md#qt-setgeometry) |
| 창 띄우기 / 닫기 | [`show`](pyqt5_gui.md#qt-show) / [`close`](pyqt5_gui.md#qt-close) |
| 버튼 만들기 | [`QPushButton`](pyqt5_gui.md#qt-qpushbutton) |
| **버튼을 누르면 함수 실행하기** | [`clicked.connect` (시그널·슬롯)](pyqt5_gui.md#qt-signal-slot) |
| 안내 문구 표시하기 / 바꾸기 / 지우기 | [`QLabel`](pyqt5_gui.md#qt-qlabel) / [`setText`](pyqt5_gui.md#qt-settext) / [`clear`](pyqt5_gui.md#qt-clear) |
| 파일 열기 대화상자 | [`QFileDialog.getOpenFileName`](pyqt5_gui.md#qt-qfiledialog-open) |
| 파일 저장 대화상자 | [`QFileDialog.getSaveFileName`](pyqt5_gui.md#qt-qfiledialog-save) |
| OpenCV 창과 Qt 창 같이 쓰기 | [통합 시 주의점](pyqt5_gui.md#qt-opencv-integration) |
| 오류를 팝업으로 알리기 | [`QMessageBox`](pyqt5_gui.md#qt-pitfalls) |
| 버튼을 자동 정렬하기 (레이아웃) | [확장: 레이아웃](pyqt5_gui.md#qt-extensions) |
| OpenCV 영상을 Qt 창 안에 표시 | [확장: QLabel에 영상 표시](pyqt5_gui.md#qt-extensions) |
| 오림(GrabCut) GUI 전체 흐름 이해 | [코드 해설 ①](pyqt5_gui.md#qt-walkthrough-orim) |
| 표지판 인식 GUI 전체 흐름 이해 | [코드 해설 ②](pyqt5_gui.md#qt-walkthrough-traffic) |
| Wk09 코드의 알려진 문제와 고치는 법 | [주의할 점과 개선 방법](pyqt5_gui.md#qt-pitfalls) |

---

<a id="주차별-사용-함수"></a>
## 📅 주차별 사용 함수

### Wk02 — 영상 읽기·변환·저장
`Wk02/1_img_edit.py`
[`cv.imread`](opencv.md#cv-imread) · [`cv.cvtColor`](opencv.md#cv-cvtcolor) · [`cv.resize`](opencv.md#cv-resize) · [`cv.imwrite`](opencv.md#cv-imwrite) · [`cv.imshow`](opencv.md#cv-imshow) · [`cv.waitKey`](opencv.md#cv-waitkey) · [`cv.destroyAllWindows`](opencv.md#cv-destroyallwindows) · [슬라이싱](numpy.md#np-ndarray-slicing) · [`.shape`](numpy.md#np-shape) · [`sys.exit`](python_stdlib.md#py-sys-exit)

### Wk03 — 그리기·마우스 이벤트·채널·오츄 이진화
| 파일 | 주요 함수 |
|---|---|
| `1_rectangle_text.py` | [`cv.rectangle`](opencv.md#cv-rectangle), [`cv.putText`](opencv.md#cv-puttext) |
| `2_click_rectangle.py` | [`cv.namedWindow`](opencv.md#cv-namedwindow), [`cv.setMouseCallback`](opencv.md#cv-setmousecallback), [`cv.rectangle`](opencv.md#cv-rectangle), [`ord`](python_stdlib.md#py-ord) |
| `3_drag_rectangle.py` | [`cv.setMouseCallback`](opencv.md#cv-setmousecallback) (`LBUTTONDOWN`/`LBUTTONUP`) |
| `4_click_paint.py` | [`cv.circle`](opencv.md#cv-circle), [마우스 플래그](opencv.md#cv-mouse-events) |
| `5_img_slicing.py` | [슬라이싱·채널 분리](numpy.md#np-ndarray-slicing) |
| `6_otsu_algorithm.py` | [`cv.threshold` + OTSU](opencv.md#cv-threshold) |

### Wk04 — 모폴로지·히스토그램 (Matplotlib 표시)
| 파일 | 주요 함수 |
|---|---|
| `1.py` | [`IMREAD_UNCHANGED`](opencv.md#cv-imread), [`cv.threshold`](opencv.md#cv-threshold), [`cv.dilate`](opencv.md#cv-dilate), [`cv.erode`](opencv.md#cv-erode), [`np.uint8`](numpy.md#np-uint8), [`plt.imshow`](matplotlib.md#plt-imshow), [`plt.xticks`](matplotlib.md#plt-xticks), [`plt.show`](matplotlib.md#plt-show) |
| `2.py` | 위 + [열림/닫힘](opencv.md#cv-morph-combo), [`plt.title`](matplotlib.md#plt-title), [한글 폰트](matplotlib.md#mpl-korean-font) |
| `3.py` | [`cv.cvtColor`](opencv.md#cv-cvtcolor), [`cv.calcHist`](opencv.md#cv-calchist), [`cv.equalizeHist`](opencv.md#cv-equalizehist), [`plt.plot`](matplotlib.md#plt-plot) |

### Wk05 — 영역 분할 (SLIC · 정규화 절단 · GrabCut)
| 파일 | 주요 함수 |
|---|---|
| `01_slic.py` | [`skimage.data.coffee`](scikit-image.md#sk-data), [`slic`](scikit-image.md#sk-slic), [`mark_boundaries`](scikit-image.md#sk-mark-boundaries), [`COLOR_RGB2BGR`](opencv.md#cv-cvtcolor) |
| `02_normalized_cut.py` | [`rag_mean_color`](scikit-image.md#sk-rag-mean-color), [`cut_normalized`](scikit-image.md#sk-cut-normalized), [`np.unique`](numpy.md#np-unique), [`time.time`](python_stdlib.md#py-time) |
| `03_grab_cut.py`, `03_.py` | [`cv.grabCut`](opencv.md#cv-grabcut), [`np.zeros`](numpy.md#np-zeros), [`np.copy`](numpy.md#np-copy), [`np.where`](numpy.md#np-where), [`np.newaxis`](numpy.md#np-newaxis), [`cv.circle`](opencv.md#cv-circle), [`cv.destroyWindow`](opencv.md#cv-destroywindow) |

### Wk06 — 외곽선·코너
| 파일 | 주요 함수 |
|---|---|
| `01_contours.py` | [`skimage.data.horse`](scikit-image.md#sk-data), [`cv.findContours`](opencv.md#cv-findcontours), [`cv.drawContours`](opencv.md#cv-drawcontours), [`cv.moments`](opencv.md#cv-moments), [`cv.contourArea`](opencv.md#cv-contourarea), [`cv.arcLength`](opencv.md#cv-arclength), [`cv.approxPolyDP`](opencv.md#cv-approxpolydp), [`cv.convexHull`](opencv.md#cv-convexhull), [`COLOR_GRAY2BGR`](opencv.md#cv-cvtcolor) |
| `02_Harris_Corner.py` | [`cv.cornerHarris`](opencv.md#cv-cornerharris), [`np.float32`](numpy.md#np-uint8), [불리언 인덱싱](numpy.md#np-boolean-index) |

### Wk07 — SIFT 특징점·FLANN 매칭
| 파일 | 주요 함수 |
|---|---|
| `01_sift.py` | [`cv.SIFT_create`](opencv.md#cv-sift-create), [`detectAndCompute`](opencv.md#cv-detectandcompute), [`cv.drawKeypoints`](opencv.md#cv-drawkeypoints) |
| `02_FLANN.py` | [`DescriptorMatcher_create`](opencv.md#cv-descriptormatcher-create), [`knnMatch`](opencv.md#cv-knnmatch), [`DMatch`](opencv.md#cv-dmatch), [`cv.drawMatches`](opencv.md#cv-drawmatches), [`np.empty`](numpy.md#np-empty) |

### ⭐ Wk09 — PyQt5 GUI + OpenCV 응용
| 파일 | GUI (PyQt5) | 영상 처리 |
|---|---|---|
| `01_Orim.py` (오림) | [`QApplication`](pyqt5_gui.md#qt-qapplication), [`QMainWindow`](pyqt5_gui.md#qt-qmainwindow), [`QPushButton`](pyqt5_gui.md#qt-qpushbutton), [`clicked.connect`](pyqt5_gui.md#qt-signal-slot), [`setGeometry`](pyqt5_gui.md#qt-setgeometry), [`getOpenFileName`](pyqt5_gui.md#qt-qfiledialog-open), [`getSaveFileName`](pyqt5_gui.md#qt-qfiledialog-save) | [`cv.grabCut`](opencv.md#cv-grabcut), [`cv.setMouseCallback`](opencv.md#cv-setmousecallback), [`cv.circle`](opencv.md#cv-circle), [`cv.imwrite`](opencv.md#cv-imwrite) |
| `02_VisionAgent02.py` (교통약자 보호) | 위 + [`QLabel`](pyqt5_gui.md#qt-qlabel), [`setText`](pyqt5_gui.md#qt-settext), [`clear`](pyqt5_gui.md#qt-clear) | [`SIFT`](opencv.md#cv-sift-create), [FLANN `knnMatch`](opencv.md#cv-knnmatch), [`cv.drawMatches`](opencv.md#cv-drawmatches) |

→ 전체 흐름 해설: [오림](pyqt5_gui.md#qt-walkthrough-orim) · [교통약자 보호](pyqt5_gui.md#qt-walkthrough-traffic) · [주의할 점](pyqt5_gui.md#qt-pitfalls)

---

<a id="함수-이름으로-찾기"></a>
## 🔤 함수 이름으로 찾기

### OpenCV
[`approxPolyDP`](opencv.md#cv-approxpolydp) · [`arcLength`](opencv.md#cv-arclength) · [`calcHist`](opencv.md#cv-calchist) · [`circle`](opencv.md#cv-circle) · [`contourArea`](opencv.md#cv-contourarea) · [`convexHull`](opencv.md#cv-convexhull) · [`cornerHarris`](opencv.md#cv-cornerharris) · [`cvtColor`](opencv.md#cv-cvtcolor) · [`DescriptorMatcher_create`](opencv.md#cv-descriptormatcher-create) · [`destroyAllWindows`](opencv.md#cv-destroyallwindows) · [`destroyWindow`](opencv.md#cv-destroywindow) · [`detectAndCompute`](opencv.md#cv-detectandcompute) · [`dilate`](opencv.md#cv-dilate) · [`DMatch`](opencv.md#cv-dmatch) · [`drawContours`](opencv.md#cv-drawcontours) · [`drawKeypoints`](opencv.md#cv-drawkeypoints) · [`drawMatches`](opencv.md#cv-drawmatches) · [`equalizeHist`](opencv.md#cv-equalizehist) · [`erode`](opencv.md#cv-erode) · [`findContours`](opencv.md#cv-findcontours) · [`grabCut`](opencv.md#cv-grabcut) · [`imread`](opencv.md#cv-imread) · [`imshow`](opencv.md#cv-imshow) · [`imwrite`](opencv.md#cv-imwrite) · [`knnMatch`](opencv.md#cv-knnmatch) · [`moments`](opencv.md#cv-moments) · [`namedWindow`](opencv.md#cv-namedwindow) · [`putText`](opencv.md#cv-puttext) · [`rectangle`](opencv.md#cv-rectangle) · [`resize`](opencv.md#cv-resize) · [`setMouseCallback`](opencv.md#cv-setmousecallback) · [`SIFT_create`](opencv.md#cv-sift-create) · [`threshold`](opencv.md#cv-threshold) · [`waitKey`](opencv.md#cv-waitkey)

### PyQt5
[`QApplication`](pyqt5_gui.md#qt-qapplication) · [`exec_`](pyqt5_gui.md#qt-exec) · [`QMainWindow`](pyqt5_gui.md#qt-qmainwindow) · [`setWindowTitle`](pyqt5_gui.md#qt-setwindowtitle) · [`setGeometry`](pyqt5_gui.md#qt-setgeometry) · [`show`](pyqt5_gui.md#qt-show) · [`close`](pyqt5_gui.md#qt-close) · [`QPushButton`](pyqt5_gui.md#qt-qpushbutton) · [`clicked.connect`](pyqt5_gui.md#qt-signal-slot) · [`QLabel`](pyqt5_gui.md#qt-qlabel) · [`setText`](pyqt5_gui.md#qt-settext) · [`clear`](pyqt5_gui.md#qt-clear) · [`QFileDialog.getOpenFileName`](pyqt5_gui.md#qt-qfiledialog-open) · [`QFileDialog.getSaveFileName`](pyqt5_gui.md#qt-qfiledialog-save)

### NumPy
[`astype`](numpy.md#np-astype) · [`copy`](numpy.md#np-copy) · [`empty`](numpy.md#np-empty) · [`float32`](numpy.md#np-uint8) · [`max`](numpy.md#np-max) · [`newaxis`](numpy.md#np-newaxis) · [`pi`](numpy.md#np-pi) · [`reshape`](numpy.md#np-reshape) · [`shape`](numpy.md#np-shape) · [`uint8`](numpy.md#np-uint8) · [`unique`](numpy.md#np-unique) · [`where`](numpy.md#np-where) · [`zeros`](numpy.md#np-zeros) · [슬라이싱](numpy.md#np-ndarray-slicing) · [불리언 인덱싱](numpy.md#np-boolean-index)

### Matplotlib
[`imshow`](matplotlib.md#plt-imshow) · [`plot`](matplotlib.md#plt-plot) · [`show`](matplotlib.md#plt-show) · [`title`](matplotlib.md#plt-title) · [`xticks / yticks`](matplotlib.md#plt-xticks) · [`font_manager / rc`](matplotlib.md#mpl-korean-font)

### scikit-image
[`data.coffee / data.horse`](scikit-image.md#sk-data) · [`segmentation.slic`](scikit-image.md#sk-slic) · [`segmentation.mark_boundaries`](scikit-image.md#sk-mark-boundaries) · [`graph.rag_mean_color`](scikit-image.md#sk-rag-mean-color) · [`graph.cut_normalized`](scikit-image.md#sk-cut-normalized)

### 파이썬 표준
[`sys.exit`](python_stdlib.md#py-sys-exit) · [`sys.argv`](python_stdlib.md#py-sys-argv) · [`time.time`](python_stdlib.md#py-time) · [`ord`](python_stdlib.md#py-ord) · [`max(key=)`](python_stdlib.md#py-max-key)
