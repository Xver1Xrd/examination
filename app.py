# -*- coding: utf-8 -*-

import sys


from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QAction, QIcon, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QLabel,
    QInputDialog,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QGridLayout,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QStatusBar,
    QHBoxLayout

)
import tools as t
from pathlib import Path
import os
import sys
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtCore import QUrl, Qt, QTime
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtWidgets import (
    QApplication,
    QLineEdit,
    QSlider,
    QMessageBox,
    QDial,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QHBoxLayout

)


class CustomDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("HELLO!")

        QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel("Завершить тестирование?")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class Player(QWidget):
    def __init__(self, contentType, stageType, filePath):
        super().__init__()
        self.filePath = filePath
        self.mediaPlayer = QMediaPlayer()
        self.audioOutput = QAudioOutput()
        # self.audioOutput.setVolume(50)
        self.mediaPlayer.setAudioOutput(self.audioOutput)

        if contentType == "video":
            self.contentType = "video"
            self.videoWidget = QVideoWidget(self)
            self.mediaPlayer.setVideoOutput(self.videoWidget)

        self.mediaPlayer.playbackStateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.errorChanged.connect(self.handleError)
        self.mediaPlayer.setSource(QUrl.fromLocalFile(self.filePath))
        self.playButton = QPushButton("▶️", self)
        self.playButton.setEnabled(True)
        self.playButton.resize(self.playButton.sizeHint())
        self.playButton.clicked.connect(self.play)
        self.pauseButton = QPushButton("⏸️", self)
        self.pauseButton.setEnabled(True)
        self.pauseButton.resize(self.pauseButton.sizeHint())
        self.pauseButton.clicked.connect(self.mediaPlayer.pause)
        self.volumeSlider = QDial(self)
        self.volumeSlider.valueChanged.connect(
            self.setVolume)
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.setSingleStep(1)
        self.volumeSlider.setPageStep(20)
        self.volumeSlider.setValue(20)
        self.controlLayout = QHBoxLayout()
        self.controlLayout.setContentsMargins(5, 0, 5, 0)
        self.controlLayout.addWidget(self.playButton)

        self.stopButton = QPushButton("⏹️", self)
        self.stopButton.setEnabled(True)
        self.stopButton.resize(self.stopButton.sizeHint())
        self.stopButton.clicked.connect(self.stop)
        self.lbl = QLineEdit('00:00:00')
        self.lbl.setReadOnly(True)
        self.lbl.setFixedWidth(70)
        self.lbl.setUpdatesEnabled(True)
        self.lbl.selectionChanged.connect(
            lambda: self.lbl.setSelection(0, 0))
        self.elbl = QLineEdit('00:00:00')
        self.elbl.setReadOnly(True)
        self.elbl.setFixedWidth(70)
        self.elbl.setUpdatesEnabled(True)
        self.elbl.selectionChanged.connect(
            lambda: self.elbl.setSelection(0, 0))
        self.positionSlider = QSlider(Qt.Orientation.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)
        self.positionSlider.setSingleStep(10)
        self.positionSlider.setPageStep(20)
        self.positionSlider.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.positionSlider.resize(self.positionSlider.sizeHint())
        self.controlLayout.addWidget(self.pauseButton)
        self.controlLayout.addWidget(self.stopButton)
        self.controlLayout.addWidget(self.volumeSlider)
        self.controlLayout.addWidget(self.positionSlider)
        self.controlLayout.addWidget(self.lbl)
        self.controlLayout.addWidget(self.elbl)

    def stop(self):
        self.mediaPlayer.stop()
        self.mediaPlayer.setSource(QUrl.fromLocalFile(self.filePath))
        self.audioOutput = QAudioOutput()
        self.audioOutput.setVolume(self.volumeSlider.value() / 100)
        self.mediaPlayer.setAudioOutput(self.audioOutput)

    def play(self):
        self.audioOutput = QAudioOutput()
        self.audioOutput.setVolume(self.volumeSlider.value() / 100)
        self.mediaPlayer.setAudioOutput(self.audioOutput)
        self.mediaPlayer.play()

    def pause(self):
        self.mediaPlayer.pause()

    def setVolume(self, position):
        self.audioOutput.setVolume(position / 100)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def mediaStateChanged(self, state):
        if self.mediaPlayer.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.playButton.setEnabled(False)
            self.pauseButton.setEnabled(True)
            self.stopButton.setEnabled(True)
        else:
            self.playButton.setEnabled(True)
            self.pauseButton.setEnabled(False)
        if self.mediaPlayer.playbackState() == QMediaPlayer.PlaybackState.StoppedState:
            self.stopButton.setEnabled(False)
            self.mediaPlayer.setSource(
                QUrl.fromLocalFile(self.filePath))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)
        mtime = QTime(0, 0, 0, 0)
        mtime = mtime.addMSecs(self.mediaPlayer.position())
        self.lbl.setText(mtime.toString())

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)
        mtime = QTime(0, 0, 0, 0)
        mtime = mtime.addMSecs(self.mediaPlayer.duration())
        self.elbl.setText(mtime.toString())

    def handleError(self):
        self.playButton.setEnabled(False)
        print("Error: ", self.mediaPlayer.errorString())


