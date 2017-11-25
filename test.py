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
            z = this.params['x'] + this.params['y']
            this.message("The sum is {}".format(z))


TestWindow.run()
