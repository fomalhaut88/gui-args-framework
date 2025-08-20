from typing import Callable, Any

from PyQt5.QtCore import pyqtSignal, QMutex, QWaitCondition, QObject


class RpcCallStr(QObject):
    """
    RPC communicator so a thread may emit data outside. If we connect the object
    to a callback, it will be called on signal come.
    """

    _signal = pyqtSignal(str)
    _mutex = QMutex()
    _waitCondition = QWaitCondition()

    def __init__(self):
        super().__init__()
        self._result = None

    def call(self, s: str) -> Any:
        """
        Call for the string `s` waiting for the result.
        """
        self._signal.emit(s)
        self._mutex.lock()
        self._waitCondition.wait(self._mutex)
        self._mutex.unlock()
        return self._result

    def connect(self, callback: Callable):
        """
        Connect to a callback.
        """
        def wrapped(s):
            self._result = callback(s)
            self._waitCondition.wakeAll()
        self._signal.connect(wrapped)
