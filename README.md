# gui-args-framework

**gui-args-framework** provides a user-friendly way to implement your Python script with GUI easily and quickly, instead of dark ugly terminal window that scares people who are far from programming.

Supposing, you have developed a program that takes arguments, does something and provides a result as text lines. Usually you develop such things as console applications that can be not so convenient to users. With gui-args-framework it can be easily done through GUI.

The example below is simple to understand how it works. There is a program to calculate sum of two integers:

```python
from gui_args_framework import ArgsWindow, fields


class TestWindow(ArgsWindow):
    title = "Test"
    args = [
        fields.IntegerField(name='x', label='First'),
        fields.IntegerField(name='y', label='Second'),
    ]
    description = "This program calculates sum of two integer numbers."

    def main(self, this):
        if this.confirm("Are you sure?"):
            z = this['x'] + this['y']
            this.message("The sum is {}".format(z))


TestWindow.run()
```

## Installation

    pip install git+https://github.com/fomalhaut88/gui-args-framework.git
