<a id="scikit-image-함수-레퍼런스"></a>
# scikit-image 함수 레퍼런스

> 대상 버전: **scikit-image 0.26.0** (`import skimage`)
> 공식 문서: <https://scikit-image.org/docs/stable/api/api.html>
> Wk05(슈퍼화소·정규화 절단)와 Wk06(예제 영상)에서 사용했습니다.
> **주의: scikit-image 영상은 RGB 순서**입니다. OpenCV로 표시할 때는 `cv.cvtColor(img, cv.COLOR_RGB2BGR)`가 필요합니다.

[← 전체 목차로](README.md)

## 목차

- [`skimage.data` — 내장 예제 영상 (`coffee`, `horse`)](#sk-data)
- [`skimage.segmentation.slic` — SLIC 슈퍼화소 분할](#sk-slic)
- [`skimage.segmentation.mark_boundaries` — 영역 경계 표시](#sk-mark-boundaries)
- [`skimage.graph.rag_mean_color` — 영역 인접 그래프(RAG) 생성](#sk-rag-mean-color)
- [`skimage.graph.cut_normalized` — 정규화 절단](#sk-cut-normalized)

---

<a id="sk-data"></a>
## `skimage.data` — 내장 예제 영상

공식 문서: <https://scikit-image.org/docs/stable/api/skimage.data.html>

파일 없이 바로 쓸 수 있는 표준 테스트 영상입니다. (일부는 첫 호출 때 내려받아 캐시)

| 함수 | 반환 (직접 확인) | 사용 |
|---|---|---|
| `skimage.data.coffee()` | `(400, 600, 3)` `uint8` **RGB** 커피잔 | Wk05/01, Wk05/02 |
| `skimage.data.horse()` | `(328, 400)` **`bool`** 말 실루엣 (말=False, 배경=True) | Wk06/01 |

```python
# Wk05/01_slic.py
img = skimage.data.coffee()
cv.imshow('Coffee image', cv.cvtColor(img, cv.COLOR_RGB2BGR))

# Wk06/01_contours.py — bool을 uint8 0/255로 바꾸고 반전해 '말=흰색' 이진 영상으로
original = skimage.data.horse()
img = 255 - np.uint8(original) * 255
```

<a id="sk-slic"></a>
## `skimage.segmentation.slic` — SLIC 슈퍼화소 분할

공식 문서: <https://scikit-image.org/docs/stable/api/skimage.segmentation.html#skimage.segmentation.slic>

```python
skimage.segmentation.slic(image, n_segments=100, compactness=10.0, max_num_iter=10, sigma=0,
                          spacing=None, convert2lab=None, enforce_connectivity=True,
                          min_size_factor=0.5, max_size_factor=3, slic_zero=False,
                          start_label=1, mask=None, *, channel_axis=-1) -> labels
```

색과 위치가 비슷한 화소를 묶어 작은 영역(**슈퍼화소**)들로 나눕니다.

| 인자 | 의미 |
|---|---|
| `n_segments` | 만들 영역의 **대략적인** 개수 |
| `compactness` | 색 유사도 vs 공간 근접성 균형. **클수록 네모반듯**, 작을수록 물체 경계를 잘 따라감 |
| `start_label` | 레이블 시작 번호 (기본 1) |
| `channel_axis` | 채널 축 위치. 회색조면 `None` |

반환값: 입력과 같은 `(H, W)` 크기의 **정수 레이블 배열** (화소마다 영역 번호)

```python
# Wk05/01_slic.py
slic1 = skimage.segmentation.slic(img, compactness=40, n_segments=600)

# Wk05/02_normalized_cut.py
slic = skimage.segmentation.slic(coffee, compactness=20, n_segments=600, start_label=1)
```

> Wk05/01_slic.py의 창 제목은 'compact 20'이지만 실제 `slic1`도 `compactness=40`으로 호출되어 두 결과가 같습니다. 비교 실험을 하려면 `slic1`의 값을 20으로 바꾸세요.

<a id="sk-mark-boundaries"></a>
## `skimage.segmentation.mark_boundaries` — 영역 경계 표시

공식 문서: <https://scikit-image.org/docs/stable/api/skimage.segmentation.html#skimage.segmentation.mark_boundaries>

```python
skimage.segmentation.mark_boundaries(image, label_img, color=(1, 1, 0), outline_color=None,
                                     mode='outer', background_label=0) -> marked
```

| 인자 | 의미 |
|---|---|
| `label_img` | `slic` 등이 만든 레이블 배열 |
| `color` | 경계선 색 RGB, **0~1 범위** (기본 노랑) |
| `mode` | `'thick'`, `'inner'`, `'outer'`(기본), `'subpixel'` |

반환값: **0~1 범위의 `float` RGB 영상**. OpenCV로 보려면 0~255 `uint8`로 변환해야 합니다.

```python
# Wk05/01_slic.py
sp_img1 = skimage.segmentation.mark_boundaries(img, slic1)
sp_img1 = np.uint8(sp_img1 * 255.0)
cv.imshow('Super pixels', cv.cvtColor(sp_img1, cv.COLOR_RGB2BGR))
```

<a id="sk-rag-mean-color"></a>
## `skimage.graph.rag_mean_color` — 영역 인접 그래프(RAG)

공식 문서: <https://scikit-image.org/docs/stable/api/skimage.graph.html#skimage.graph.rag_mean_color>

```python
skimage.graph.rag_mean_color(image, labels, connectivity=2, mode='distance', sigma=255.0) -> RAG
```

각 영역을 **노드**, 맞닿은 영역 쌍을 **간선**으로 하는 그래프를 만들고, 간선 가중치를 두 영역의 **평균 색 차이**로 정합니다.

| 인자 | 의미 |
|---|---|
| `labels` | 영역 레이블 (보통 `slic` 결과) |
| `connectivity` | 인접 판정 (1: 4-이웃, 2: 8-이웃) |
| `mode` | `'distance'`: 가중치 = 색 거리 / **`'similarity'`: 가중치 = exp(−d²/σ)** (유사할수록 큼) |

`cut_normalized`는 **유사도 그래프**를 입력으로 받으므로 `mode='similarity'`로 만들어야 합니다.

```python
# Wk05/02_normalized_cut.py
g = skimage.graph.rag_mean_color(coffee, slic, mode='similarity')
```

<a id="sk-cut-normalized"></a>
## `skimage.graph.cut_normalized` — 정규화 절단

공식 문서: <https://scikit-image.org/docs/stable/api/skimage.graph.html#skimage.graph.cut_normalized>

```python
skimage.graph.cut_normalized(labels, rag, thresh=0.001, num_cuts=10, in_place=True,
                             max_edge=1.0, *, rng=None) -> new_labels
```

RAG를 **정규화 절단(Normalized Cut)** 으로 재귀적으로 둘로 나눠, 슈퍼화소들을 더 큰 의미 있는 영역으로 합칩니다.

| 인자 | 의미 |
|---|---|
| `thresh` | 이 값보다 절단 비용이 작을 때만 계속 분할. **작을수록 덜 쪼갬** |
| `num_cuts` | 최적 분할을 찾을 때 시도할 후보 수 |
| `in_place` | `True`면 `rag`를 직접 수정 |

반환값: 새 레이블 배열 `(H, W)`

```python
# Wk05/02_normalized_cut.py
ncut = skimage.graph.cut_normalized(slic, g)
marking = skimage.segmentation.mark_boundaries(coffee, ncut)
print('분리된 영역의 개수: ', np.unique(ncut).size)
```

> 계산량이 많아 수 초가 걸립니다. 코드에서 `time.time()`으로 소요 시간을 측정합니다.

[↑ 맨 위로](#scikit-image-함수-레퍼런스) · [← 전체 목차로](README.md)
