from PyQt5 import QtWidgets, QtGui, QtCore, Qt

class TableView(QtWidgets.QTableView):
    mouse_pressed = QtCore.pyqtSignal()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def mousePressEvent(self, e: QtGui.QMouseEvent):
        QtWidgets.QTableView.mousePressEvent(self, e)
        button = e.button()
        if button == Qt.Qt.RightButton:
            self.mouse_pressed.emit()
