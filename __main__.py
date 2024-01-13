import asyncio
import sys

import qasync

from pathlib import Path
from PySide2 import QtWidgets, QtQml
from PySide2.QtCore import QUrl

from backend.model import Client


class App:
    def __init__(self):
        self.app = QtWidgets.QApplication([])
        self.qml_eng = QtQml.QQmlApplicationEngine()
        self.root_ctx = self.qml_eng.rootContext()
        self.client = Client()

    @staticmethod
    def get_app_qml_path() -> str:
        app_path = Path(__file__).parent.resolve()
        qml_path = app_path / 'ui' / 'App.qml'
        return qml_path.as_posix()

    def setup_app(self):
        self.qml_eng.quit.connect(self.app.quit)
        self.setup_ctx()

    def setup_ctx(self):
        self.root_ctx.setContextProperty('client', self.client)

    def run_app(self):
        self.qml_eng.load(QUrl.fromLocalFile(self.get_app_qml_path()))
        self.app.exec_()
        self.client.cclose()


if __name__ == '__main__':
    app = App()
    app.setup_app()
    app.run_app()
