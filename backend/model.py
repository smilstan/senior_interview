import random

from PySide2.QtCore import QObject, Signal, Property, QAbstractListModel, Qt, QModelIndex, QTimer, Slot, \
    QStringListModel
from PySide2.QtWidgets import QListView

COLORS = "red", "yellow", "gold", "green", "blue", "white", "black"


class Client(QObject):
    MAX_ITEMS_COUNT = 30

    def __init__(self):
        super().__init__()
        self._data = []
        self._download_state = False

        self._timer = QTimer(self)
        self._timer.setInterval(100)
        self._timer.timeout.connect(self._append_value)
        self._timer.start()


    modelChanged = Signal()
    model = Property('QVariant',
                     fget=lambda self: self._data,
                     notify=modelChanged)

    downloadStateChanged = Signal(bool)
    downloadState = Property(bool,
                             fget=lambda self: self._download_state,
                             fset=lambda self, value: self._update_download_state(value),
                             notify=downloadStateChanged)

    @Slot(result=int)
    def getMaxItemsCount(self) -> int:
        return self.MAX_ITEMS_COUNT

    @Slot()
    def terminateDownloadProcess(self):
        self._timer.stop()
        self.downloadState = False

    def _append_value(self):
        if not self._download_state:
            self.downloadState = True

        if len(self._data) >= self.MAX_ITEMS_COUNT:
            self._timer.stop()
            self.downloadState = False
            return

        color = random.choice(COLORS)
        self._data.append(color)
        self.modelChanged.emit()

    def _update_download_state(self, value: bool):
        self._download_state = value
        self.downloadStateChanged.emit(value)
