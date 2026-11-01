<a id="파이썬-표준-라이브러리내장-함수"></a>
# 파이썬 표준 라이브러리·내장 함수

> 공식 문서: <https://docs.python.org/3/library/>
> 프로젝트 요구 버전: Python ≥ 3.11

[← 전체 목차로](README.md)

## 목차

- [`sys.exit` — 프로그램 종료](#py-sys-exit)
- [`sys.argv` — 명령줄 인자](#py-sys-argv)
- [`time.time` — 실행 시간 측정](#py-time)
- [`ord` — 문자 → 키 코드](#py-ord)
- [`max(..., key=)` / `list.index` — 가장 좋은 후보 고르기](#py-max-key)

---

<a id="py-sys-exit"></a>
## `sys.exit` — 프로그램 종료

공식 문서: <https://docs.python.org/3/library/sys.html#sys.exit>

```python
sys.exit([arg])
```

`SystemExit` 예외를 발생시켜 종료합니다. 문자열을 넘기면 **stderr에 출력하고 종료 코드 1**로 끝납니다.

```python
img = cv.imread('soccer.jpg')
if img is None:
    sys.exit('파일을 찾을 수 없습니다.')     # Wk02 ~ Wk09 공통 패턴
```

> GUI 프로그램(Wk09)의 버튼 콜백 안에서 호출하면 창 전체가 꺼집니다. GUI에서는 [QMessageBox](pyqt5_gui.md#qt-pitfalls)로 알리고 `return` 하는 편이 낫습니다.

<a id="py-sys-argv"></a>
## `sys.argv` — 명령줄 인자

공식 문서: <https://docs.python.org/3/library/sys.html#sys.argv>

스크립트 이름과 명령줄 인자가 담긴 리스트. `QApplication`에 넘겨 Qt가 옵션을 해석하게 합니다.

```python
app = QApplication(sys.argv)     # Wk09
```

<a id="py-time"></a>
## `time.time` — 실행 시간 측정

공식 문서: <https://docs.python.org/3/library/time.html#time.time>

```python
time.time() -> float     # 1970-01-01 이후 경과 초
```

```python
# Wk05/02_normalized_cut.py, Wk07/02_FLANN.py
start = time.time()
...
print(f'매칭에 걸린 시간 : {time.time() - start}')
```

> 짧은 구간의 정밀 측정에는 `time.perf_counter()`가 권장됩니다.

<a id="py-ord"></a>
## `ord` — 문자 → 키 코드

공식 문서: <https://docs.python.org/3/library/functions.html#ord>

```python
ord('q')   # 113
```

`cv.waitKey()`가 돌려주는 키 코드와 비교할 때 사용합니다.

```python
if cv.waitKey(1) == ord('q'):    # Wk03, Wk05
    break
```

<a id="py-max-key"></a>
## `max(..., key=)` / `list.index` — 가장 좋은 후보 고르기

공식 문서: [max](https://docs.python.org/3/library/functions.html#max) · [list.index](https://docs.python.org/3/tutorial/datastructures.html#more-on-lists)

```python
# Wk09/02_VisionAgent02.py — good match 리스트 중 가장 긴 것의 위치
best = GM.index(max(GM, key=len))

# 같은 결과, 한 번에
best = max(range(len(GM)), key=lambda i: len(GM[i]))
```

[↑ 맨 위로](#파이썬-표준-라이브러리내장-함수) · [← 전체 목차로](README.md)
