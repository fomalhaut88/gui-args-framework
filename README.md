**gui-args-framework** provides a user-friendly way to implement Python programs with GUI.

Supposing, you have developed a program that takes arguments, does something and provides a result as text lines.
Usually you develop such things as console applications that gives other people creeps if they are far from programming.
With gui-args-framework it can be easily done through GUI.

An example of a program that calculates sum of two integer numbers:

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
