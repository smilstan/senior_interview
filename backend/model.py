from PySide2.QtCore import QObject, Signal, Property, Slot, QTimer

from logger import app_logger as logger
from backend.connector import TcpSocket


class Client(QObject):
    MAX_ITEMS_COUNT = 35

    def __init__(self):
        super().__init__()
        self.data = []
        self.download_state = False
        self.model_setup_terminated = False
        self.socket = TcpSocket(parent=self)
        self.requestTimer = QTimer(parent=self)
        self.requestTimer.setInterval(200)
        self.requestTimer.timeout.connect(self.try_setup_model)

        self.manage_signals()

    modelChanged = Signal()
    model = Property('QVariant',
                     fget=lambda self: self.data,
                     notify=modelChanged)

    def update_model_with(self, value: str):
        logger.debug(f'Update model with value: {value}')
        self.data.append(value)
        self.modelChanged.emit()

    downloadStateChanged = Signal(bool)
    downloadState = Property(bool,
                             fget=lambda self: self.download_state,
                             fset=lambda self, value: self.update_download_state(value),
                             notify=downloadStateChanged)

    def update_download_state(self, value: bool):
        self.download_state = value
        self.downloadStateChanged.emit(value)

    @Slot(result=int)
    def getMaxItemsCount(self) -> int:
        return self.MAX_ITEMS_COUNT

    def cclose(self):
        print("cclose")
        self.socket.close()

    def setup_model(self):
        logger.info("Start setup model")
        self.requestTimer.start()
        self.downloadState = True

    def try_setup_model(self):
        if self.model_setup_terminated:
            logger.debug("Model setup finished: terminated")
            self.stop_model_setup()
        elif len(self.data) == self.MAX_ITEMS_COUNT:
            logger.debug("Model setup finished: max size reached")
            self.stop_model_setup()
        else:
            self.socket.send("next")

    def stop_model_setup(self):
        logger.info("Stop model setup")
        self.requestTimer.stop()
        self.downloadState = False
        self.socket.close()

    @Slot()
    def terminateModelSetup(self):
        self.model_setup_terminated = True

    def manage_signals(self):
        self.socket.connected.connect(self.setup_model)
        self.socket.dataReceived.connect(self.update_model_with)