class Testing(QMainWindow):

    questionID = 0

    def __init__(self):
        super().__init__()

        self.setGeometry(0, 0, 1024, 720)
        self.setWindowTitle('Сиситема тестирования: "Проверяйка"')

        exitAct = QAction(QIcon('exit.png'), '&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(QApplication.instance().quit)

        openFile = QAction(QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open exam File')
        openFile.triggered.connect(self.showDialog)
        self.timer = QTimer()
        self.layoutMain = QVBoxLayout()
        self.layoutQuestion = QVBoxLayout()
        self.layoutAnswers = QVBoxLayout()
        self.layoutControl = QHBoxLayout()
        self.layoutProgress = QGridLayout()
        self.menu = self.menuBar()

        file_menu = self.menu.addMenu("&File")
        file_menu.addAction(openFile)
        file_menu.addSeparator()
        file_menu.addAction(exitAct)

        self.progressBar = QProgressBar()
        self.progressBar.hide()
        self.layoutProgress.addWidget(self.progressBar, 0, 0, 0, 3)

        self.layoutMain.addLayout(self.layoutQuestion)
        self.layoutMain.addLayout(self.layoutAnswers)
        self.layoutMain.addLayout(self.layoutControl)
        self.layoutMain.addLayout(self.layoutProgress)

        self.setStatusBar(QStatusBar(self))
        widget = QWidget()
        widget.setLayout(self.layoutMain)
        self.setCentralWidget(widget)

    def showDialog(self):

        home_dir = str(Path.home())
        fname = QFileDialog.getOpenFileName(
            self, 'Open file', home_dir)

        if fname[0]:
            self.EX = t.load_data(fname[0])
            self.Result = {}
            self.Score = {}
            for q in range(0, len(self.EX.questions)):
                self.Result[q] = []
                self.Score[q] = 0
            print(self.Result)
        self.askName()
        self.setControl()
        self.testing()

    def setControl(self):
        self.endTimer()
        self.clear_item(self.layoutControl)
        self.next = QPushButton('Следующий вопрос >>', self)
        self.next.clicked.connect(self.nextQuestion)
        self.next.resize(self.next.sizeHint())
        self.preview = QPushButton('<< Предыдущий вопрос', self)
        self.preview.clicked.connect(self.previewQuestion)
        self.preview.resize(self.preview.sizeHint())
        self.layoutControl.addWidget(self.preview)
        self.layoutControl.addWidget(self.next)
        self.progressBar.show()
        self.progressBar.setRange(0, self.EX.count_questions())
        self.labelTimer = QLabel(self)
        self.labelTimerDesc = QLabel("Прошло времени: ")
        self.timer = QTimer()
        self.timer.timeout.connect(self.showTime)
        self.layoutProgress.addWidget(self.labelTimerDesc, 0, 4)
        self.layoutProgress.addWidget(self.labelTimer, 0, 5, 0, 2)
        self.startTimer()

    def askName(self):
        text, ok = QInputDialog.getText(self, 'Ввод имени', 'Как тебя зовут?')
        if ok:
            self.UserName = str(text)
        else:
            self.askName()

    def testing(self):
        self.Path = os.path.dirname(os.path.abspath(__file__))
        self.questionsFilePath = ""

        if self.questionID <= len(self.EX.questions)-1:
            if self.EX.questions[self.questionID].path != "":
                self.questionsFilePath = os.path.join(
                    self.Path, self.EX.questions[self.questionID].path)
            self.clear_item(self.layoutQuestion)
            if self.EX.questions[self.questionID].question != "":
                self.questionText = QLabel(self)
                self.layoutQuestion.addWidget(self.questionText)
                self.questionText.setText(
                    self.EX.questions[self.questionID].question)

            if self.EX.questions[self.questionID].question_type == "image":
                self.questionImage = QPixmap(
                    self.questionsFilePath).scaled(400, 400)
                self.questionImageLabel = QLabel()
                self.questionImageLabel.setPixmap(self.questionImage)
                self.layoutQuestion.addWidget(self.questionImageLabel)
            elif self.EX.questions[self.questionID].question_type == "video":
                player = Player(
                    self.EX.questions[self.questionID].question_type, "question", self.questionsFilePath)

                self.layoutQuestion.addWidget(player.videoWidget)
                self.layoutQuestion.addLayout(player.controlLayout)
            elif self.EX.questions[self.questionID].question_type == "audio":
                player = Player(
                    self.EX.questions[self.questionID].question_type, "question", self.questionsFilePath)
                self.layoutQuestion.addLayout(player.controlLayout)

            if self.questionID > 0:
                self.preview.setEnabled(True)
            if self.questionID == 0:
                self.preview.setEnabled(False)

            self.clear_item(self.layoutAnswers)
            for answersID in range(0, len(self.EX.questions[self.questionID].answers)):
                if self.EX.questions[self.questionID].answers[answersID].answer_type != "input":
                    сheckBox = QCheckBox()
                    сheckBox.answer = self.EX.questions[self.questionID].answers[answersID].is_true
                    сheckBox.id = answersID
                    сheckBox.toggled.connect(self.onClicked)

                    if self.EX.questions[self.questionID].answers[answersID].answer_type == "text":
                        сheckBox.setText(
                            self.EX.questions[self.questionID].answers[answersID].answer)
                        self.layoutAnswers.addWidget(
                            сheckBox, alignment=Qt.AlignmentFlag.AlignLeft)
                    elif self.EX.questions[self.questionID].answers[answersID].answer_type == "image":
                        layoutAnswer = QHBoxLayout()
                        layoutAnswer.setContentsMargins(0, 0, 0, 0)
                        layoutAnswer.setSpacing(0)
                        layoutAnswer.addWidget(
                            сheckBox)
                        answerFilePath = os.path.join(
                            self.Path, self.EX.questions[self.questionID].answers[answersID].path)
                        answerImage = QPixmap(answerFilePath).scaled(80, 80)
                        answerImageLabel = QLabel()
                        answerImageLabel.setPixmap(answerImage)
                        layoutAnswer.addWidget(
                            answerImageLabel)
                        self.layoutAnswers.addLayout(layoutAnswer)
                    elif self.EX.questions[self.questionID].answers[answersID].answer_type == "audio":
                        layoutAnswer = QHBoxLayout()
                        layoutAnswer.addWidget(
                            сheckBox, alignment=Qt.AlignmentFlag.AlignLeft)
                        answerFilePath = os.path.join(
                            self.Path, self.EX.questions[self.questionID].answers[answersID].path)
                        player = Player("audio", "answer", answerFilePath)
                        layoutAnswer.addLayout(player.controlLayout)
                        self.layoutAnswers.addLayout(layoutAnswer)
                    if answersID in self.Result[self.questionID]:
                        сheckBox.setChecked(True)
                    else:
                        сheckBox.setChecked(False)
                else:
                    self.input = QLineEdit()
                    self.input.editingFinished.connect(self.updateInput)
                    try:
                        self.input.setText(
                            self.Result[self.questionID][answersID])
                    except IndexError:
                        self.input.setText("")
                    self.layoutAnswers.addWidget(self.input)

    def askEndTest(self):
        dlg = CustomDialog()
        if dlg.exec():
            self.clear_item(self.layoutAnswers)
            self.clear_item(self.layoutQuestion)
            self.clear_item(self.layoutControl)
            self.endTest()
        else:
            print("Cancel!")
            self.testing()

    def endTest(self):
        self.UserScore = self.checkResult()
        res = ""
        time = self.countTimer
        if self.UserScore >= self.EX.passingScore:
            res = "Тест пройден!"
        else:
            res = "Тест не пройден!"

        msg = "Участник: {0}\nЗакончил тестирование  по тесту: {1}\nЗа время: {2}\nНабрал балов: {3}\nРезультат: {4}".format(
            self.UserName, self.EX.name, str(time), str(self.UserScore), res)

        self.questionText = QLabel(self)
        self.layoutQuestion.addWidget(self.questionText)
        self.questionText.setText(msg)

        self.replayButton = QPushButton('Повторить', self)
        self.replayButton.clicked.connect(self.replay)
        self.replayButton.resize(self.replayButton.sizeHint())
        self.layoutControl.addWidget(self.replayButton)

    def replay(self):
        self.setControl()
        self.testing()

    def checkResult(self):
        score = 0
        for question in self.Score:
            score += self.Score[question]
        return score

    def checkAnswer(self):
        countCorrectAnswer = 0
        countCorrectUserAnswer = 0
        countIncorrectUserAnswer = 0
        print(self.questionID)
        for answers in self.EX.questions[self.questionID].answers:
            if answers.is_true:
                countCorrectAnswer += 1
        for answersID in self.Result[self.questionID]:
            if isinstance(answersID, str):
                answersID = 0
            if self.EX.questions[self.questionID].answers[answersID].is_true and self.EX.questions[self.questionID].answers[answersID].answer_type != "input":
                countCorrectUserAnswer += 1
            elif self.EX.questions[self.questionID].answers[answersID].answer_type == "input":
                if self.EX.questions[self.questionID].answers[answersID].answer == self.Result[self.questionID][answersID]:
                    print("Tr")
                    countCorrectUserAnswer += 1
            else:
                countIncorrectUserAnswer += 1
        if countCorrectUserAnswer == countCorrectAnswer and countIncorrectUserAnswer == 0:
            print(True)
            self.Score[self.questionID] = self.EX.questions[self.questionID].weight
        else:
            print(False)
            self.Score[self.questionID] = 0

    def updateInput(self):
        if self.EX.questions[self.questionID].answers[0].answer_type == "input":
            print("-----------------------------")
            try:
                self.Result[self.questionID][0] = self.input.text()

            except IndexError:
                self.Result[self.questionID].append(self.input.text())

            # if self.Result[self.questionID][0]:
            #     self.Result[self.questionID][0] = self.input.text()
            # else:
            #     self.Result[self.questionID].append(self.input.text())
            print(self.Result[self.questionID])

    def nextQuestion(self):
        self.checkAnswer()
        if len(self.EX.questions)-1 <= self.questionID:
            print("last")
            self.testing()
            self.askEndTest()
        else:
            self.questionID += 1
            self.progressBar.setValue(self.questionID)
            self.testing()

    def previewQuestion(self):
        self.checkAnswer()
        if self.questionID < 0:
            self.questionID = 0
        else:
            self.questionID -= 1
            self.progressBar.setValue(self.questionID)

        self.testing()

    def onMyToolBarButtonClick(self, s):
        print("click", s)

    def onClicked(self):
        сheckBox = self.sender()
        # print("Animal " + str(сheckBox.answer) + " is " + str(сheckBox.isChecked())+ " is " + str(сheckBox.id))
        if сheckBox.isChecked():
            self.Result[self.questionID].append(сheckBox.id)
        else:
            self.Result[self.questionID].remove(сheckBox.id)

    def clear_item(self, item):
        if hasattr(item, "layout"):
            if callable(item.layout):
                layout = item.layout()
        else:
            layout = None

        if hasattr(item, "widget"):
            if callable(item.widget):
                widget = item.widget()
        else:
            widget = None

        if widget:
            widget.setParent(None)
        elif layout:
            for i in reversed(range(layout.count())):
                self.clear_item(layout.itemAt(i))

    def showTime(self):
        # time=QDateTime.currentDateTime()
        self.countTimer += 1
        timeDisplay = str(self.countTimer)
        self.labelTimer.setText(timeDisplay)
        if self.EX.timeLimit != 0 and self.EX.timeLimit == self.countTimer:
            print("Timeout")

    def startTimer(self):
        self.countTimer = 0
        self.timer.start(1000)

    def endTimer(self):
        self.timer.stop()


def main():

    app = QApplication(sys.argv)
    ex = Testing()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
