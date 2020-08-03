# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'viewer_window.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from TableView import TableView


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1056, 666)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(232, 236, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(232, 236, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(232, 236, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(232, 236, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        MainWindow.setPalette(palette)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.context_searchLine = QtWidgets.QLineEdit(self.centralwidget)
        self.context_searchLine.setGeometry(QtCore.QRect(10, 20, 171, 31))
        self.context_searchLine.setText("")
        self.context_searchLine.setObjectName("context_searchLine")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 0, 141, 20))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(370, 0, 161, 21))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.message_searchLine = QtWidgets.QLineEdit(self.centralwidget)
        self.message_searchLine.setGeometry(QtCore.QRect(360, 20, 171, 31))
        self.message_searchLine.setText("")
        self.message_searchLine.setObjectName("message_searchLine")
        # self.context_view = QtWidgets.QTableView(self.centralwidget)
        self.context_view = TableView(self.centralwidget)
        self.context_view.setGeometry(QtCore.QRect(0, 69, 300, 531))
        self.context_view.setMinimumSize(QtCore.QSize(300, 50))
        self.context_view.setBaseSize(QtCore.QSize(300, 500))
        self.context_view.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.context_view.setFrameShadow(QtWidgets.QFrame.Raised)
        self.context_view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.context_view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.context_view.setShowGrid(False)
        self.context_view.setObjectName("context_view")
        self.context_view.horizontalHeader().setCascadingSectionResizes(True)
        self.context_view.horizontalHeader().setDefaultSectionSize(220)
        self.context_view.horizontalHeader().setHighlightSections(False)
        self.context_view.horizontalHeader().setMinimumSectionSize(60)
        self.context_view.horizontalHeader().setStretchLastSection(True)
        self.context_view.verticalHeader().setVisible(False)
        # self.message_view = QtWidgets.QTableView(self.centralwidget)
        self.message_view = TableView(self.centralwidget)
        self.message_view.setGeometry(QtCore.QRect(350, 70, 300, 531))
        self.message_view.setMinimumSize(QtCore.QSize(250, 50))
        self.message_view.setBaseSize(QtCore.QSize(300, 500))
        self.message_view.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.message_view.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.message_view.setFrameShadow(QtWidgets.QFrame.Raised)
        self.message_view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.message_view.setObjectName("message_view")
        self.message_view.horizontalHeader().setDefaultSectionSize(301)
        self.message_view.horizontalHeader().setHighlightSections(False)
        self.message_view.horizontalHeader().setStretchLastSection(True)
        self.message_view.verticalHeader().setVisible(False)
        self.btSearchContext = QtWidgets.QPushButton(self.centralwidget)
        self.btSearchContext.setGeometry(QtCore.QRect(200, 20, 61, 31))
        self.btSearchContext.setObjectName("btSearchContext")
        self.btSearchMessage = QtWidgets.QPushButton(self.centralwidget)
        self.btSearchMessage.setGeometry(QtCore.QRect(550, 20, 61, 31))
        self.btSearchMessage.setObjectName("btSearchMessage")
        self.btLoad = QtWidgets.QPushButton(self.centralwidget)
        self.btLoad.setGeometry(QtCore.QRect(730, 10, 93, 28))
        self.btLoad.setObjectName("btLoad")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(700, 60, 351, 161))
        self.groupBox.setObjectName("groupBox")
        self.sourceText = QtWidgets.QTextEdit(self.groupBox)
        self.sourceText.setGeometry(QtCore.QRect(10, 20, 301, 87))
        self.sourceText.setObjectName("sourceText")
        self.btChange_source = QtWidgets.QPushButton(self.groupBox)
        self.btChange_source.setGeometry(QtCore.QRect(250, 120, 93, 28))
        self.btChange_source.setObjectName("btChange_source")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(680, 60, 21, 541))
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setObjectName("line")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(700, 250, 351, 161))
        self.groupBox_2.setFlat(False)
        self.groupBox_2.setObjectName("groupBox_2")
        self.ru_transText = QtWidgets.QTextEdit(self.groupBox_2)
        self.ru_transText.setGeometry(QtCore.QRect(10, 20, 301, 91))
        self.ru_transText.setObjectName("ru_transText")
        self.btChange_rus = QtWidgets.QPushButton(self.groupBox_2)
        self.btChange_rus.setGeometry(QtCore.QRect(250, 120, 93, 28))
        self.btChange_rus.setObjectName("btChange_rus")
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(699, 430, 351, 161))
        self.groupBox_3.setObjectName("groupBox_3")
        self.en_transText = QtWidgets.QTextEdit(self.groupBox_3)
        self.en_transText.setGeometry(QtCore.QRect(10, 20, 301, 91))
        self.en_transText.setObjectName("en_transText")
        self.btChange_eng = QtWidgets.QPushButton(self.groupBox_3)
        self.btChange_eng.setGeometry(QtCore.QRect(250, 120, 93, 28))
        self.btChange_eng.setObjectName("btChange_eng")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(-10, 50, 701, 20))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.btSave = QtWidgets.QPushButton(self.centralwidget)
        self.btSave.setGeometry(QtCore.QRect(840, 10, 93, 28))
        self.btSave.setObjectName("btSave")
        self.addMessage_bt = QtWidgets.QToolButton(self.centralwidget)
        self.addMessage_bt.setGeometry(QtCore.QRect(650, 80, 27, 22))
        self.addMessage_bt.setAutoFillBackground(False)
        self.addMessage_bt.setStyleSheet("background-color: #e8ecf0;")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("plus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addMessage_bt.setIcon(icon)
        self.addMessage_bt.setPopupMode(QtWidgets.QToolButton.DelayedPopup)
        self.addMessage_bt.setObjectName("addMessage_bt")
        self.addContext_bt = QtWidgets.QToolButton(self.centralwidget)
        self.addContext_bt.setGeometry(QtCore.QRect(300, 80, 27, 22))
        self.addContext_bt.setAutoFillBackground(False)
        self.addContext_bt.setStyleSheet("background-color: #e8ecf0;")
        self.addContext_bt.setIcon(icon)
        self.addContext_bt.setPopupMode(QtWidgets.QToolButton.DelayedPopup)
        self.addContext_bt.setObjectName("addContext_bt")
        self.delContext_bt = QtWidgets.QToolButton(self.centralwidget)
        self.delContext_bt.setGeometry(QtCore.QRect(300, 110, 27, 22))
        self.delContext_bt.setAutoFillBackground(False)
        self.delContext_bt.setStyleSheet("background-color: #e8ecf0;")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("minus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.delContext_bt.setIcon(icon1)
        self.delContext_bt.setPopupMode(QtWidgets.QToolButton.DelayedPopup)
        self.delContext_bt.setObjectName("delContext_bt")
        self.delMessage_bt = QtWidgets.QToolButton(self.centralwidget)
        self.delMessage_bt.setGeometry(QtCore.QRect(650, 110, 27, 22))
        self.delMessage_bt.setAutoFillBackground(False)
        self.delMessage_bt.setStyleSheet("background-color: #e8ecf0;")
        self.delMessage_bt.setIcon(icon1)
        self.delMessage_bt.setPopupMode(QtWidgets.QToolButton.DelayedPopup)
        self.delMessage_bt.setObjectName("deMessage_bt")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1056, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:9pt;\">Поиск в contexts</span></p></body></html>"))
        self.label_4.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:9pt;\">Поиск в messages</span></p></body></html>"))
        self.btSearchContext.setText(_translate("MainWindow", "Поиск"))
        self.btSearchMessage.setText(_translate("MainWindow", "Поиск"))
        self.btLoad.setText(_translate("MainWindow", "LOAD"))
        self.groupBox.setTitle(_translate("MainWindow", "Исходный текст"))
        self.btChange_source.setText(_translate("MainWindow", "Изменить"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Русский перевод"))
        self.btChange_rus.setText(_translate("MainWindow", "Изменить"))
        self.groupBox_3.setTitle(_translate("MainWindow", "English translation"))
        self.btChange_eng.setText(_translate("MainWindow", "Изменить"))
        self.btSave.setText(_translate("MainWindow", "SAVE"))
        self.addMessage_bt.setText(_translate("MainWindow", "..."))
        self.addContext_bt.setText(_translate("MainWindow", "..."))
        self.delContext_bt.setText(_translate("MainWindow", "..."))
        self.delMessage_bt.setText(_translate("MainWindow", "..."))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
