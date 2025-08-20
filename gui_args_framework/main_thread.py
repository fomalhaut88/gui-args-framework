import traceback
from typing import Callable, List, Any

from PyQt5.QtCore import QThread, pyqtSignal

from .rpc_call import RpcCallStr


class MainThread(QThread):
    """
    Thread class that implements the communication between the main function
    and dialogues.
    """

    stopSignal = pyqtSignal()
    """
    Stop signal is emited after the execution.
    """

    errorSignal = pyqtSignal(str)
    """
    Error signal is emited on error.
    """

    successSignal = pyqtSignal(str)
    """
    Success signal is emited if everything finished without errors.
    """

    # infoSignal = pyqtSignal(str)

    def __init__(self, main: Callable, params: List[Any]):
        """
        Create an instance having the callable `main` function to execute and
        the parameters `params`.
        """
        super().__init__()
        self._main = main
        self._params = params

        self.rpcMessage = RpcCallStr()
        """
        RPC message to communicate.
        """

        self.rpcConfirm = RpcCallStr()
        """
        RPC confirm to communicate.
        """

    def __getitem__(self, key: str) -> Any:
        return self._params[key]

    def run(self):
        """
        Run the thread.
        """
        try:
            self._main(self)
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

    def confirm(self, prompt: str) -> bool:
        """
        Emit `prompt` to confirm.
        """
        return self.rpcConfirm.call(prompt)

    def message(self, text: str):
        """
        Emit `text` to message.
        """
        self.rpcMessage.call(text)
