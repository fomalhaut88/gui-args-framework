# gui-args-framework

**gui-args-framework** provides a user-friendly way to implement your Python script with GUI easily and quickly, instead of dark ugly terminal window that scares people who are far from programming.

Supposing, you have developed a program that takes arguments, does something and provides a result as text lines. Usually you develop such things as console applications that can be not so convenient to users. With `gui-args-framework` it can be easily done through GUI.

The example below is to understand how it works. There is a program to calculate sum of two integers:

```python
from gui_args_framework.args_window import ArgsWindow
from gui_args_framework.fields import IntegerField


class TestWindow(ArgsWindow):
    title = "Test"
    args = [
        IntegerField(name='x', label='First'),
        IntegerField(name='y', label='Second'),
    ]
    description = "This program calculates sum of two integer numbers."

    def main(self, this):
        if this.confirm("Are you sure?"):
            z = this['x'] + this['y']
            this.message("The sum is {}".format(z))


TestWindow.run()
```

## Installation

    pip install gui-args-framework

## Window parameters

You can customize your windows with following parameters:

```
title = "Name of your program"  # This is required
args = []  # List of arguments (see the example adove)
description = "Some description of your program."  # Default is empty

window_pos = (100, 100)  # A 2D-tuple that defines (x, y) of the absolute position of the window, default is (100, 100)
geom = (400, 400)  # A 2D-tuple that defines width and height of the window, default is (400, 400)
showTypes = False  # Show types of the arguments near the names, default is False
descriptionLimit = 50  # Maximum length of the line in the description without breaking, default is 50
```

## This methods of **this**

In `main` function that must be overrriden there is an argument `this` that contains the values of GUI arguments (by their names) and it has two methods to interact with GUI.

*this[**name**]* - gets the value of the argument *name*.

*this.**message**(text)* - shows information dialog with text *text*.

*this.**confirm**(prompt)* - shows prompt dialog with text *prompt*, returns True or False depending on user's choice.

## Field arguments

**name** - name of the argument. Required.

**label** - description of the argument (shown in GUI). Required.

**required** - necessity of the argument. Default is `True`.

**default** - default value of the argument. Default is `None`.

**choices** - list allowed values of the argument (for *EnumField*). Default is `None`.

## Fields

**StringField** - string argument.

**IntegerField** - integer argument.

**FloatField** - float argument.

**BooleanField** - boolean argument, represented as a checkbox.

**EnumField** - enum argument, represented as a dropdown list (argument *choices* is required).

**FileOpenField** - argument to choose existing file.

**DirectoryField** - argument to choose existing directory.

**FileSaveField** - argument to choose a new file to save.
