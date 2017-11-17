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
    description = ""

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
