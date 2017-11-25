import traceback

from PyQt5.QtCore import QThread, pyqtSignal

from .rpc_call import RpcCallStr


class MainThread(QThread):
    stopSignal = pyqtSignal()
    errorSignal = pyqtSignal(str)
    successSignal = pyqtSignal(str)
    infoSignal = pyqtSignal(str)

    def __init__(self, main, params):
        super().__init__()
        self.main = main
        self.params = params

        self.rpcMessage = RpcCallStr()
        self.rpcConfirm = RpcCallStr()

    def __getitem__(self, key):
        return self.params[key]

    def run(self):
        try:
            self.main(self)
        except Exception as err:
            text = "{}: {}".format(
                err.__class__.__name__,
                str(err)
            )
            self.errorSignal.emit(text)
            print(traceback.format_exc())
        else:
            self.successSignal.emit("Success")
        finally:
            self.stopSignal.emit()

    def confirm(self, prompt):
        return self.rpcConfirm.call(prompt)

    def message(self, text):
        self.rpcMessage.call(text)
