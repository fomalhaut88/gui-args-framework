from time import sleep

from gui_args_framework import ArgsWindow, fields


class TestWindow(ArgsWindow):
    title = "Test"
    args = [
        fields.IntegerField(name='x', label='First'),
        fields.IntegerField(name='y', label='Second'),
    ]
    description = "This program calculates sum of two integer numbers."

    def main(self, values):
        raise KeyError("my error")
        z = values['x'] + values['y']
        print(z)


TestWindow.run()
