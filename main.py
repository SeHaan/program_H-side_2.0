"""
ver 2.0.0 - 20230308
================================================================
                       업데이트 내역
----------------------------------------------------------------
ver. 2.0.0 조합형 문자열 칼럼 출력 삭제, 저장 디렉토리 추가 20230308
ver. 1.1.1 조합형 문자열도 출력하도록 수정 20220519
ver. 1.1.0 Initial Commit 20220322
ver. 1.0.5 자소검색 와일드카드 문자(*) 오류 수정 20220322
ver. 1.0.4 에러 핸들링: QMessageBox 20220322
ver. 1.0.3 판다스 데이터프레임을 딕셔너리로 변환 20220322
ver. 1.0.2 자소검색 기능 추가 20220322
ver. 1.0.1 검색 스트링을 첫가끝으로 변환 20220317
ver. 1.0.0 Initial Setting 20220309
================================================================
"""
#%%
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, \
    QFileDialog, QLineEdit, QWidget, QPushButton, QTextEdit, QHBoxLayout, \
    QVBoxLayout, QLabel, QMessageBox
from searching import *
import pickle

with open('dict/dict_0_TOTAL.pickle', 'rb') as f:
    dict_0_TOTAL = pickle.load(f)
with open('dict/dict_0_ONSET.pickle', 'rb') as fo:
    dict_0_ONSET = pickle.load(fo)
with open('dict/dict_0_PEAK.pickle', 'rb') as fp:
    dict_0_PEAK = pickle.load(fp)
with open('dict/dict_0_CODA.pickle', 'rb') as fc:
    dict_0_CODA = pickle.load(fc)

class Search(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # setting widgets
        direcLable = QLabel('data dir')
        direcLine = QLineEdit()
        findBtn = QPushButton(text="find dir")

        saveLabel = QLabel('save dir')
        saveLine = QLineEdit()
        saveBtn = QPushButton(text="find dir")

        targetLabel = QLabel('target word')
        targetWord = QLineEdit()
        searchBtn = QPushButton(text='search')

        findRes = QTextEdit()

        # style
        font_init = direcLine.font()
        font_init.setPointSize(15)
        font_init.setFamilies(['Times New Roman', 'Malgun Gothic'])

        direcLable.setFont(font_init)
        direcLine.setFont(font_init)
        findBtn.setFont(font_init)

        saveLabel.setFont(font_init)
        saveLine.setFont(font_init)
        saveBtn.setFont(font_init)

        targetLabel.setFont(font_init)
        targetWord.setFont(font_init)
        searchBtn.setFont(font_init)

        findRes.setFont(font_init)

        # setting box
        hbox_1 = QHBoxLayout()
        hbox_1.addWidget(direcLable)
        hbox_1.addWidget(direcLine)
        hbox_1.addWidget(findBtn)

        hbox_2 = QHBoxLayout()
        hbox_2.addWidget(saveLabel)
        hbox_2.addWidget(saveLine)
        hbox_2.addWidget(saveBtn)

        hbox_3 = QHBoxLayout()
        hbox_3.addWidget(targetLabel)
        hbox_3.addWidget(targetWord)
        hbox_3.addWidget(searchBtn)

        hbox_4 = QHBoxLayout()
        hbox_4.addWidget(findRes)
        
        vbox = QVBoxLayout()
        vbox.addLayout(hbox_1)
        vbox.addLayout(hbox_2)
        vbox.addLayout(hbox_3)
        vbox.addLayout(hbox_4)

        self.setLayout(vbox)
        

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):        
        wg = Search()
        self.setCentralWidget(wg)
        self.statusBar().showMessage('준비됨')

        # items #
        """
        0   <PyQt5.QtWidgets.QVBoxLayout object
        1   <PyQt5.QtWidgets.QLabel object
        2   <PyQt5.QtWidgets.QLineEdit object
        3   <PyQt5.QtWidgets.QPushButton object
        4   <PyQt5.QtWidgets.QLabel object
        5   <PyQt5.QtWidgets.QLineEdit object
        6   <PyQt5.QtWidgets.QPushButton object
        7   <PyQt5.QtWidgets.QLabel object
        8   <PyQt5.QtWidgets.QLineEdit object
        9   <PyQt5.QtWidgets.QPushButton object
        10  <PyQt5.QtWidgets.QTextEdit object
        """

        self.direcLine = self.centralWidget().children()[2]
        self.findBtn = self.centralWidget().children()[3]
        self.saveLine = self.centralWidget().children()[5]
        self.saveBtn = self.centralWidget().children()[6]
        self.targetWord = self.centralWidget().children()[8]
        self.searchBtn = self.centralWidget().children()[9]
        self.findRes = self.centralWidget().children()[10]

        # Actions #
        self.findBtn.clicked.connect(self.dataFolderOpen)
        self.searchBtn.clicked.connect(self.searchWord)
        self.saveBtn.clicked.connect(self.saveFolderOpen)

        # Window #
        self.setWindowTitle("Historical Linguistics for Middle Korean (ver. 2.0.1)")
        self.resize(800, 800)
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def dataFolderOpen(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Data Directory")
        self.direcLine.setText(folder)

    def saveFolderOpen(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Save Directory")
        self.saveLine.setText(folder)

    def searchWord(self):
        self.findRes.clear()
        dir = self.direcLine.text()
        save_dir = self.saveLine.text()

        ## 디렉토리 확인 ##
        if dir == '' or save_dir == '':
            self.statusBar().showMessage('오류: 빈 디렉토리')
            msgBox = QMessageBox.critical(self, 'Warning', '디렉토리를 설정해야 합니다!')
            return
        else:
            dir += "/"
            save_dir += "/"
        
        target = self.targetWord.text()

        if target == '':
            self.statusBar().showMessage('오류: 빈 검색 문자열')
            msgBox = QMessageBox.critical(self, 'Warning', '빈 문자열은 검색할 수 없습니다!')
        else:
            target = PUAtoUni(target, dict_0_TOTAL)
            target = seperation(target, dict_0_ONSET, dict_0_PEAK, dict_0_CODA)

            if target == '!!error!!':
                self.statusBar().showMessage('오류: 잘못된 검색 문자열')
                msgBox = QMessageBox.critical(self, 'Warning', '잘못된 입력입니다!')
                return

            result_line, iter = searchForWord(dir, save_dir, target, dict_0_TOTAL)

            if result_line == '':
                msgBox = QMessageBox.critical(self, 'Warning', '검색 결과가 없습니다 ㅜㅡㅜ')
            else:
                msgBox = QMessageBox.critical(self, 'Completed', '총 ' + str(iter) + '개가 검색되었습니다.')
            
            self.findRes.append(result_line)
            self.statusBar().showMessage('열심히 검색 완료: 총 {0}개의 검색 결과'.format(str(iter)))

## 메인 ##
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainApp()
    sys.exit(app.exec_())