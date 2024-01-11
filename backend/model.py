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

    def __init__(self):
        super().__init__()
        self._data = []
        # self._data = MyModel()
        self._timer = QTimer(self)
        self._timer.setInterval(200)
        self._timer.timeout.connect(self.append_value)
        self._timer.start()

    def _model(self):
        return self._data

    modelChanged = Signal()
    model = Property('QVariant', _model, notify=modelChanged)

    def append_value(self):
        if len(self._data) > 2:
            self._timer.stop()
            return

        color = random.choice(COLORS)
        self._data.append(color)
        self.modelChanged.emit()

    # def append_value(self):
    #     if self._data.rowCount() > 5:
    #         self._timer.stop()
    #         return
    #
    #     color = random.choice(COLORS)
    #     self._data.append_data(color)
