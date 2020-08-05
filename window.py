from PyQt5 import QtWidgets, QtGui, QtCore
from viewer_window_1 import Ui_MainWindow
import sys
from ContextsTableModel import ContextsTableModel
from MessagesTableModel import MessagesTableModel
from ContextItem import ContextItem

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
        self.ui.context_view.setEditTriggers(QtWidgets.QTableView.NoEditTriggers)
        self.hidden_contexts = []
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
        self.ui.message_view.setEditTriggers(QtWidgets.QTableView.NoEditTriggers)
        self.hidden_messages = []
        self.ui.message_view.horizontalHeader().setStyleSheet('border: 2px solid white; border-top-left-radius: 8px;\
    border-top-right-radius: 8px;')# padding: 2px;')
    #     palette = self.ui.message_view.palette()
    #     palette.setColor(QtGui.QPalette.Normal, QtGui.QPalette.Background, QtGui.QColor('#42464d'))
    #     self.ui.message_view.setPalette(palette)

        # настройка контексного меню для таблицы контекстов
        # вставить контекст
        insert_context = QtWidgets.QAction('Вставить новый контекст', self)
        insert_context.triggered.connect(self.insert_context)
        # удалить контекст
        delete_context = QtWidgets.QAction('Удалить', self)
        delete_context.triggered.connect(self.delete_context)
        # переименовать контекст
        rename_context = QtWidgets.QAction('Переименовать', self)
        rename_context.triggered.connect(self.rename_context)
        self.menu_for_context_view = QtWidgets.QMenu(self)
        self.menu_for_context_view.addAction(insert_context)
        self.menu_for_context_view.addAction(delete_context)
        self.menu_for_context_view.addAction(rename_context)


        # настройка контексного меню для таблицы сообщений
        # вставить сообщение
        insert_message = QtWidgets.QAction('Вставить новое сообщение',  self)
        insert_message.triggered.connect(self.insert_message)
        # удалить сообщение
        delete_message = QtWidgets.QAction('Удалить', self)
        delete_message.triggered.connect(self.delete_message)
        # переименовать сообщение
        rename_message = QtWidgets.QAction('Изменить исходный текст', self)
        rename_message.triggered.connect(self.rename_message)
        self.menu_for_message_view = QtWidgets.QMenu(self)
        self.menu_for_message_view.addAction(insert_message)
        self.menu_for_message_view.addAction(delete_message)
        self.menu_for_message_view.addAction(rename_message)


        # связываем слоты и сигналы
        # двойное нажатие на имя контекста открывает список сообщений контекста
        self.ui.context_view.doubleClicked.connect(lambda x: self.show_context_messages(x))
        # двойное нажатие на сообщение открывает переводы
        self.ui.message_view.doubleClicked.connect(lambda x: self.show_message(x))
        # показ контекста соответсвующего выбранному сообщению
        self.ui.message_view.clicked.connect(lambda x: self.choose_context(x))
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
        # удаление контекста по имени
        self.ui.delContext_bt.clicked.connect(self.delete_context_by_name)
        # удаление сообщения по имени
        self.ui.delMessage_bt.clicked.connect(self.delete_message_by_name)
        # при изменении текущего выбранного сообщения стираются поля, отображающие данные сообщения
        self.ui.message_view.selectionModel().selectionChanged.connect(self.clean_textEditors)
        # появление контексного меню при нажатии на правую кнопку мыши
        self.ui.context_view.mouse_pressed.connect(self.show_context_menu)
        self.ui.message_view.mouse_pressed.connect(self.show_context_menu)
        # показать скрытые контексты
        self.ui.showAllContexts_bt.clicked.connect(self.showAllContexts)
        # показать скрытые сообщения
        self.ui.showAllMessages_bt.clicked.connect(self.showAllMessages)
        # очистить представление сообщений
        self.ui.cleanMessageView_bt.clicked.connect(self.cleanMessageView)
        # очистить представление контекстов
        self.ui.cleanContextView_bt.clicked.connect(self.cleanContextView)

    # очистить представление сообщение
    def cleanContextView(self):
        messageBox = QtWidgets.QMessageBox()
        messageBox.setText('Вы уверены, что хотите удалить все контексты?')
        messageBox.setWindowTitle('Удаление')
        messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        messageBox.setIcon(QtWidgets.QMessageBox.Warning)
        answer = messageBox.exec()
        if answer == QtWidgets.QMessageBox.Ok:
            self.ui.context_view.model().clean_model()

    # очистить представление сообщений
    def cleanMessageView(self):
        self.ui.message_view.model().setContext(None)

    # выбираем контекст соответсвующий выбранному контексту
    def choose_context(self, index):
        self.showAllContexts()
        name = self.ui.message_view.model().get_message(index).get_parent().get_name()
        for n in range(0, self.ui.context_view.model().rowCount()):
            if self.ui.context_view.model().get_context(n).get_name() != name:
                self.ui.context_view.hideRow(n)
                self.hidden_contexts.append(n)
        self.ui.statusbar.showMessage('Context: {0}'.format(name))

    # переименовывание контекста
    def rename_context(self):
        index = self.ui.context_view.currentIndex()
        self.ui.context_view.edit(index)

    # переименовывание контекста
    def rename_message(self):
        index = self.ui.message_view.currentIndex()
        self.ui.message_view.edit(index)

    # вставка нового элемента context в модель по индексу
    def insert_context(self):
        index = self.ui.context_view.currentIndex().row()
        name, _ = QtWidgets.QInputDialog.getText(self, 'Новый контекст', 'Введите название нового контекста')
        if _ == True and name != '':
            self.ui.context_view.model().insert_context(name, index + 1)
            self.ui.statusbar.showMessage('Контекст успешно добавлен.')

    # вставка нового элемента message в модель по индексу
    def insert_message(self):
        index = self.ui.message_view.currentIndex().row()
        name, _ = QtWidgets.QInputDialog.getText(self, 'Новое сообщение', 'Введите исходный текст нового сообщения')
        if _ == True and name != '':
            if self.ui.message_view.model().isContextSetted() == True:
                self.ui.message_view.model().insert_message(name, index + 1)
                self.ui.statusbar.showMessage('Сообщение успешно добавлено.')
            else:
                self.ui.statusbar.showMessage('Контекст не выбран.')

    # удаление элемента context по индексу
    def delete_context(self):
        row = self.ui.context_view.currentIndex().row()
        index = self.ui.context_view.model().index(row, 0)
        messageBox = QtWidgets.QMessageBox(self)
        messageBox.setWindowTitle('Удаление элемента context')
        messageBox.setText('Вы уверены, что хотите удалить контекст "{0}"?'.format(self.ui.context_view.model().data(index, QtCore.Qt.DisplayRole)))
        messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        messageBox.setIcon(QtWidgets.QMessageBox.Warning)
        answer = messageBox.exec()
        if answer == QtWidgets.QMessageBox.Ok:
            self.ui.context_view.model().delete_context(row)

    # удаление элемента message по индексу
    def delete_message(self):
        row = self.ui.message_view.currentIndex().row()
        index = self.ui.message_view.model().index(row, 0)
        messageBox = QtWidgets.QMessageBox(self)
        messageBox.setWindowTitle('Удаление элемента message')
        messageBox.setText('Вы уверены, что хотите удалить сообщение "{0}"?'.format(self.ui.message_view.model().data(index, QtCore.Qt.DisplayRole)))
        messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        messageBox.setIcon(QtWidgets.QMessageBox.Warning)
        answer = messageBox.exec()
        if answer == QtWidgets.QMessageBox.Ok:
            self.ui.message_view.model().delete_message(row)

    # удаление элемента context по имени
    def delete_context_by_name(self):
        name, _ = QtWidgets.QInputDialog.getText(self, 'Удаление элемента context', 'Введите название контекста')
        if _== True and name != '':
            index = self.ui.context_view.model().search_context(name)
            self.ui.context_view.setCurrentIndex(index)
            self.delete_context()

    # удаление элемента message по исходному тексту
    def delete_message_by_name(self):
        name, _ = QtWidgets.QInputDialog.getText(self, 'Удаление элемента message', 'Введите название сообщения')
        if _ == True and name != '':
            index = self.ui.message_view.model().search_message(name)
            self.ui.message_view.setCurrentIndex(index)
            self.delete_message()

    # появление контекстного меню в представлениях
    def show_context_menu(self):
        if self.sender() is self.ui.context_view:
            self.menu_for_context_view.exec(QtGui.QCursor.pos())
        else:
            self.menu_for_message_view.exec(QtGui.QCursor.pos())

    # очистка полей описания сообщения
    def clean_textEditors(self):
        self.ui.ru_transText.clear()
        self.ui.en_transText.clear()
        self.ui.sourceText.clear()

    # сохранение изменений исходного текста сообщения
    def save_source(self):
        try:
            index = self.ui.message_view.currentIndex()
            text = self.ui.sourceText.toPlainText()
            self.ui.message_view.model().set_message_source(index, text)
        except Exception:
            self.ui.statusbar.showMessage('Ошибка изменения исходного текста сообщения.')

    # сохранение изменений текста переводов сообщений
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

    # показ сообщений выбранного контекста
    def show_context_messages(self, index):
        context = self.ui.context_view.model().get_context(index.row())
        self.ui.message_view.model().setContext(context)
        self.ui.statusbar.showMessage('Выбран контекст "{0}"'.format(context.get_name()))
        self.showAllMessages()
        self.ui.message_view.resizeRowsToContents()

    # показ исходного текста и переводов выбранного сообщения
    def show_message(self, index):
        ru, en = self.ui.message_view.model().get_message(index).get_translations()
        self.ui.sourceText.setText(self.ui.message_view.model().data(index))
        self.ui.ru_transText.setText(ru)
        self.ui.en_transText.setText(en)

    # загрузка переводов из файла
    def load(self):
        try:
            filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Открыть', '/rex.ts',
                                                                 'Файлы переводов (*.ts)')
            self.ui.context_view.model().load_data(filename)
            self.ui.statusbar.showMessage('Загружено из файла:' + filename)
            self.showAllContexts()
        except Exception:
            self.ui.statusbar.showMessage('Ошибка заргузки.')

    # сохранение переводов в файл
    def save(self):
        try:
            # filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Сохранить', '/rex.ts',
            #                                                     'Файлы переводов (*.ts)')

            language, _ = QtWidgets.QInputDialog.getItem(self, 'Сохранение', 'Выберите сохраняемый язык:',
                                                  ['Русский', 'Английский', 'Оба языка'])
            if _ == True:
                if language == 'Оба языка':
                    filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Файл для сохранения английской версии', '/rex.ts',
                                                                     'Файл (*.ts)')
                    if _ == True:
                         self.ui.context_view.model().save_data(filename, 'en')
                    filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Файл для сохранения русской версии',
                                                                        '/rex.ts', 'Файл (*.ts)')
                    if _== True:
                        self.ui.context_view.model().save_data(filename, 'ru')
                elif language == 'Русский':
                    filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Файл для сохранения русской версии',
                                                                        '/rex.ts', 'Файл (*.ts)')
                    if _ == True:
                        self.ui.context_view.model().save_data(filename, 'ru')
                else:
                    filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Файл для сохранения английской версии',
                                                                        '/rex.ts',
                                                                        'Файл (*.ts)')
                    if _ == True:
                        self.ui.context_view.model().save_data(filename, 'en')
        except Exception:
            self.ui.statusbar.showMessage('Ошибка сохранения.')

    # поиск контекстов по названию
    def search_context(self, string=None):
        self.showAllContexts()
        if string is None:
            string = self.ui.context_searchLine.text()
        found_contexts = self.ui.context_view.model().contexts_to_hide(string)
        if found_contexts != []:
            self.found_contexts_model = ContextsTableModel()
            for n in found_contexts:
                self.ui.context_view.hideRow(n)
            self.hidden_contexts = found_contexts
            self.ui.statusbar.showMessage('Найдено {0} элементов.'.format(self.ui.context_view.model().rowCount() - len(found_contexts)))
        else:
            self.ui.statusbar.showMessage('Ничего не найдено.')

    # поиск контекстов по исходному тексту
    def search_message(self):
        line = self.ui.message_searchLine.text()
        if line == '':
            return False
        if self.ui.search_in_currContext_chB.isChecked() == True:
            if self.ui.message_view.model().isContextSetted() == True:
                found_messages = self.ui.message_view.model().messages_to_hide(line)
                for n in found_messages:
                    self.ui.message_view.hideRow(n)
                self.hidden_messages = found_messages
                self.ui.statusbar.showMessage('Поиск в {0}. Найдено {1} элементов.'.format(self.ui.message_view.model().get_context_name(),
                    self.ui.message_view.model().rowCount() - len(found_messages)))
            else:
                self.ui.statusbar.showMessage('Контекст не выбран!')
        else:
            found = list(filter(lambda x: x != [], self.ui.context_view.model().search_messages(line)))
            f = []
            [f.extend(x) for x in found if x!=[]]
            context = ContextItem('Найдено', f)
            self.ui.message_view.model().setContext(context)
            self.ui.statusbar.showMessage('Найдено {0} элементов'.format(len(f)))
        return True

    # добавление нового контекста в конец
    def add_context(self):
        name, _ = QtWidgets.QInputDialog.getText(self, 'Новый контекст', 'Введите название нового контекста')
        if _ == True and name != '':
            self.ui.context_view.model().add_context(name)
            self.ui.statusbar.showMessage('Контекст добавлен.')

    # добавление нового сообщения в конец
    def add_message(self):
        name, _ = QtWidgets.QInputDialog.getText(self, 'Новое сообщение', 'Введите исходный текст нового сообщения')
        if _ == True and name != '':
            if self.ui.message_view.model().isContextSetted() == True:
                self.ui.message_view.model().add_message(name)
                self.ui.statusbar.showMessage('Сообщение добавлено.')
            else:
                self.ui.statusbar.showMessage('Контекст не выбран.')

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Enter or e.key() == QtCore.Qt.Key_Return:
            if self.centralWidget().focusWidget() is self.ui.context_searchLine:
                self.search_context()
            if self.centralWidget().focusWidget() is self.ui.message_searchLine:
                self.search_message()
        elif e.key() == QtCore.Qt.Key_Save:
            self.save()
        elif e.key() == QtCore.Qt.Key_Open:
            self.load()

    # показываются скрытые контексты
    def showAllContexts(self):
        for n in self.hidden_contexts:
            self.ui.context_view.setRowHidden(n, False)
        self.hidden_contexts = []

    # показываются скрытые сообщения
    def showAllMessages(self):
        for n in self.hidden_messages:
            self.ui.message_view.setRowHidden(n, False)
        self.hidden_messages = []

    def resizeEvent(self, a0: QtGui.QResizeEvent):
        print(a0.size())
        print(a0.oldSize())
        if a0.oldSize() != QtCore.QSize(-1,-1):
            width = a0.size().width() - a0.oldSize().width()
            height = a0.size().height() - a0.oldSize().height()
            w = self.ui.context_view.width()
            h = self.ui.context_view.height()
            self.ui.context_view.resize(w + width/3, h + height)
            self.ui.message_view.setGeometry(w + width/3 + 50, 70, w + width/3, h + height)
            # кнопки для работы с представлениями
            self.ui.context_viewTools.setGeometry(w + width / 3, 70, 40, 170)
            self.ui.message_viewTools.setGeometry(2 * w + 2 *width / 3 + 50, 70, 40, 170)
            # окна редактирования сообщения
            w_boxes = self.ui.source_editBox.width()
            h_boxes = self.ui.source_editBox.height()
            self.ui.source_editBox.setGeometry(2*w + 100 + 2 * width/3, 60, w_boxes + width/3, h_boxes + height/3)
            w_editors = self.ui.sourceText.width()
            h_editors = self.ui.sourceText.height()
            self.ui.sourceText.resize(w_editors + width/3, h_editors + height / 3)
            self.ui.ru_transText.resize(w_editors + width/3, h_editors + height / 3)
            self.ui.en_transText.resize(w_editors + width/3, h_editors + height / 3)
            self.ui.btChange_source.setGeometry(w_boxes + width/3 - 120, h_boxes + height/3 - 40, 93, 28)
            self.ui.btChange_rus.setGeometry(w_boxes + width/3 - 120, h_boxes + height/3 - 40, 93, 28)
            self.ui.btChange_eng.setGeometry(w_boxes + width/3 - 120, h_boxes + height/3 - 40, 93, 28)

            self.ui.ru_transBox.setGeometry(2 * w + 100 + 2 * width / 3, 90 + h_boxes + height / 3, w_boxes + width / 3, h_boxes + height / 3)
            self.ui.en_transBox.setGeometry(2 * w + 100 + 2 * width / 3, 120 + h_boxes * 2 + height * 2 /3, w_boxes + width / 3, h_boxes + height / 3)
            # поиск
            self.ui.search_message.setGeometry(w + width/3 + 50, -1, 430, 51)
            self.ui.btLoad.setGeometry(a0.size().width() - 256, 20, 100, 30)
            self.ui.btSave.setGeometry(a0.size().width() - 136, 20, 100, 30)
            self.ui.line_2.resize(2 * w + 2 * width/3 + 101, 20)
            self.ui.line.setGeometry(2 * w + 2 * width / 3 + 82, 60, 20, h + height + 10)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = Window()
    main.show()
    sys.exit(app.exec_())