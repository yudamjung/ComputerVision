<a id="pyqt5-gui-레퍼런스-wk09-중점"></a>
# PyQt5 GUI 레퍼런스 (Wk09 중점)

> 대상 버전: **PyQt5 5.15.11 / Qt 5.15.14**
> 공식 문서
> - PyQt5 (Riverbank): <https://www.riverbankcomputing.com/static/Docs/PyQt5/>
> - 시그널/슬롯: <https://www.riverbankcomputing.com/static/Docs/PyQt5/signals_slots.html>
> - Qt 5 클래스 문서: <https://doc.qt.io/qt-5/classes.html>
>
> PyQt5는 C++ Qt를 파이썬으로 감싼 것이라, 클래스·메서드 설명은 Qt 공식 문서(doc.qt.io)를 그대로 따릅니다. 파이썬에서 시그니처가 다른 부분(예: `QFileDialog`의 반환값이 튜플)은 따로 표시했습니다.

[← 전체 목차로](README.md)

## 목차

1. [PyQt5 프로그램의 뼈대](#qt-structure)
2. [애플리케이션·이벤트 루프](#2-애플리케이션이벤트-루프)
   - [QApplication](#qt-qapplication) · [app.exec_()](#qt-exec)
3. [창(Window)](#3-창window)
   - [QMainWindow](#qt-qmainwindow) · [setWindowTitle](#qt-setwindowtitle) · [setGeometry](#qt-setgeometry) · [show](#qt-show) · [close](#qt-close)
4. [위젯(Widget)](#4-위젯widget)
   - [QPushButton](#qt-qpushbutton) · [QLabel](#qt-qlabel) · [QLabel.setText](#qt-settext) · [QLabel.clear](#qt-clear)
5. [시그널과 슬롯 — 버튼 클릭 처리](#qt-signal-slot)
6. [파일 대화상자](#6-파일-대화상자)
   - [QFileDialog.getOpenFileName](#qt-qfiledialog-open) · [QFileDialog.getSaveFileName](#qt-qfiledialog-save)
7. [OpenCV 창과 PyQt5를 함께 쓰는 법](#qt-opencv-integration)
8. [코드 해설 ① 오림 (Wk09/01_Orim.py)](#qt-walkthrough-orim)
9. [코드 해설 ② 교통약자 보호 (Wk09/02_VisionAgent02.py)](#qt-walkthrough-traffic)
10. [주의할 점과 개선 방법](#qt-pitfalls)
11. [확장: 레이아웃·QLabel에 영상 표시하기](#qt-extensions)

---

<a id="qt-structure"></a>
## 1. PyQt5 프로그램의 뼈대

Wk09의 두 프로그램은 모두 다음 구조입니다.

```python
import sys
from PyQt5.QtWidgets import *          # QApplication, QMainWindow, QPushButton, QLabel, QFileDialog ...

class MyWindow(QMainWindow):           # ① 메인 창 클래스를 상속
    def __init__(self):
        super().__init__()             # ② 부모 초기화 (반드시 먼저)
        self.setWindowTitle('제목')     # ③ 창 설정
        self.setGeometry(200, 200, 700, 200)

        btn = QPushButton('버튼', self) # ④ 위젯 생성 (부모 = self)
        btn.setGeometry(10, 10, 100, 30)
        btn.clicked.connect(self.onClick)   # ⑤ 시그널 → 슬롯 연결

    def onClick(self):                 # ⑥ 버튼을 누르면 호출될 메서드(슬롯)
        ...

app = QApplication(sys.argv)           # ⑦ 애플리케이션 객체 (위젯보다 먼저!)
win = MyWindow()
win.show()                             # ⑧ 창 표시
app.exec_()                            # ⑨ 이벤트 루프 시작 (창이 닫힐 때까지 여기서 멈춤)
```

핵심 개념: **이벤트 기반(event-driven) 프로그래밍**
`app.exec_()` 이후로 프로그램은 위에서 아래로 실행되지 않고, **사용자의 클릭 같은 이벤트가 발생할 때마다 연결된 메서드가 호출**됩니다. 그래서 각 기능(파일 열기, 페인팅, 오리기…)을 메서드로 나누어 작성합니다.

> `from PyQt5.QtWidgets import *`는 수업 코드 방식입니다. 실제 프로젝트에서는 `from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFileDialog`처럼 필요한 것만 가져오는 것이 권장됩니다.

---

<a id="2-애플리케이션이벤트-루프"></a>
## 2. 애플리케이션·이벤트 루프

<a id="qt-qapplication"></a>
### `QApplication` — GUI 애플리케이션 객체

공식 문서: <https://doc.qt.io/qt-5/qapplication.html>

```python
QApplication(argv: List[str])
```

- GUI 프로그램의 **제어 흐름과 전역 설정**을 관리합니다.
- 위젯을 사용하는 프로그램에는 **정확히 하나** 있어야 하며, **어떤 위젯보다도 먼저** 만들어야 합니다. (먼저 만들지 않으면 `QWidget: Must construct a QApplication before a QWidget` 에러)
- `sys.argv`를 넘기는 것은 Qt가 명령줄 옵션(`-style` 등)을 처리할 수 있게 하기 위함입니다.

```python
app = QApplication(sys.argv)     # Wk09/01_Orim.py, Wk09/02_VisionAgent02.py
```

<a id="qt-exec"></a>
### `app.exec_()` — 이벤트 루프 실행

공식 문서: <https://doc.qt.io/qt-5/qapplication.html#exec>

```python
app.exec_() -> int
```

- 메인 이벤트 루프에 들어가 **`exit()`가 호출되거나 마지막 창이 닫힐 때까지** 이벤트(클릭, 키, 다시 그리기 등)를 처리합니다.
- 반환값은 종료 코드입니다. 그래서 흔히 `sys.exit(app.exec_())`로 씁니다.
- 파이썬 2에서 `exec`가 예약어였던 탓에 PyQt5는 `exec_()`를 제공합니다. PyQt5에서는 `app.exec()`도 동작하고(직접 확인), PyQt6에서는 `exec()`만 있습니다.

```python
app.exec_()                      # 수업 코드
sys.exit(app.exec_())            # 권장: 종료 코드를 운영체제에 전달
```

---

<a id="3-창window"></a>
## 3. 창(Window)

<a id="qt-qmainwindow"></a>
### `QMainWindow` — 메인 애플리케이션 창

공식 문서: <https://doc.qt.io/qt-5/qmainwindow.html>

- 메뉴바, 툴바, 상태바, 도킹 위젯, **중앙 위젯(central widget)** 영역을 갖춘 메인 창 클래스입니다.
- Wk09 코드는 이 기능들을 쓰지 않고, 버튼을 **절대 좌표로 창 위에 직접 배치**하는 단순한 방식을 사용합니다.
- 상속해서 `__init__`에서 화면을 구성하는 것이 일반적인 패턴입니다.

```python
class Orim(QMainWindow):          # Wk09/01_Orim.py
    def __init__(self):
        super().__init__()
```

> 메뉴/상태바가 필요 없다면 `QWidget`을 상속해도 됩니다. `QMainWindow`에서 레이아웃을 쓰려면 `setCentralWidget()`이 필요합니다([확장](#qt-extensions) 참고).

<a id="qt-setwindowtitle"></a>
### `QWidget.setWindowTitle` — 창 제목 설정

공식 문서: <https://doc.qt.io/qt-5/qwidget.html#windowTitle-prop>

```python
widget.setWindowTitle(title: str) -> None
```

```python
self.setWindowTitle('오림')            # Wk09/01_Orim.py
self.setWindowTitle('교통약자 보호')    # Wk09/02_VisionAgent02.py
```

<a id="qt-setgeometry"></a>
### `QWidget.setGeometry` — 위치와 크기 지정

공식 문서: <https://doc.qt.io/qt-5/qwidget.html#geometry-prop>

```python
widget.setGeometry(x: int, y: int, w: int, h: int) -> None
widget.setGeometry(rect: QRect) -> None
```

| 인자 | 의미 |
|---|---|
| `x, y` | 왼쪽 위 위치. **창이면 화면 기준, 자식 위젯이면 부모 위젯 기준** 좌표 |
| `w, h` | 너비, 높이 (픽셀) |

```python
# Wk09/01_Orim.py
self.setGeometry(200, 200, 700, 200)        # 화면 (200,200)에 700x200 창
fileButton.setGeometry(10, 10, 100, 30)     # 창 안 (10,10)에 100x30 버튼
paintButton.setGeometry(110, 10, 100, 30)   # x를 100씩 늘려 가로로 나란히
incButton.setGeometry(310, 10, 50, 30)      # +/- 버튼은 폭 50
```

버튼 배치 그림 (Wk09/01_Orim.py)

```
x:  10      110     210     310 360 410     510     610
    ┌──────┬──────┬──────┬───┬───┬──────┬──────┐
    │ 파일 │페인팅│ 오림 │ + │ - │ 저장 │나가기│   y = 10 ~ 40
    └──────┴──────┴──────┴───┴───┴──────┴──────┘
```

> 절대 좌표 배치는 창 크기를 바꿔도 위젯이 따라 움직이지 않습니다. 반응형 배치는 [레이아웃](#qt-extensions)을 사용하세요.

<a id="qt-show"></a>
### `QWidget.show` — 창 표시

공식 문서: <https://doc.qt.io/qt-5/qwidget.html#show>

```python
win.show()
```

위젯(과 자식들)을 화면에 보이게 합니다. 실제로 그려지는 것은 이벤트 루프(`app.exec_()`)가 돌기 시작한 뒤입니다.

<a id="qt-close"></a>
### `QWidget.close` — 창 닫기

공식 문서: <https://doc.qt.io/qt-5/qwidget.html#close>

```python
widget.close() -> bool
```

창을 닫습니다. 마지막 창이 닫히면 `QApplication`의 기본 설정(`quitOnLastWindowClosed=True`)에 따라 이벤트 루프가 끝나고 `app.exec_()`가 반환됩니다.

```python
# Wk09 공통 — OpenCV 창을 먼저 닫고 Qt 창 닫기
def quitFunction(self):
    cv.destroyAllWindows()
    self.close()
```

---

<a id="4-위젯widget"></a>
## 4. 위젯(Widget)

<a id="qt-qpushbutton"></a>
### `QPushButton` — 누름 버튼

공식 문서: <https://doc.qt.io/qt-5/qpushbutton.html> · 시그널은 부모 클래스 [QAbstractButton](https://doc.qt.io/qt-5/qabstractbutton.html#signals)

```python
QPushButton(text: str, parent: QWidget = None)
```

| 인자 | 의미 |
|---|---|
| `text` | 버튼에 표시할 글자 |
| `parent` | 부모 위젯. **`self`를 넘겨야 창 안에 표시**되고, 창이 사라질 때 함께 정리됨 |

주요 시그널 (QAbstractButton)

| 시그널 | 발생 시점 |
|---|---|
| `clicked(checked=False)` | 버튼을 눌렀다 **버튼 위에서 뗐을 때** (가장 많이 사용) |
| `pressed()` | 누르는 순간 |
| `released()` | 떼는 순간 |
| `toggled(bool)` | 체크 가능한 버튼의 상태가 바뀔 때 |

자주 쓰는 메서드: `setText(str)`, `setEnabled(bool)`, `setCheckable(bool)`, `setToolTip(str)`

```python
# Wk09/01_Orim.py — 7개 버튼 생성
fileButton = QPushButton('파일', self)
paintButton = QPushButton('페인팅', self)
cutButton  = QPushButton('오림', self)
incButton  = QPushButton('+', self)
decButton  = QPushButton('-', self)
saveButton = QPushButton('저장', self)
quitButton = QPushButton('나가기', self)
```

> 버튼은 지역 변수(`fileButton`)로 만들었지만 부모(`self`)가 참조를 가지고 있으므로 사라지지 않습니다. 나중에 버튼 상태를 바꿔야 한다면 `self.fileButton`처럼 속성으로 저장하세요.

---

<a id="qt-qlabel"></a>
### `QLabel` — 글자/이미지 표시

공식 문서: <https://doc.qt.io/qt-5/qlabel.html>

```python
QLabel(text: str = '', parent: QWidget = None)
```

사용자와 상호작용하지 않는 **텍스트나 이미지(QPixmap) 표시용** 위젯입니다. Wk09/02에서는 프로그램의 **상태 메시지 창** 역할을 합니다.

```python
# Wk09/02_VisionAgent02.py — 나중에 다른 메서드에서 바꿔야 하므로 self.label로 저장
self.label = QLabel('환영합니다!', self)
self.label.setGeometry(10, 40, 600, 170)
```

<a id="qt-settext"></a>
#### `QLabel.setText` — 표시 글자 변경

```python
label.setText(text: str) -> None
```

이전 내용을 지우고 새 글자를 표시합니다. HTML 일부(`<b>굵게</b>`)도 해석합니다.

```python
self.label.setText("교통약자 표지판을 등록합니다.")
self.label.setText(self.signFiles[best][1] + '보호구역입니다. 30km로 서행하세요.')
```

<a id="qt-clear"></a>
#### `QLabel.clear` — 내용 지우기

```python
label.clear() -> None
```

글자·이미지를 모두 지웁니다. (`setText`가 어차피 덮어쓰므로 Wk09/02의 `clear()` → `setText()` 순서에서 `clear()`는 생략해도 결과가 같습니다.)

기타 유용한 QLabel 메서드

| 메서드 | 용도 |
|---|---|
| `setAlignment(Qt.AlignCenter)` | 정렬 (`from PyQt5.QtCore import Qt`) |
| `setWordWrap(True)` | 긴 글 줄바꿈 |
| `setPixmap(QPixmap)` | 이미지 표시 ([확장](#qt-extensions) 참고) |
| `setFont(QFont('', 20))` | 글꼴 크기 변경 |

---

<a id="qt-signal-slot"></a>
## 5. 시그널과 슬롯 — 버튼 클릭 처리

공식 문서: <https://www.riverbankcomputing.com/static/Docs/PyQt5/signals_slots.html>

Qt의 이벤트 처리 방식입니다.
- **시그널(signal)**: 위젯에서 어떤 일이 일어났다는 알림 (예: `clicked`)
- **슬롯(slot)**: 그 알림을 받아 실행될 함수/메서드

```python
bound_signal.connect(slot)      # 연결 — 반환값은 Connection 객체
bound_signal.disconnect(slot)   # 연결 해제 (인자 없으면 모든 연결 해제)
bound_signal.emit(*args)        # (직접 정의한 시그널을) 발생시킴
```

- `button.clicked`처럼 **인스턴스를 통해 접근한 시그널을 bound signal**이라 하며, 여기에 `connect`/`disconnect`/`emit`이 있습니다.
- 슬롯에는 **함수 객체 자체**를 넘깁니다. `self.fileOpenFunction()`처럼 괄호를 붙이면 연결하는 순간 실행되어 버리니 주의하세요.

```python
# Wk09/01_Orim.py — 버튼 7개를 각 기능 메서드에 연결
fileButton.clicked.connect(self.fileOpenFunction)
paintButton.clicked.connect(self.paintFunction)
cutButton.clicked.connect(self.cutFunction)
incButton.clicked.connect(self.incFunction)
decButton.clicked.connect(self.decFunction)
saveButton.clicked.connect(self.saveFunction)
quitButton.clicked.connect(self.quitFunction)
```

**슬롯에 인자를 넘기고 싶을 때** — `lambda` 또는 `functools.partial`

```python
# 같은 메서드를 다른 값으로 재사용
incButton.clicked.connect(lambda: self.changeBrush(+1))
decButton.clicked.connect(lambda: self.changeBrush(-1))
```

> 공식 문서: lambda로 연결한 경우 `connect()`가 돌려준 `Connection` 객체로만 해제할 수 있습니다.
> ```python
> conn = self.button.clicked.connect(lambda checked: print("clicked"))
> self.button.clicked.disconnect(conn)
> ```

**직접 시그널 정의하기** (`pyqtSignal`, 클래스 속성으로만 정의 가능)

```python
from PyQt5.QtCore import QObject, pyqtSignal

class Detector(QObject):
    found = pyqtSignal(str)          # 문자열 하나를 싣는 시그널

det = Detector()
det.found.connect(lambda name: print(name, '발견'))
det.found.emit('어린이')
```

---

<a id="6-파일-대화상자"></a>
## 6. 파일 대화상자

공식 문서: <https://doc.qt.io/qt-5/qfiledialog.html>

<a id="qt-qfiledialog-open"></a>
### `QFileDialog.getOpenFileName` — "열기" 대화상자

```python
QFileDialog.getOpenFileName(parent=None, caption='', directory='', filter='', initialFilter='', options=0) -> (str, str)
```

| 인자 | 의미 |
|---|---|
| `parent` | 부모 창. 그 창 위에 **모달**로 가운데 정렬됨 |
| `caption` | 대화상자 제목 |
| `directory` | 시작 폴더. 파일 이름을 포함하면 그 파일이 미리 선택됨 |
| `filter` | 표시할 파일 종류. 여러 개는 `;;`로 구분 |
| `initialFilter` | 처음 선택되어 있을 필터 |

**반환값 (PyQt5 특이점)**: C++ Qt는 경로 문자열만 반환하지만, PyQt5는 **`(선택한 경로, 선택된 필터)` 튜플**을 반환합니다. 그래서 `fname[0]`으로 경로를 꺼냅니다.
**취소하면 경로가 빈 문자열 `''`** 입니다(Qt 문서: "null string").

```python
# Wk09/01_Orim.py
fname = QFileDialog.getOpenFileName(self, 'Open File', './')
self.img = cv.imread(fname[0])

# 권장: 튜플 언패킹 + 필터 + 취소 처리
path, _ = QFileDialog.getOpenFileName(self, '영상 열기', './',
                                      'Images (*.png *.jpg *.bmp);;All files (*)')
if not path:          # 사용자가 취소함
    return
```

> 플랫폼 노트(Qt 문서): Windows·macOS에서는 Qt 자체 대화상자 대신 **운영체제 기본 대화상자**가 뜹니다.

<a id="qt-qfiledialog-save"></a>
### `QFileDialog.getSaveFileName` — "저장" 대화상자

```python
QFileDialog.getSaveFileName(parent=None, caption='', directory='', filter='', initialFilter='', options=0) -> (str, str)
```

인자·반환 형식은 `getOpenFileName`과 같습니다. 차이점은 **존재하지 않는 파일 이름도 선택**할 수 있고, 이미 있는 파일을 고르면 덮어쓰기 확인을 묻는다는 것입니다. (Qt 문서: macOS에서는 `filter` 인자가 무시됨)

```python
# Wk09/01_Orim.py
fname = QFileDialog.getSaveFileName(self, '파일 저장', './')
cv.imwrite(fname[0], self.grabImg)
```

> `cv.imwrite`는 **확장자로 형식을 정하므로** 사용자가 `result`처럼 확장자 없이 입력하면 저장에 실패합니다. `if not path.lower().endswith(('.png', '.jpg')): path += '.png'` 같은 보정을 권장합니다.

---

<a id="qt-opencv-integration"></a>
## 7. OpenCV 창과 PyQt5를 함께 쓰는 법

Wk09 코드는 **두 종류의 창**을 동시에 씁니다.

| 창 | 만드는 쪽 | 역할 |
|---|---|---|
| 버튼이 있는 제어 창 | PyQt5 (`QMainWindow`) | 명령 입력 |
| `'Painting'`, `'Scissoring'`, `'Road scene'` 등 | OpenCV (`cv.imshow`) | 영상 표시·마우스 페인팅 |

동작 원리와 주의점
1. Wk02~Wk07에서는 `while True: cv.waitKey(1)` 루프가 OpenCV 창의 이벤트를 처리했습니다. Wk09에서는 그 루프가 없고 **Qt의 `app.exec_()` 이벤트 루프**가 대신 돌고 있습니다.
2. 이 프로젝트 환경(macOS + opencv-python)에서는 Qt 이벤트 루프가 같은 메인 스레드의 네이티브 이벤트를 처리하므로 `cv.imshow` 창이 표시되고 `setMouseCallback`도 동작합니다.
3. 운영체제/OpenCV 빌드에 따라 OpenCV 창이 갱신되지 않거나 멈춘 것처럼 보일 수 있습니다. 그럴 땐 `cv.imshow(...)` 직후 `cv.waitKey(1)`을 호출해 HighGUI 이벤트를 한 번 처리시키세요.
4. Linux에서는 `opencv-python`에 포함된 Qt 플러그인과 PyQt5의 Qt가 충돌(`Could not load the Qt platform plugin "xcb"`)하는 일이 잦습니다. 이 경우 `opencv-python-headless`를 설치하고 영상을 [QLabel에 직접 표시](#qt-extensions)하는 방식이 안전합니다.
5. 콜백 등록 순서: `setMouseCallback`은 **이미 존재하는 창**에만 붙일 수 있습니다. Orim에서 '파일'을 먼저 눌러 `'Painting'` 창을 만든 뒤 '페인팅'을 눌러야 하는 이유입니다.

---

<a id="qt-walkthrough-orim"></a>
## 8. 코드 해설 ① 오림 (Wk09/01_Orim.py)

**목적**: GrabCut으로 사진에서 물체를 오려 내는 GUI 도구 (교재 프로그램 6-3)

### 사용 순서

```
[파일] → 영상 선택, 'Painting' 창 표시, 마스크 초기화
   ↓
[페인팅] → 'Painting' 창에 마우스 콜백 연결
   ↓  왼쪽 드래그 = 물체(파랑, GC_FGD) / 오른쪽 드래그 = 배경(빨강, GC_BGD)
[+] / [-] → 붓 크기 1~20 조절
   ↓
[오림] → grabCut 실행, 'Scissoring' 창에 결과
   ↓
[저장] → 결과를 파일로 저장   /   [나가기] → 모든 창 닫기
```

### 버튼 ↔ 메서드 ↔ 사용 함수

| 버튼 | 메서드 | 핵심 함수 |
|---|---|---|
| 파일 | `fileOpenFunction` | [`QFileDialog.getOpenFileName`](#qt-qfiledialog-open), [`cv.imread`](opencv.md#cv-imread), [`np.copy`](numpy.md#np-copy), [`cv.imshow`](opencv.md#cv-imshow), [`np.zeros`](numpy.md#np-zeros) |
| 페인팅 | `paintFunction` → `painting` | [`cv.setMouseCallback`](opencv.md#cv-setmousecallback), [`cv.circle`](opencv.md#cv-circle) |
| 오림 | `cutFunction` | [`cv.grabCut`](opencv.md#cv-grabcut), [`np.where`](numpy.md#np-where), [`np.newaxis`](numpy.md#np-newaxis) |
| + / - | `incFunction` / `decFunction` | 파이썬 `min` / `max`로 범위 제한 |
| 저장 | `saveFunction` | [`QFileDialog.getSaveFileName`](#qt-qfiledialog-save), [`cv.imwrite`](opencv.md#cv-imwrite) |
| 나가기 | `quitFunction` | [`cv.destroyAllWindows`](opencv.md#cv-destroyallwindows), [`close`](#qt-close) |

### 핵심 부분

```python
def fileOpenFunction(self):
    fname = QFileDialog.getOpenFileName(self, 'Open File', './')
    self.img = cv.imread(fname[0])
    if self.img is None: sys.exit('파일을 찾을 수 없습니다.')

    self.img_show = np.copy(self.img)          # 화면용 복사본 (원본은 grabCut에 사용)
    cv.imshow('Painting', self.img_show)

    self.mask = np.zeros((self.img.shape[0], self.img.shape[1]), np.uint8)
    self.mask[:, :] = cv.GC_PR_BGD             # 전체를 '아마 배경'으로

def paintFunction(self):
    cv.setMouseCallback('Painting', self.painting)   # 메서드를 콜백으로 등록

def painting(self, event, x, y, flags, param):  # self + OpenCV 콜백 인자 5개
    if event == cv.EVENT_LBUTTONDOWN:
        cv.circle(self.img_show, (x, y), self.BrushSize, self.LColor, -1)
        cv.circle(self.mask,     (x, y), self.BrushSize, cv.GC_FGD, -1)
    ...
    cv.imshow('Painting', self.img_show)

def incFunction(self):
    self.BrushSize = min(20, self.BrushSize + 1)   # 최대 20
def decFunction(self):
    self.BrushSize = max(1, self.BrushSize - 1)    # 최소 1
```

**왜 `self.`에 저장하나?** 버튼마다 다른 메서드가 호출되므로, 영상(`self.img`)·마스크(`self.mask`)·결과(`self.grabImg`)처럼 **여러 메서드가 공유해야 하는 상태는 인스턴스 속성**으로 들고 있어야 합니다. (Wk03·Wk05에서 `global` 변수로 하던 일을 클래스로 정리한 것)

---

<a id="qt-walkthrough-traffic"></a>
## 9. 코드 해설 ② 교통약자 보호 (Wk09/02_VisionAgent02.py)

**목적**: 도로 영상에서 어린이·노인·장애인 보호구역 표지판을 SIFT + FLANN 매칭으로 인식하고, 결과를 `QLabel`에 안내 문구로 표시

### 사용 순서

```
[표지판 등록] → child.png / elder.png / disabled.png 읽어 각각 창에 표시
   ↓
[도로 영상 불러옴] → traffic*.jpg 선택, 'Road scene' 창 표시
   ↓
[인식] → 표지판 3개 각각과 도로 영상을 매칭
          → 좋은 매칭이 가장 많은 표지판 선택
          → 4개 미만이면 '표지판이 없습니다.'
          → 아니면 매칭 결과 창 + "○○보호구역입니다. 30km로 서행하세요." + 경고음
```

### 버튼 ↔ 메서드 ↔ 사용 함수

| 버튼 | 메서드 | 핵심 함수 |
|---|---|---|
| 표지판 등록 | `signFunction` | [`QLabel.clear`](#qt-clear)/[`setText`](#qt-settext), [`cv.imread`](opencv.md#cv-imread), [`cv.imshow`](opencv.md#cv-imshow) |
| 도로 영상 불러옴 | `roadFunction` | [`QFileDialog.getOpenFileName`](#qt-qfiledialog-open) |
| 인식 | `recognitionFunction` | [`cv.SIFT_create`](opencv.md#cv-sift-create), [`detectAndCompute`](opencv.md#cv-detectandcompute), [`DescriptorMatcher_create`](opencv.md#cv-descriptormatcher-create), [`knnMatch`](opencv.md#cv-knnmatch), [`cv.drawMatches`](opencv.md#cv-drawmatches), [`np.empty`](numpy.md#np-empty) |
| 나가기 | `quitFunction` | [`cv.destroyAllWindows`](opencv.md#cv-destroyallwindows), [`close`](#qt-close) |

### 인식 알고리즘 요약

```python
sift = cv.SIFT_create()
KD = [sift.detectAndCompute(cv.cvtColor(s, cv.COLOR_BGR2GRAY), None)   # 표지판별 (kp, des)
      for s in self.signImgs]
road_kp, road_des = sift.detectAndCompute(cv.cvtColor(self.roadImg, cv.COLOR_BGR2GRAY), None)

matcher = cv.DescriptorMatcher_create(cv.DescriptorMatcher_FLANNBASED)
GM = []                                         # 표지판별 good match 리스트
for sign_kp, sign_des in KD:
    knn_match = matcher.knnMatch(sign_des, road_des, 2)
    good = [a for a, b in knn_match if a.distance / b.distance < 0.7]   # ratio test
    GM.append(good)

best = GM.index(max(GM, key=len))               # good match가 가장 많은 표지판의 인덱스
if len(GM[best]) < 4:                           # 4개 미만이면 신뢰 불가
    self.label.setText('표지판이 없습니다.')
else:
    ...
    self.label.setText(self.signFiles[best][1] + '보호구역입니다. 30km로 서행하세요.')
```

- `max(GM, key=len)`: 리스트들 중 **길이가 가장 긴 것**을 찾음 → `GM.index(...)`로 그 위치를 얻음
- 4개 기준: 이후 호모그래피(`cv.findHomography`)를 구하려면 최소 4쌍의 대응점이 필요하기 때문
- `winsound.Beep`은 Windows 전용이라 macOS에서는 `print('\a')`(터미널 벨)로 대체

---

<a id="qt-pitfalls"></a>
## 10. 주의할 점과 개선 방법

수업 코드를 직접 실행·수정할 때 마주칠 수 있는 문제들입니다. (코드는 수정하지 않았고, 문서에만 정리했습니다.)

| # | 파일 | 상황 | 결과 | 개선 |
|---|---|---|---|---|
| 1 | 01_Orim | '파일' 대화상자에서 **취소** | `cv.imread('')` → `None` → `sys.exit`로 **프로그램 전체 종료** | `if not path: return` 으로 취소 처리 |
| 2 | 01_Orim | '오림' 전에 **'저장'** 클릭 | `self.grabImg` 없음 → `AttributeError` | `__init__`에서 `self.grabImg = None` 후 검사 |
| 3 | 01_Orim | '파일' 전에 '페인팅' 클릭 | `'Painting'` 창이 없는 상태라 콜백이 의도대로 붙지 않음(환경에 따라 에러 또는 빈 창) | `hasattr(self, 'img')` 검사 |
| 4 | 01_Orim | 전경/배경 중 한쪽만 칠하고 '오림' | `cv.grabCut` 에러 | 두 레이블이 모두 있는지 확인 후 실행 |
| 5 | 02_VisionAgent | 도로 영상 없이 **'인식'** 클릭 | `self.roadImg`가 `__init__`에 없어 `AttributeError` (의도한 안내 문구가 안 나옴) | `__init__`에 `self.roadImg = None` 추가 |
| 6 | 02_VisionAgent | '표지판 등록'을 **두 번** 클릭 | `signImgs`가 6개로 늘어 `best`가 3 이상이면 `self.signFiles[best]`에서 `IndexError` | 등록 시작 시 `self.signImgs = []`로 초기화 |
| 7 | 02_VisionAgent | `recognitionFunction`의 들여쓰기 | 도로 영상 SIFT·매칭·표시가 `for img in self.signImgs:` **안쪽**에 있어 표지판 수만큼 반복 실행됨(마지막 반복 결과만 남으므로 최종 결과는 같지만 3배 느림) | 도로 영상 처리 이후 부분을 `for` 밖으로 내어쓰기 |
| 8 | 공통 | `sys.exit()`를 GUI 콜백 안에서 호출 | 오류 하나로 앱 전체 종료 | `QMessageBox.warning(self, '오류', '파일을 읽을 수 없습니다.')` 로 알리고 `return` |

#7 개선 예시

```python
def recognitionFunction(self):
    if self.roadImg is None:
        self.label.setText('먼저 도로 영상을 입력하세요.')
        return

    sift = cv.SIFT_create()
    KD = [sift.detectAndCompute(cv.cvtColor(img, cv.COLOR_BGR2GRAY), None)
          for img in self.signImgs]                         # 표지판 특징은 여기서 한 번만
    grayRoad = cv.cvtColor(self.roadImg, cv.COLOR_BGR2GRAY)
    road_kp, road_des = sift.detectAndCompute(grayRoad, None)   # 도로 영상도 한 번만

    matcher = cv.DescriptorMatcher_create(cv.DescriptorMatcher_FLANNBASED)
    GM = []
    for sign_kp, sign_des in KD:
        knn_match = matcher.knnMatch(sign_des, road_des, 2)
        GM.append([a for a, b in knn_match if a.distance / b.distance < 0.7])

    best = GM.index(max(GM, key=len))
    ...   # 이하 동일 (for 밖)
```

`QMessageBox` 사용 예 (공식 문서: <https://doc.qt.io/qt-5/qmessagebox.html>)

```python
from PyQt5.QtWidgets import QMessageBox
QMessageBox.warning(self, '알림', '먼저 표지판을 등록하세요.')          # 경고 창
ans = QMessageBox.question(self, '종료', '정말 나갈까요?')               # 예/아니오
if ans == QMessageBox.Yes:
    self.close()
```

---

<a id="qt-extensions"></a>
## 11. 확장: 레이아웃·QLabel에 영상 표시하기

수업 코드에는 없지만, Wk09 GUI를 발전시킬 때 바로 쓸 수 있는 공식 API입니다.

### 레이아웃으로 버튼 자동 배치

공식 문서: <https://doc.qt.io/qt-5/qboxlayout.html>

```python
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout

central = QWidget()
vbox = QVBoxLayout(central)          # 세로 배치
hbox = QHBoxLayout()                 # 가로 배치 (버튼 줄)
for b in (fileButton, paintButton, cutButton):
    hbox.addWidget(b)
vbox.addLayout(hbox)
vbox.addWidget(self.label)
self.setCentralWidget(central)       # QMainWindow는 중앙 위젯에 레이아웃을 둠
```

→ `setGeometry`로 좌표를 하나하나 계산할 필요가 없고, 창 크기를 바꾸면 위젯도 따라 늘어납니다.

### OpenCV 영상을 QLabel에 표시

공식 문서: [QImage](https://doc.qt.io/qt-5/qimage.html) · [QPixmap](https://doc.qt.io/qt-5/qpixmap.html)

```python
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap

def show_on_label(label, img_bgr):
    h, w = img_bgr.shape[:2]
    qimg = QImage(img_bgr.data, w, h, img_bgr.strides[0], QImage.Format_BGR888)  # Qt 5.14+
    pix = QPixmap.fromImage(qimg)
    label.setPixmap(pix.scaled(label.width(), label.height(), Qt.KeepAspectRatio))
```

- `img_bgr.strides[0]`(한 행의 바이트 수)를 넘겨야 너비가 4의 배수가 아닐 때 영상이 기울어지지 않습니다.
- `QImage`는 NumPy 메모리를 복사하지 않고 참조하므로, 배열이 사라지기 전에 `QPixmap.fromImage`로 변환하세요.
- 1채널 영상은 `QImage.Format_Grayscale8`을 사용합니다.

[↑ 맨 위로](#pyqt5-gui-레퍼런스-wk09-중점) · [← 전체 목차로](README.md)
