from pathlib import Path
from PySide2 import QtWidgets, QtQml
from PySide2.QtCore import QUrl

from backend.solution import Client


class App:
    qml_path = Path(__file__).parent.resolve() / 'ui' / 'App.qml'

    def __init__(self):
        self.app = QtWidgets.QApplication([])
        self.qml_eng = QtQml.QQmlApplicationEngine()
        self.root_ctx = self.qml_eng.rootContext()
        self.client = Client()

    def setup_app(self):
        self.qml_eng.quit.connect(self.app.quit)
        self.setup_ctx()

    def setup_ctx(self):
        self.root_ctx.setContextProperty('client', self.client)

    def run_app(self):
        self.qml_eng.load(QUrl.fromLocalFile(self.qml_path.as_posix()))
        self.app.exec_()
        self.client.release_resources()


if __name__ == '__main__':
    app = App()
    app.setup_app()
    app.run_app()
