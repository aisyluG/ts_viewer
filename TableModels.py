from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt, QVariant
from PyQt5.QtGui import QColor, QBrush
import xml.etree.ElementTree as ET
from ContextItem import ContextItem, MessageItem

class ContextsTableModel(QAbstractTableModel):
    contexts = []
    def __init__(self):
        QAbstractTableModel.__init__(self)

    # возвращаем число строк в данных в модели
    def rowCount(self, parent=QModelIndex()):
        return len(self.contexts)

    def columnCount(self, parent=QModelIndex()):
        return 2

    def get_context(self, index):
        return self.contexts[index.row()]

    def setData(self, index, value, role=Qt.DisplayRole):
        # если элемент не редактируем, то изменения не вносятся
        if role != Qt.DisplayRole:
            return False
        self.contexts.insert(index.row(), value)
        self.dataChanged.emit(index, index)
        return True

    def data(self, index, role):
        column = index.column()
        row = index.row()
        # если отображаемые или редактируемые данные
        if role == Qt.EditRole or role == Qt.DisplayRole:
            if column == 0:
                return self.contexts[row].get_name()
            else:
                return self.contexts[row].get_messages_count()
        # если цвет фона
        if role == Qt.BackgroundColorRole:
            if row % 2 == 0:
                return QBrush(QColor('#eaeaf0'))
            else:
                return QBrush(QColor('#ffffff'))
        else:
            return QVariant()

    def load_data(self, filename):
        # оповещаем об изменении модели
        self.beginResetModel()
        # читаем файл
        tree = ET.parse(filename)
        root = tree.getroot()
        # узнаем язык переводов
        language = root.attrib['language']
        # для каждого контекста в файле
        for n, c in enumerate(root):
            name = c.find('name')
            # если контекст не имеет имя, то называем его 'no name'
            if name is None:
                context = ContextItem('no name')
            # иначе ищем его  в модели
            else:
                context = self.findContextInModel(name.text)
                # если контекста с таким именем нет в модели, то создаем новый контекст
                if context is None:
                    context = ContextItem(name.text)
                # иначе дополняем новыми сообщениями, если они есть
                else:
                    print('*')
                    for n, mes in enumerate(c.findall('message')):
                        print('+')
                        source = mes.find('source').text
                        translation = mes.find('translation').text
                        # ищем в контексте сообщением с теми же исходными данными
                        message = context.findMessageInContext(source)
                        # если нет, то создаем новое сообщение
                        if message is None:
                            print('/')
                            message = MessageItem(context)
                            message.set_source(source)
                            # добавляем сообщение в контекст
                            context.insert_message(n, message)
                        # устанавливаем перевод
                        message.set_translation(translation, language)
                    continue
            # если был создан новый контекст, то заполняем его сообщениями
            for mes in c.findall('message'):
                source = mes.find('source').text
                translation = mes.find('translation').text
                message = MessageItem(context)
                message.set_source(source)
                # устанавливаем перевод
                message.set_translation(translation, language)

                # добавляем сообщение в контекст
                context.add_message(message)
            self.setData(self.index(n, 0), context)
        self.endResetModel()

    def index(self, row, column, parent=QModelIndex()):
        return self.createIndex(row, column)

    def headerData(self, section, Qt_Orientation, role=Qt.DisplayRole):
        if role == Qt.BackgroundColorRole:
            return QBrush(QColor('#7e8d95'))
        if Qt_Orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if section == 0:
                return 'Контекст'
            else:
                return 'Записи'
        return None #QVariant()

    def search_context(self, string):
        for n, context in enumerate(self.contexts):
            if context.get_name().lower().find(string.lower()) == -1:
                continue
            else:
                return self.index(n, 0)
        return None

    def findContextInModel(self, name):
        for c in self.contexts:
            if c.get_name() == name:
                return c
        return None

class MessagesTableModel(QAbstractTableModel):
    def __init__(self):
        QAbstractTableModel.__init__(self)
        self.context = None
        self.messages_count = 0
        self.messages = []

    def get_message_translations(self, index):
        row = index.row()
        return self.messages[row].get_translations()


    def setContext(self, context):
        self.beginResetModel()
        self.context = context
        self.messages_count = context.get_messages_count()
        for i in range(0, self.messages_count):
            self.setData(self.index(i, 0), context.get_message(i))
        self.endResetModel()
        # self.messages = [context.get_message(i) for i in range(0, self.messages_count)]

    def setData(self, index, data, role=Qt.DisplayRole):
        # если элемент не редактируем, то изменения не вносятся
        if role != Qt.DisplayRole:
            return False
        self.messages.insert(index.row(), data)
        self.dataChanged.emit(index, index)
        return True

    def columnCount(self, parent=QModelIndex()):
        return 1

    def rowCount(self, parent=QModelIndex()):
        return self.messages_count

    def data(self, index, role=Qt.DisplayRole):
        row = index.row()
        # если отображаемые или редактируемые данные
        if role == Qt.EditRole or role == Qt.DisplayRole:
            return self.messages[row].get_source()
        # если цвет фона
        if role == Qt.BackgroundColorRole:
            if row % 2 == 0:
                return QBrush(QColor('#eaeaf0'))
            else:
                return QBrush(QColor('#ffffff'))
        else:
            return QVariant()

    def index(self, row, column, parent=QModelIndex()):
        return self.createIndex(row, column)

    def headerData(self, section, Qt_Orientation, role=Qt.DisplayRole):
        if role == Qt.BackgroundColorRole:
            return QBrush(QColor('#7e8d95'))
        if Qt_Orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return 'Cooбщение'
        return None  # QVariant()

    def search_message(self, string):
        for n, message in enumerate(self.messages):
            if message.get_source().lower().find(string.lower()) == -1:
                continue
            else:
                return self.index(n, 0)
        return None