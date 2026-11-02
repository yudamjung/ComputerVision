# 프로그램 6-3
# [전체 목적] GrabCut 알고리즘으로 영상에서 원하는 물체만 오려내는(배경 제거) GUI 프로그램.
#  사용자가 마우스로 "이건 물체(전경)", "이건 배경"이라고 힌트를 칠해주면 GrabCut이 나머지를 알아서 분할한다.

import cv2 as cv
import numpy as np
import sys
from PyQt5.QtWidgets import *

class Orim(QMainWindow):
    # [역할] 프로그램 전체를 담는 메인 윈도우 클래스.
    #  버튼들과 상태값(붓 크기, 색)을 한 객체에 묶어 두어, 각 버튼 함수들이 self.img, self.mask 등을 공유하게 하려고 클래스로 정의.
    def __init__(self):
        # [역할] 윈도우 생성, 버튼 배치, 버튼-함수 연결, 초기 상태값 설정 (GUI 초기화).
        super().__init__()
        self.setWindowTitle('오림')
        self.setGeometry(200, 200, 700, 200)

        # 기능별 버튼 생성
        fileButton = QPushButton('파일', self)
        paintButton = QPushButton('페인팅', self)
        cutButton = QPushButton('오림', self)
        incButton = QPushButton('+', self)
        decButton = QPushButton('-', self)
        saveButton = QPushButton('저장', self)
        quitButton = QPushButton('나가기', self)

        # 버튼 위치/크기 지정
        fileButton.setGeometry(10, 10, 100, 30)
        paintButton.setGeometry(110, 10, 100, 30)
        cutButton.setGeometry(210, 10, 100, 30)
        incButton.setGeometry(310, 10, 50, 30)
        decButton.setGeometry(360, 10, 50, 30)
        saveButton.setGeometry(410, 10, 100, 30)
        quitButton.setGeometry(510, 10, 100, 30)

        # 버튼 클릭 시 실행할 함수 연결 (시그널-슬롯)
        fileButton.clicked.connect(self.fileOpenFunction)
        paintButton.clicked.connect(self.paintFunction)
        cutButton.clicked.connect(self.cutFunction)
        incButton.clicked.connect(self.incFunction)
        decButton.clicked.connect(self.decFunction)
        saveButton.clicked.connect(self.saveFunction)
        quitButton.clicked.connect(self.quitFunction)

        self.BrushSize = 5          # 붓(원) 반지름 초기값
        self.LColor = (255, 0, 0)   # 왼쪽 버튼 = 전경 표시색 (파랑, BGR)
        self.RColor = (0, 0, 255)   # 오른쪽 버튼 = 배경 표시색 (빨강, BGR)

    def fileOpenFunction(self):
        # [역할] 분할할 영상을 파일 대화상자로 골라 읽고, 그림 그릴 화면용 복사본과 GrabCut용 마스크를 준비한다.
        fname = QFileDialog.getOpenFileName(self, 'Open File', './')   # 파일 선택 창
        self.img = cv.imread(fname[0])
        if self.img is None: sys.exit('파일을 찾을 수 없습니다.')   # 읽기 실패 시 종료

        # 원본(self.img)은 GrabCut 입력으로 보존하고, 붓칠은 복사본(img_show)에만 그린다.
        self.img_show = np.copy(self.img)
        cv.imshow('Painting', self.img_show)

        # 마스크: 영상과 같은 크기의 1채널 배열. 전부 "아마도 배경(PR_BGD)"으로 초기화
        #  → 사용자가 칠한 곳만 확실한 전경/배경으로 덮어쓰이고 나머지는 GrabCut이 판단.
        self.mask = np.zeros((self.img.shape[0], self.img.shape[1]), np.uint8)
        self.mask[:,:] = cv.GC_PR_BGD

    def paintFunction(self):
        # [역할] '페인팅' 버튼을 누르면 Painting 창에 마우스 콜백(painting)을 등록해 붓칠을 가능하게 한다.
        cv.setMouseCallback('Painting', self.painting)

    def painting(self, event, x, y, flags, param):
        # [역할] 마우스 이벤트마다 호출되어, 화면에는 색 원을, 마스크에는 전경/배경 라벨을 동시에 기록한다.
        #  (화면 = 사용자가 보는 표시용, 마스크 = GrabCut이 실제로 쓰는 힌트)
        if event == cv.EVENT_LBUTTONDOWN:
            # 왼쪽 클릭 → 전경(GC_FGD) 힌트
            cv.circle(self.img_show, (x, y), self.BrushSize, self.LColor, -1)  # 왼쪽 버튼 클릭하면 파랑
            cv.circle(self.mask, (x, y), self.BrushSize, cv.GC_FGD, -1)

        elif event == cv.EVENT_RBUTTONDOWN:
            # 오른쪽 클릭 → 배경(GC_BGD) 힌트
            cv.circle(self.img_show, (x, y), self.BrushSize, self.RColor, -1)  # 오른쪽 버튼 클릭하면 빨강
            cv.circle(self.mask, (x, y), self.BrushSize, cv.GC_BGD, -1)

        elif event == cv.EVENT_MOUSEMOVE and flags == cv.EVENT_FLAG_LBUTTON:
            # 왼쪽 버튼 누른 채 드래그 → 연속으로 전경 칠하기
            cv.circle(self.img_show, (x, y), self.BrushSize, self.LColor, -1)  # 왼쪽 버튼 클릭하고 이동하면 파랑
            cv.circle(self.mask, (x, y), self.BrushSize, cv.GC_FGD, -1)

        elif event == cv.EVENT_MOUSEMOVE and flags == cv.EVENT_FLAG_RBUTTON:
            # 오른쪽 버튼 누른 채 드래그 → 연속으로 배경 칠하기
            cv.circle(self.img_show, (x, y), self.BrushSize, self.RColor, -1)
            cv.circle(self.mask, (x, y), self.BrushSize, cv.GC_BGD, -1)

        cv.imshow('Painting', self.img_show)   # 칠한 결과를 즉시 화면에 갱신


    def cutFunction(self):
        # [역할] 사용자가 칠한 마스크를 초기값으로 GrabCut을 실행해 전경만 남기고 배경은 검게 만든다. (핵심 기능)
        # GrabCut 내부 모델(GMM) 저장용 임시 배열. 크기 (1,65)는 OpenCV 규격.
        background = np.zeros((1,65), np.float64)
        foreground = np.zeros((1,65), np.float64)

        # 마스크를 초기 조건으로(GC_INIT_WITH_MASK) 5회 반복하여 전경/배경 분할. 결과는 self.mask에 갱신됨.
        cv.grabCut(self.img, self.mask, None, background, foreground, 5, cv.GC_INIT_WITH_MASK)

        # 배경(0)·아마도배경(2)은 0, 전경(1)·아마도전경(3)은 1인 이진 마스크로 변환
        mask2 = np.where((self.mask == 2) | (self.mask == 0), 0, 1).astype('uint8')
        # 원본에 마스크를 곱해 배경 픽셀을 0(검정)으로 → 오려낸 영상. (채널 축 추가해 3채널에 브로드캐스팅)
        self.grabImg = self.img * mask2[:, :, np.newaxis]
        cv.imshow('Scissoring', self.grabImg)

    def incFunction(self):
        # [역할] 붓 크기를 1 키우되 최대 20으로 제한 (너무 커지지 않도록 min 사용).
        self.BrushSize = min(20, self.BrushSize+1)

    def decFunction(self):
        # [역할] 붓 크기를 1 줄이되 최소 1로 제한 (0 이하가 되지 않도록 max 사용).
        self.BrushSize = max(1, self.BrushSize-1)

    def saveFunction(self):
        # [역할] 오려낸 결과(self.grabImg)를 사용자가 지정한 경로에 이미지 파일로 저장한다.
        fname = QFileDialog.getSaveFileName(self, '파일 저장', './')   # 저장 경로 선택 창
        cv.imwrite(fname[0], self.grabImg)

    def quitFunction(self):
        # [역할] 열려 있는 OpenCV 창을 모두 닫고 GUI 윈도우도 종료한다.
        cv.destroyAllWindows()
        self.close()

# 프로그램 시작부: Qt 앱 생성 → 윈도우 표시 → 이벤트 루프 실행(버튼/마우스 입력 대기)
app = QApplication(sys.argv)
win = Orim()
win.show()
app.exec_()
