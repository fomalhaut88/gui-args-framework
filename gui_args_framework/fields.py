from typing import Any, List, Optional

from PyQt5.QtWidgets import (QWidget, QLineEdit, QCheckBox, QComboBox, 
                             QPushButton, QFileDialog)
from PyQt5.QtGui import QIntValidator


class FieldError(Exception):
    """
    Error class for field parsing.
    """
    pass


class Field:
    """
    Base field class.
    """

    def __init__(self, name: str, label: str, required: bool = True, 
                 default: Any = None, choices: Optional[List[Any]] = None):
        self._name = name
        self._label = label
        self._required = required
        self._default = default
        self._choices = choices
        self._widget = None

    @classmethod
    def getType(cls) -> str:
        """
        Get type name of the field.
        """
        return cls.__name__[:-5].lower()

    @property
    def name(self) -> str:
        """
        Get name of the field.
        """
        return self._name

    @property
    def label(self) -> str:
        """
        Get label text
        """
        return self._label

    @property
    def widget(self) -> QWidget:
        """
        Get QT widget.
        """
        return self._widget

    def createWidget(self):
        """
        Create QT widget.
        """
        self._widget = QLineEdit()
        if self._default is not None:
            self._widget.setText(str(self._default))

    def getRawValue(self) -> Any:
        """
        Get raw data in the widget.
        """
        return self._widget.text()

    def getValue(self) -> Any:
        """
        Get value parsing the raw data.
        """
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

    def convert(self, value: Any) -> Any:
        """
        Parse raw data according to the type.
        """
        return value


class StringField(Field):
    """
    Field for a string as text input.
    """
    pass


class IntegerField(Field):
    """
    Field for an integer value as text input.
    """
    def createWidget(self):
        super().createWidget()
        self._widget.setValidator(QIntValidator())

    def convert(self, value):
        return int(value)


class FloatField(Field):
    """
    Field for a float value as text input.
    """
    def convert(self, value):
        return float(value)


class BooleanField(Field):
    """
    Field for a boolean value as checkbox.
    """
    def createWidget(self):
        self._widget = QCheckBox()
        if self._default is not None:
            self._widget.setChecked(self._default)

    def getRawValue(self):
        return self._widget.isChecked()


class EnumField(Field):
    """
    Field for a enum value as dropdown.
    """
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
    """
    Field for file path to open.
    """
    _INIT_TEXT = "choose..."

    def createWidget(self):
        self._widget = QPushButton(text=self._INIT_TEXT)
        self._widget.clicked.connect(self._click)
        if self._default is not None:
            self._widget.setText(str(self._default))

    def getRawValue(self):
        text = self._widget.text()
        if text == self._INIT_TEXT:
            text = ""
        return text

    def _click(self):
        path = self._performDialog()
        self._widget.setText(path)

    def _performDialog(self):
        return QFileDialog.getOpenFileName(self._widget, 'File')[0]


class DirectoryField(FileOpenField):
    """
    Field for directory path.
    """
    def _performDialog(self):
        return QFileDialog.getExistingDirectory(self._widget, 'Directory')


class FileSaveField(FileOpenField):
    """
    Field for file path to save.
    """
    def _performDialog(self):
        return QFileDialog.getSaveFileName(self._widget, 'Save')[0]
