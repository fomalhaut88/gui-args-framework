from PyQt5.QtCore import pyqtSignal, QMutex, QWaitCondition, QObject


class RpcCallStr(QObject):
    signal = pyqtSignal(str)
    mutex = QMutex()
    waitCondition = QWaitCondition()

    def __init__(self):
        super().__init__()
        self.result = None

    def call(self, s):
        self.signal.emit(s)
        self.mutex.lock()
        self.waitCondition.wait(self.mutex)
        self.mutex.unlock()
        return self.result

    def connect(self, callback):
        def wrapped(s):
            self.result = callback(s)
            self.waitCondition.wakeAll()
        self.signal.connect(wrapped)
