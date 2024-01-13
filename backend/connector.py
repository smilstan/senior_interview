from PySide2.QtCore import Signal
from PySide2.QtNetwork import QTcpSocket

from logger import connector_logger as logger

server_socket = ('localhost', 8080)


class TcpSocket(QTcpSocket):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.manage_signals()

        logger.info(f"Trying to connect to {server_socket}")
        self.connectToHost(*server_socket)

    def send(self, data: str):
        bdata = (data + "\n").encode('utf-8')
        super().write(bdata)
        self.flush()
        logger.debug(f"Data sent: {data}")

    def close(self):
        print("Closing")
        if self.state() is self.SocketState.ConnectedState:
            self.send('stop')
        super().close()

    def manage_signals(self):
        self.readyRead.connect(self.receive_data)
        self.stateChanged.connect(lambda state: print(state))
        self.connected.connect(lambda: print("connected"))
        self.disconnected.connect(self.handle_disconnect)

    def handle_disconnect(self):
        logger.debug("Handle disconnect event")
        if self.error() is self.SocketError.RemoteHostClosedError:
            self.lostConnection.emit()
        logger.error(self.errorString())

    dataReceived = Signal(str)

    def receive_data(self):
        data = self.readLine().data()
        logger.debug(f"Data received: {data}")
        sdata = data.decode('utf-8').strip()
        self.dataReceived.emit(sdata)

