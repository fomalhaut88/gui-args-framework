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
