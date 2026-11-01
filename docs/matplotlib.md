<a id="matplotlib-함수-레퍼런스"></a>
# Matplotlib 함수 레퍼런스

> 대상 버전: **Matplotlib 3.11.2** (`import matplotlib.pyplot as plt`)
> 공식 문서: <https://matplotlib.org/stable/api/pyplot_summary.html>
> Wk04에서 영상과 히스토그램을 표시하는 데 사용했습니다. (OpenCV 창 대신 쓰면 **제목·축·한글**을 쉽게 붙일 수 있음)

[← 전체 목차로](README.md)

## 목차

- [`plt.imshow` — 영상 표시](#plt-imshow)
- [`plt.xticks` / `plt.yticks` — 눈금 숨기기](#plt-xticks)
- [`plt.plot` — 선 그래프 (히스토그램)](#plt-plot)
- [`plt.title` — 제목](#plt-title)
- [`plt.show` — 그림 창 띄우기](#plt-show)
- [한글 폰트 설정 (`font_manager`, `rc`)](#mpl-korean-font)

---

<a id="plt-imshow"></a>
## `plt.imshow` — 영상 표시

공식 문서: <https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.imshow.html>

```python
plt.imshow(X, cmap=None, norm=None, *, aspect=None, interpolation=None, alpha=None, vmin=None, vmax=None, ...) -> AxesImage
```

| 인자 | 의미 |
|---|---|
| `X` | `(H,W)` 1채널 또는 `(H,W,3)` **RGB** / `(H,W,4)` RGBA 배열 |
| `cmap` | 1채널일 때 색상표. **회색조 영상은 반드시 `cmap='gray'`** (기본은 `viridis`라 초록·보라로 보임) |
| `vmin`, `vmax` | 색상표에 대응할 값 범위. 생략 시 데이터의 최소~최대로 자동 조정 |

```python
# Wk04/1.py, Wk04/2.py, Wk04/3.py
plt.imshow(bin_img, cmap='gray'), plt.xticks([]), plt.yticks([])
plt.show()
```

> OpenCV 컬러 영상(BGR)을 그대로 넣으면 빨강·파랑이 뒤바뀝니다. `plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))`로 변환하세요.
> 1채널 영상은 기본적으로 최소~최대로 **자동 정규화**되므로, 원래 밝기 그대로 보려면 `vmin=0, vmax=255`를 지정하세요.

<a id="plt-xticks"></a>
## `plt.xticks` / `plt.yticks` — 축 눈금

공식 문서: <https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.xticks.html>

```python
plt.xticks(ticks=None, labels=None, *, minor=False, **kwargs)
```

빈 리스트를 넘기면 눈금이 사라져 영상만 깔끔하게 보입니다.

```python
plt.xticks([]), plt.yticks([])          # Wk04 공통
# 또는 plt.axis('off')  — 축 테두리까지 모두 숨김
```

<a id="plt-plot"></a>
## `plt.plot` — 선 그래프

공식 문서: <https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html>

```python
plt.plot([x], y, [fmt], *, data=None, **kwargs) -> list[Line2D]
```

| 키워드 | 의미 |
|---|---|
| `color` | 선 색 (`'r'`, `'red'`, `'#ff0000'`) |
| `linewidth` | 선 두께 |
| `label` | 범례 이름 (`plt.legend()`와 함께) |

x를 생략하면 0, 1, 2, … 를 x로 씁니다 → 히스토그램의 밝기 값(0~255)이 그대로 x축이 됩니다.

```python
# Wk04/3.py — 평활화 전후 히스토그램
h = cv.calcHist([gray], [0], None, [256], [0, 256])
plt.plot(h, color='r', linewidth=1)
plt.title("평활화 전 히스토그램")
plt.show()
```

<a id="plt-title"></a>
## `plt.title` — 제목

공식 문서: <https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.title.html>

```python
plt.title(label, fontdict=None, loc=None, pad=None, *, y=None, **kwargs) -> Text
```

```python
plt.title('첫 번째 사진 erosion 4번, dilation 2번 이후')   # Wk04/2.py
```

<a id="plt-show"></a>
## `plt.show` — 그림 창 띄우기

공식 문서: <https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.show.html>

```python
plt.show()
```

지금까지 그린 그림을 창으로 표시하고, 창을 닫을 때까지 기다립니다(기본 블로킹). Wk04처럼 `imshow → show`를 반복하면 **창을 닫아야 다음 그림이 나타납니다.** 여러 장을 한 번에 보려면 `plt.subplot(1, 2, 1)` 등으로 나눠 그리세요.

```python
plt.subplot(1, 2, 1); plt.imshow(gray,  cmap='gray'); plt.title('원본')
plt.subplot(1, 2, 2); plt.imshow(equal, cmap='gray'); plt.title('평활화')
plt.show()
```

<a id="mpl-korean-font"></a>
## 한글 폰트 설정 (`font_manager`, `rc`)

공식 문서: [font_manager.FontProperties](https://matplotlib.org/stable/api/font_manager_api.html#matplotlib.font_manager.FontProperties) · [matplotlib.rc](https://matplotlib.org/stable/api/matplotlib_configuration_api.html#matplotlib.rc)

Matplotlib 기본 글꼴(DejaVu Sans)은 한글이 없어 제목이 □□로 깨집니다. 시스템 한글 폰트를 등록합니다.

```python
# Wk04/2.py, Wk04/3.py (macOS)
from matplotlib import font_manager, rc
font_path = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
font_name = font_manager.FontProperties(fname=font_path).get_name()   # 폰트 파일 → 글꼴 이름
rc('font', family=font_name)                                          # 전역 글꼴로 설정
```

- `FontProperties(fname=...)`: 파일 경로로 글꼴 속성 객체 생성, `.get_name()`으로 글꼴 이름 획득
- `rc(group, **kwargs)`: `rcParams['font.family'] = ...`와 같은 전역 설정
- Windows라면 `rc('font', family='Malgun Gothic')`처럼 이름을 바로 지정 가능
- 한글 폰트 사용 시 축의 마이너스 기호가 깨지면 `rc('axes', unicode_minus=False)`

[↑ 맨 위로](#matplotlib-함수-레퍼런스) · [← 전체 목차로](README.md)
