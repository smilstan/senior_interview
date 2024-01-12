import random

from PySide2.QtCore import QObject, Signal, Property, QAbstractListModel, Qt, QModelIndex, QTimer, Slot, \
    QStringListModel
from PySide2.QtWidgets import QListView

COLORS = "red", "yellow", "gold", "green", "blue", "white", "black"


class MyModel(QAbstractListModel):
    def __init__(self):
        super().__init__()
        self._items = QListView()



    def rowCount(self, parent=...):
        return len(self._items)

    def data(self, index, role=...):
        return self._items[index.row()]

    def append_data(self, item: str):
        self.beginInsertRows(QModelIndex(), len(self._items), len(self._items))
        self._items.append(item)
        self.endInsertRows()

    @Slot(int, int)
    def move(self, from_, to_):
        self.beginMoveRows(QModelIndex(), from_, from_, QModelIndex(), to_)
        t = self._items.pop(to_)
        f = self._items.pop(from_)
        self._items.insert(from_, t)
        self._items.insert(to_, f)
        self.endMoveRows()

    # def moveRows(self, sourceParent, sourceRow, count, destinationParent, destinationChild):


class Client(QObject):
    MAX_ITEMS_COUNT = 30

    def __init__(self):
        super().__init__()
        self._data = []
        # self._data = MyModel()
        self._timer = QTimer(self)
        self._timer.setInterval(200)
        self._timer.timeout.connect(self._append_value)
        self._timer.start()
        self._download_state = False

    modelChanged = Signal()
    model = Property('QVariant',
                     fget=lambda self: self._data,
                     notify=modelChanged)

    downloadStateChanged = Signal(bool)

    @Property(bool, notify=downloadStateChanged)
    def downloadState(self) -> bool:
        return self._download_state

    @downloadState.setter
    def downloadState(self, value: bool):
        self._download_state = value
        self.downloadStateChanged.emit(value)


    # downloadState = Property(bool,
    #                          fget=lambda self: self._download_state,
    #                          fset=lambda self, value: setattr(self, '_download_state', value),
    #                          notify=downloadStateChanged)

    # @downloadState.setter
    # def downloadState(self, value):
    #     self._download_state = value
    #     self.downloadStateChanged.emit(value)

    @Slot(result=int)
    def getMaxItemsCount(self) -> int:
        return self.MAX_ITEMS_COUNT

    @Slot()
    def terminateDownloadProcess(self):
        self._timer.stop()
        self.downloadState = False

    def _append_value(self):
        if not self._download_state:
            print(1)
            self.downloadState = True

        if len(self._data) >= self.MAX_ITEMS_COUNT:
            self._timer.stop()
            self.downloadState = False
            return

        color = random.choice(COLORS)
        self._data.append(color)
        self.modelChanged.emit()




