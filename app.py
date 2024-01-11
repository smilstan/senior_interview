from pathlib import Path

from PySide2 import QtWidgets, QtQml
from PySide2.QtCore import QUrl

from pyside.qml_playground.dragndrop.backend.model import Client


class App:
    def __init__(self):
        app_path = Path(__file__).parent.resolve()
        qml_path = app_path / 'ui' / 'App.qml'
        self.app = QtWidgets.QApplication([])
        self.qml_eng = QtQml.QQmlApplicationEngine()
        self.qml_eng.quit.connect(self.app.quit)

        self.client = Client()
        self.root_ctx = self.qml_eng.rootContext()
        self.setup_ctx()

        self.qml_eng.load(QUrl.fromLocalFile(qml_path.as_posix()))
        self.app.exec_()

    def setup_ctx(self):
        self.root_ctx.setContextProperty('client', self.client)


if __name__ == '__main__':
    app = App()



