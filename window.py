from PyQt5 import QtWidgets, QtGui
from viewer_window_2 import Ui_MainWindow
import sys
from TableModels import ContextsTableModel, MessagesTableModel

file = 'D:/ucheba/python/grid/translate/en1.ts'

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # #настрока toolbar
        # load_rex_ru = QtWidgets.QAction(QtGui.QIcon('ru.jpg'), 'load_ru', self)
        # load_rex_ru.triggered.connect(self.load)
        # self.toolBar = self.addToolBar('Load_ru')
        # self.toolBar.addAction(load_rex_ru)

        # создаем и устанавливаем модель в представление контекстов
        self.contexts_model = ContextsTableModel(file)
        self.ui.context_view.setModel(self.contexts_model)
        self.ui.context_view.setColumnWidth(1, 80)

        # создаем и устанавливаем модель в представление сообщений
        self.messages_model = MessagesTableModel()
        self.ui.message_view.setModel(self.messages_model)

        # свзываем слоты и сигналы
        # двойное нажатие на имя контекста открывает список сообщений контекста
        self.ui.context_view.doubleClicked.connect(lambda x: self.show_context_messages(x))
        # двойное нажатие на сообщение открывает переводы
        self.ui.message_view.doubleClicked.connect(lambda x: self.show_message_translations(x))
        # поиск контекста по строке
        self.ui.btSearchContext.clicked.connect(self.search_context)
        # поиск сообщения по строке
        self.ui.btSearchMessage.clicked.connect(self.search_message)


    def show_context_messages(self, index):
        self.ui.message_view.model().setContext(self.contexts_model.get_context(index))
        # self.ui.message_view.data
        self.ui.message_view.resizeRowsToContents()

    def show_message_translations(self, index):
        ru, en = self.ui.message_view.model().get_message_translations(index)
        self.ui.ru_transText.setText(ru)
        self.ui.en_transText.setText(en)


    def load(self):
        return None

    def search_context(self):
        line = self.ui.context_searchLine.text()
        context_index = self.ui.context_view.model().search_context(line)
        if context_index is not None:
            self.ui.context_view.setCurrentIndex(context_index)
            self.ui.context_view.setFocus()
            self.ui.statusbar.showMessage('')
        else:
            self.ui.statusbar.showMessage('Ничего не найдено.')


    def search_message(self):
        line = self.ui.message_searchLine.text()
        message_index = self.ui.message_view.model().search_message(line)
        if message_index is not None:
            self.ui.message_view.setCurrentIndex(message_index)
            self.ui.message_view.setFocus()
            self.ui.statusbar.showMessage('')
        else:
            self.ui.statusbar.showMessage('Ничего не найдено.')




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = Window()
    main.show()
    sys.exit(app.exec_())