import sys
import os

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QMessageBox

from .fields import FieldError


BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
UI_PATH = os.path.join(BASE_DIR, 'ui/ArgsWindow.ui')


class ArgsWindow(QMainWindow):
    title = None
    args = []

    geom = (400, 400)
    showtypes = False

    def __init__(self):
        super().__init__()
        self.ui = self.initUI()
        self.setWindowTitle(self.__class__.title)
        self.initGeom()
        self.initArgs()

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
        geometry.setWidth(self.__class__.geom[0])
        geometry.setHeight(self.__class__.geom[1])
        self.setGeometry(geometry)

    def initArgs(self):
        for i, field in enumerate(self.getArgs()):
            labelText = self.getLabelText(field)
            label = QLabel(text=labelText)
            field.createWidget()
            self.ui.argsTab.layout().insertRow(i, label, field.widget)

    def extractVariables(self):
        try:
            for field in self.getArgs():
                self.__dict__[field.name] = field.getValue()
            return True
        except FieldError as err:
            self.showError(str(err))
            return False

    def startButtonClick(self):
        success = self.extractVariables()
        if success:
            self.ui.outputTextEdit.setPlainText('')
            try:
                self.main()
            except Exception as err:
                text = "{}: {}".format(
                    err.__class__.__name__,
                    str(err)
                )
                self.showError(text)
            else:
                self.showSuccess("Success")

    def getArgs(self):
        return self.__class__.args

    def getLabelText(self, field):
        if self.__class__.showtypes:
            return "{} [{}]".format(field.name, field.getType())
        else:
            return field.name

    def out(self, *args):
        output = self.ui.outputTextEdit.toPlainText()
        output += ' '.join(map(str, args)) + '\n'
        self.ui.outputTextEdit.setPlainText(output)

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
