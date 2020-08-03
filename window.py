from PyQt5 import QtWidgets, QtGui, QtCore
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
        self.contexts_model = ContextsTableModel()
        self.ui.context_view.setModel(self.contexts_model)
        self.ui.context_view.setColumnWidth(1, 80)
    #     self.ui.context_view.horizontalHeader().setStyleSheet('background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\
    #                             stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,\
    #                             stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);\
    # border: 2px solid #C4C4C3;\
    # border-bottom-color: #C2C7CB; /* same as the pane color */\
    # border-top-left-radius: 4px;\
    # border-top-right-radius: 4px;\
    # min-width: 8ex;\
    # padding: 2px;')

        # создаем и устанавливаем модель в представление сообщений
        self.messages_model = MessagesTableModel()
        self.ui.message_view.setModel(self.messages_model)
        self.ui.message_view.horizontalHeader().setStyleSheet('border: 2px solid white; border-top-left-radius: 8px;\
    border-top-right-radius: 8px;')# padding: 2px;')
    #     palette = self.ui.message_view.palette()
    #     palette.setColor(QtGui.QPalette.Normal, QtGui.QPalette.Background, QtGui.QColor('#42464d'))
    #     self.ui.message_view.setPalette(palette)

        # настройка контексного меню для таблицы контекстов
        insert_context = QtWidgets.QAction('Вставить контекст', self)
        insert_context.triggered.connect(self.insert_context)
        self.menu_for_context_view = QtWidgets.QMenu(self)
        self.menu_for_context_view.addAction(insert_context)

        # настройка контекстного меню для таблицы сообщений
        insert_message = QtWidgets.QAction('Вставить сообщение',  self)
        insert_message.triggered.connect(self.insert_message)
        self.menu_for_message_view = QtWidgets.QMenu(self)
        self.menu_for_message_view.addAction(insert_message)


        # связываем слоты и сигналы
        # двойное нажатие на имя контекста открывает список сообщений контекста
        self.ui.context_view.doubleClicked.connect(lambda x: self.show_context_messages(x))
        # двойное нажатие на сообщение открывает переводы
        self.ui.message_view.doubleClicked.connect(lambda x: self.show_message(x))
        # поиск контекста по строке
        self.ui.btSearchContext.clicked.connect(self.search_context)
        # поиск сообщения по строке
        self.ui.btSearchMessage.clicked.connect(self.search_message)
        # загрузка данных
        self.ui.btLoad.clicked.connect(self.load)
        # сохранение данных
        self.ui.btSave.clicked.connect(self.save)
        # сохранение значения русского перевода
        self.ui.btChange_rus.clicked.connect(self.save_translation)
        # сохранение значения английского перевода
        self.ui.btChange_eng.clicked.connect(self.save_translation)
        # сохранение значения исходного текста
        self.ui.btChange_source.clicked.connect(self.save_source)
        # добавление нового контекста
        self.ui.addContext_bt.clicked.connect(self.add_context)
        # добавление нового сообщения
        self.ui.addMessage_bt.clicked.connect(self.add_message)
        # при изменении текущего выбранного сообщения стираются поля, отображающие данные сообщения
        self.ui.message_view.selectionModel().selectionChanged.connect(self.clean_textEditors)
        # появление контексного меню при нажатии на правую кнопку мыши
        self.ui.context_view.mouse_pressed.connect(self.show_context_menu)
        self.ui.message_view.mouse_pressed.connect(self.show_context_menu)

    def insert_context(self):
        index = self.ui.context_view.currentIndex().row()
        name, _ = QtWidgets.QInputDialog.getText(self, 'Новый контекст', 'Введите название нового контекста')
        if _ == True:
            self.ui.context_view.model().insert_context(name, index + 1)
            self.ui.statusbar.showMessage('Контекст успешно добавлен.')

    def insert_message(self):
        index = self.ui.message_view.currentIndex().row()
        name, _ = QtWidgets.QInputDialog.getText(self, 'Новое сообщение', 'Введите исходный текст нового сообщения')
        if _ == True:
            if self.ui.message_view.model().isContextSetted() == True:
                self.ui.message_view.model().insert_message(name, index + 1)
                self.ui.statusbar.showMessage('Сообщение успешно добавлено.')
            else:
                self.ui.statusbar.showMessage('Контекст не выбран.')

    def show_context_menu(self):
        if self.sender() is self.ui.context_view:
            self.menu_for_context_view.exec(QtGui.QCursor.pos())
        else:
            self.menu_for_message_view.exec(QtGui.QCursor.pos())

    def clean_textEditors(self):
        self.ui.ru_transText.clear()
        self.ui.en_transText.clear()
        self.ui.sourceText.clear()

    def save_source(self):
        try:
            index = self.ui.message_view.currentIndex()
            text = self.ui.sourceText.toPlainText()
            self.ui.message_view.model().set_message_source(index, text)
        except Exception:
            self.ui.statusbar.showMessage('Ошибка изменения исходного текста сообщения.')

    def save_translation(self):
        try:
            index = self.ui.message_view.currentIndex()
            if self.sender() is self.ui.btChange_rus:
                text = self.ui.ru_transText.toPlainText()
                self.ui.message_view.model().set_message_translation('ru', index, text)
            else:
                text = self.ui.en_transText.toPlainText()
                self.ui.message_view.model().set_message_translation('en', index, text)
        except Exception:
            self.ui.statusbar.showMessage('Ошибка изменения перевода.')

    def show_context_messages(self, index):
        self.ui.message_view.model().setContext(self.contexts_model.get_context(index))
        # self.ui.message_view.data
        self.ui.message_view.resizeRowsToContents()

    def show_message(self, index):
        ru, en = self.ui.message_view.model().get_message_translations(index)
        self.ui.sourceText.setText(self.ui.message_view.model().data(index))
        self.ui.ru_transText.setText(ru)
        self.ui.en_transText.setText(en)

    def load(self):
        try:
            filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Открыть', '/rex.ts',
                                                                 'Файлы переводов (*.ts)')
            self.ui.context_view.model().load_data(filename)
            self.ui.statusbar.showMessage('Загружено из файла:' + filename)
        except Exception:
            self.ui.statusbar.showMessage('Ошибка заргузки.')

    def save(self):
        try:
            filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Сохранить', '/rex.ts',
                                                                'Файлы переводов (*.ts)')
            self.ui.context_view.model().save_data(filename, 'ru')
            self.ui.statusbar.showMessage('Сохранено в файл:' + filename)
        except Exception:
            self.ui.statusbar.showMessage('Ошибка сохранения.')

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
        print(line)
        message_index = self.ui.message_view.model().search_message(line)
        if message_index is not None:
            self.ui.message_view.setCurrentIndex(message_index)
            self.ui.message_view.setFocus()
            self.ui.statusbar.showMessage('')
        else:
            self.ui.statusbar.showMessage('Ничего не найдено.')

    def add_context(self):
        name, _ = QtWidgets.QInputDialog.getText(self, 'Новый контекст', 'Введите название нового контекста')
        if _ == True:
            self.ui.context_view.model().add_context(name)
            self.ui.statusbar.showMessage('Контекст успешно добавлен.')

    def add_message(self):
        name, _ = QtWidgets.QInputDialog.getText(self, 'Новое сообщение', 'Введите исходный текст нового сообщения')
        if _ == True:
            if self.ui.message_view.model().isContextSetted() == True:
                self.ui.message_view.model().add_message(name)
                self.ui.statusbar.showMessage('Сообщение успешно добавлено.')
            else:
                self.ui.statusbar.showMessage('Контекст не выбран.')

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = Window()
    main.show()
    sys.exit(app.exec_())