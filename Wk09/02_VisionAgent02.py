# [전체 목적] 교통약자(어린이/노인/장애인) 표지판 이미지를 미리 등록해 두고,
#  도로 영상에서 SIFT 특징점 + FLANN 매칭으로 어떤 표지판이 있는지 찾아 안내 메시지를 띄우는 프로그램.

import cv2 as cv
import numpy as np
from PyQt5.QtWidgets import *
import sys
# import winsound


class TrafficWeak(QMainWindow):
    # [역할] 프로그램 전체를 담는 메인 윈도우 클래스.
    #  등록한 표지판(self.signImgs), 도로 영상(self.roadImg), 안내 라벨(self.label)을 버튼 함수들이 공유하기 위해 클래스로 정의.
    def __init__(self):
        # [역할] 윈도우/버튼/안내 라벨을 만들고 버튼과 기능 함수를 연결, 표지판 파일 목록을 초기화한다.
        super().__init__()
        self.setWindowTitle('교통약자 보호')
        self.setGeometry(200, 200, 700, 200)

        signButton = QPushButton('표지판 등록', self)
        roadButton = QPushButton('도로 영상 불러옴', self)
        recognitionButton = QPushButton('인식', self)
        quitButton = QPushButton('나가기', self)
        self.label = QLabel('환영합니다!', self)   # 사용자에게 상태/결과를 보여주는 안내 문구

        signButton.setGeometry(10, 10, 100, 30)
        roadButton.setGeometry(110, 10, 100, 30)
        recognitionButton.setGeometry(210, 10, 100, 30)
        quitButton.setGeometry(510, 10, 100, 30)
        self.label.setGeometry(10, 40, 600, 170)

        # 버튼 클릭 → 해당 기능 함수 실행
        signButton.clicked.connect(self.signFunction)
        roadButton.clicked.connect(self.roadFunction)
        recognitionButton.clicked.connect(self.recognitionFunction)
        quitButton.clicked.connect(self.quitFunction)

        # [파일명, 안내문에 쓸 이름] 쌍. 인덱스가 곧 signImgs/매칭 결과의 인덱스와 대응된다.
        self.signFiles = [
            ['child.png', '어린이'],
            ['elder.png', '노인'],
            ['disabled.png', '장애인']
        ]
        self.signImgs = []   # 읽어 들인 표지판 영상 저장 리스트

    def signFunction(self):
        # [역할] 표지판 파일들을 읽어 메모리에 등록하고 화면에 보여준다. (인식의 "비교 기준" 준비 단계)
        self.label.clear()
        self.label.setText("교통약자 표지판을 등록합니다.")

        for fname,_ in self.signFiles:
            self.signImgs.append(cv.imread(fname))      # 영상 읽어 리스트에 추가
            cv.imshow(fname, self.signImgs[-1])         # 방금 읽은 표지판 표시

    def roadFunction(self):
        # [역할] 표지판 등록 여부를 확인한 뒤, 인식 대상인 도로 영상을 파일 대화상자로 불러온다.
        if self.signImgs == []:
            # 표지판이 없으면 비교할 대상이 없으므로 먼저 등록하도록 안내
            self.label.setText("먼저 표지판을 등록하세요.")
        else:
            fname = QFileDialog.getOpenFileName(self, '파일읽기', './')
            self.roadImg = cv.imread(fname[0])
            if self.roadImg is None:
                sys.exit('파일을 찾을 수 없습니다.')

            cv.imshow('Road scene', self.roadImg)

    def recognitionFunction(self):
        # [역할] 핵심 기능. 도로 영상과 각 표지판의 SIFT 특징점을 FLANN으로 매칭하고,
        #  좋은 매칭이 가장 많은 표지판을 선택해 결과(매칭 그림·안내문·경고음)를 출력한다.
        if self.roadImg is None:
            self.label.setText('먼저 도로 영상을 입력하세요.')
        else:
            sift = cv.SIFT_create()   # 특징점 검출 + 기술자 계산기

            KD = []   # 표지판별 (특징점, 기술자) 저장
            for img in self.signImgs:
                # 1) 표지판 / 도로 영상의 특징점과 기술자 추출 (흑백 변환 후 SIFT)
                gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
                KD.append(sift.detectAndCompute(gray, None))
                grayRaod = cv.cvtColor(self.roadImg, cv.COLOR_BGR2GRAY)
                road_kp, road_des = sift.detectAndCompute(grayRaod, None)

                # 2) FLANN 기반 매처로 기술자 간 가장 비슷한 점 찾기
                matcher = cv.DescriptorMatcher_create(cv.DescriptorMatcher_FLANNBASED)
                GM = []   # 표지판별 "좋은 매칭" 리스트
                for sign_kp, sign_des in KD:
                    knn_match = matcher.knnMatch(sign_des, road_des, 2)   # 각 점마다 가장 가까운 2개 후보
                    T = 0.7   # 거리비 임계값
                    good_match = []
                    # 3) 비율 테스트: 1순위가 2순위보다 확실히 가까울 때만 신뢰할 수 있는 매칭으로 채택
                    for nearest1, nearest2 in knn_match:
                        if (nearest1.distance / nearest2.distance) < T :
                            good_match.append(nearest1)
                    GM.append(good_match)

                # 4) 좋은 매칭이 가장 많은 표지판 = 도로 영상에 가장 닮은 표지판
                best = GM.index(max(GM, key=len))

                if len(GM[best]) < 4:
                    # 매칭이 너무 적으면(4개 미만) 표지판이 없다고 판단
                    self.label.setText('표지판이 없습니다.')
                else:
                    sign_kp = KD[best][0]
                    good_match = GM[best]

                    # 5) 매칭 결과를 나란히 그릴 캔버스 크기 계산 (높이는 큰 쪽, 너비는 합)
                    h1, w1 = self.signImgs[best].shape[0], self.signImgs[best].shape[1]
                    h2, w2 = self.roadImg.shape[0], self.roadImg.shape[1]

                    img_match = np.empty((max(h1, h2), w1+w2, 3), dtype=np.uint8)
                    # 표지판-도로 영상 사이 대응점을 선으로 연결해 시각화
                    cv.drawMatches(
                        self.signImgs[best],
                        sign_kp,
                        self.roadImg,
                        road_kp,
                        good_match,
                        img_match,
                        flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
                    )

                    cv.imshow('Matches and Homography', img_match)

                    # 6) 인식된 표지판 종류에 맞는 안내문 + 경고음
                    self.label.setText(self.signFiles[best][1] + '보호구역입니다. 30km로 서행하세요.')
                    # winsound.Beep(3000, 500)
                    # 맥에서는 winsound 가 임포트 되지 않음. (winsound가 윈도우 전용 모듈이기 때문에)
                    print('\a')

    def quitFunction(self):
        # [역할] 열려 있는 OpenCV 창을 모두 닫고 GUI 윈도우도 종료한다.
        cv.destroyAllWindows()
        self.close()

# 프로그램 시작부: Qt 앱 생성 → 윈도우 표시 → 이벤트 루프 실행(버튼 입력 대기)
app = QApplication(sys.argv)
win = TrafficWeak()
win.show()
app.exec_()
