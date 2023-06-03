from PyQt5.QtWidgets import QLineEdit, QCheckBox, QComboBox, QPushButton, QFileDialog
from PyQt5.QtGui import QIntValidator


class FieldError(Exception):
    pass


class Field:
    def __init__(self, name, label, required=True, default=None, choices=None):
        self._name = name
        self._label = label
        self._required = required
        self._default = default
        self._choices = choices
        self._widget = None

    @classmethod
    def getType(cls):
        return cls.__name__[:-5].lower()

    @property
    def name(self):
        return self._name

    @property
    def label(self):
        return self._label

    @property
    def widget(self):
        return self._widget

    def createWidget(self):
        self._widget = QLineEdit()
        if self._default is not None:
            self._widget.setText(str(self._default))

    def getRawValue(self):
        return self._widget.text()

    def getValue(self):
        rawValue = self.getRawValue()
        if rawValue == '':
            if self._required:
                raise FieldError("value '{}' required".format(self._label))
            else:
                return None
        else:
            try:
                return self.convert(rawValue)
            except Exception:
                raise FieldError("invalid value: '{}'".format(self._label))

    def convert(self, value):
        return value


class StringField(Field):
    pass


class IntegerField(Field):
    def createWidget(self):
        super().createWidget()
        self._widget.setValidator(QIntValidator())

    def convert(self, value):
        return int(value)


class FloatField(Field):
    def convert(self, value):
        return float(value)


class BooleanField(Field):
    def createWidget(self):
        self._widget = QCheckBox()
        if self._default is not None:
            self._widget.setChecked(self._default)

    def getRawValue(self):
        return self._widget.isChecked()


class EnumField(Field):
    def createWidget(self):
        assert self._choices is not None, "no choices"

        self._widget = QComboBox()

        if self._default is None:
            self._widget.addItem("")

        self._widget.addItems(self._choices)

        if self._default is not None:
            self._widget.setCurrentText(self._default)

    def getRawValue(self):
        return self._widget.currentText()


class FileOpenField(Field):
    INIT_TEXT = "choose..."

    def createWidget(self):
        self._widget = QPushButton(text=self.INIT_TEXT)
        self._widget.clicked.connect(self._click)
        if self._default is not None:
            self._widget.setText(str(self._default))

    def getRawValue(self):
        text = self._widget.text()
        if text == self.INIT_TEXT:
            text = ""
        return text

    def _click(self):
        path = self._performDialog()
        self._widget.setText(path)

    def _performDialog(self):
        return QFileDialog.getOpenFileName(self._widget, 'File')[0]


class DirectoryField(FileOpenField):
    def _performDialog(self):
        return QFileDialog.getExistingDirectory(self._widget, 'Directory')


class FileSaveField(FileOpenField):
    def _performDialog(self):
        return QFileDialog.getSaveFileName(self._widget, 'Save')[0]
