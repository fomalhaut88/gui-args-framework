import sys
import os

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QMessageBox

from .fields import FieldError
from .main_thread import MainThread


BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
UI_PATH = os.path.join(BASE_DIR, 'ui/ArgsWindow.ui')


class ArgsWindow(QMainWindow):
    title = None
    args = []
    description = ""

    window_pos = (100, 100)
    geom = (400, 400)
    showTypes = False
    descriptionLimit = 50

    def __init__(self):
        super().__init__()
        self.ui = self.initUI()
        self.setWindowTitle(self.__class__.title)
        self.initGeom()
        self.initArgs()
        self.initDescription()

    def main(self):
        raise NotImplementedError()

    @classmethod
    def run(cls):
        assert cls.title, "no title"
        app = QApplication(sys.argv)
        app.setApplicationName(cls.title)
        window = cls()
        window.show()
        sys.exit(app.exec_())

    def initUI(self):
        ui = uic.loadUi(UI_PATH, self)
        ui.startButton.clicked.connect(self.startButtonClick)
        return ui

    def initGeom(self):
        geometry = self.geometry()
        geometry.setLeft(self.__class__.window_pos[0])
        geometry.setTop(self.__class__.window_pos[1])
        geometry.setWidth(self.__class__.geom[0])
        geometry.setHeight(self.__class__.geom[1])
        self.setGeometry(geometry)

    def initArgs(self):
        self.__class__.args = self.getArgs()

        for i, field in enumerate(self.__class__.args):
            labelText = self.getLabelText(field)
            label = QLabel(text=labelText)
            field.createWidget()
            self.ui.argsTab.layout().insertRow(i, label, field.widget)

    def extractVariables(self):
        try:
            values = {}
            for field in self.__class__.args:
                values[field.name] = field.getValue()
            return values

        except FieldError as err:
            self.showError(str(err))
            return None

    def startButtonClick(self):
        params = self.extractVariables()
        if params is not None:
            mainThread = MainThread(self.main, params)

            msgBox = QMessageBox(self)
            msgBox.setWindowTitle("Running...")
            msgBox.setText("Running.\nClick cancel to interrupt.")
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setStandardButtons(QMessageBox.Cancel)

            cancelButton = msgBox.button(QMessageBox.Cancel)

            mainThread.stopSignal.connect(msgBox.close)
            mainThread.errorSignal.connect(self.showError)
            mainThread.successSignal.connect(self.showSuccess)
            mainThread.rpcMessage.connect(self.showInfo)
            mainThread.rpcConfirm.connect(self.confirm)

            mainThread.start()
            msgBox.exec_()

            if msgBox.clickedButton() == cancelButton and mainThread.isRunning():
                mainThread.terminate()

    def getArgs(self):
        return self.__class__.args

    def initDescription(self):
        words = self.__class__.description.split(' ')
        lines = []
        i0 = 0
        for i in range(len(words)):
            line = ' '.join(words[i0:i])
            lineNext = ' '.join(words[i0:i + 1])
            if len(lineNext) > self.__class__.descriptionLimit:
                i0 = i
                lines.append(line)
                lineNext = words[i]
        lines.append(lineNext)
        self.ui.descriptionLabel.setText('\n'.join(lines))

    def getLabelText(self, field):
        if self.__class__.showTypes:
            return "{} [{}]".format(field.label, field.getType())
        else:
            return field.label

    def confirm(self, prompt):
        reply = QMessageBox.question(
            self, "Confirmation", prompt,
            QMessageBox.Yes, QMessageBox.No
        )
        return reply == QMessageBox.Yes

    def showError(self, text):
        msgBox = QMessageBox(self)
        msgBox.setWindowTitle("Error")
        msgBox.setText(text)
        msgBox.setIcon(QMessageBox.Critical)
        msgBox.exec_()

    def showSuccess(self, text):
        msgBox = QMessageBox(self)
        msgBox.setWindowTitle("Completed")
        msgBox.setText(text)
        msgBox.setIcon(QMessageBox.Information)
        msgBox.exec_()

    def showInfo(self, text):
        QMessageBox.question(
            self, "Message", text,
            QMessageBox.Ok
        )
