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

    def __repr__(self):
        return f"<{self.__class__.__name__}>"

    def manage_signals(self):
        self.readyRead.connect(self.receive_data)
        self.stateChanged.connect(self.handle_state_changed)

    def send(self, data: str):
        bdata = (data + "\n").encode('utf-8')
        super().write(bdata)
        self.flush()
        logger.debug(f"Data sent: {data}")

    dataReceived = Signal(str)

    def receive_data(self):
        data = self.readLine().data()
        logger.debug(f"Data received: {data}")
        sdata = data.decode('utf-8').strip()
        self.dataReceived.emit(sdata)

    errorOccurred = Signal(str)

    def handle_state_changed(self, state: QTcpSocket.SocketState):
        logger.debug(f"{self} state changed on: {state}")
        # handle UnconnectedState only
        if state is not QTcpSocket.SocketState.UnconnectedState:
            return

        self.process_socket_error()

    def process_socket_error(self):
        # skip UnknownSocketError because it is a default return value of self.error()
        if self.error() is QTcpSocket.SocketError.UnknownSocketError:
            return

        logger.debug(f"{self} error: {self.errorString()}")
        error = "Unhandled socket error"
        # handle error related to connection state
        if self.error() in (QTcpSocket.SocketError.ConnectionRefusedError,
                            QTcpSocket.SocketError.RemoteHostClosedError):
            error = self.errorString()

        self.errorOccurred.emit(error)

    def close(self):
        if self.state() is self.SocketState.ConnectedState:
            self.send('stop')
        super().close()
        logger.info("Connection closed")
