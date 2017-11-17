from gui_args_framework import ArgsWindow, fields


class TestWindow(ArgsWindow):
    title = "Test"
    args = [
        fields.IntegerField(name='x', default=2),
        fields.IntegerField(name='y', default=3),
        fields.StringField(name='my_str', required=False),
        fields.BooleanField(name='b', default=True),
        fields.EnumField(name='c', choices=["Windows", "Linux"], default="Linux"),
        fields.FileSaveField(name='f'),
    ]

    def main(self):
        z = self.x + self.y
        self.out(z)
        self.out(self.my_str)
        self.out(self.c)


if __name__ == "__main__":
    TestWindow.run()
