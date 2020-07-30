from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt, QVariant
from PyQt5.QtGui import QColor, QBrush
import xml.etree.ElementTree as ET
from ContextItem import ContextItem, MessageItem

class ContextsTableModel(QAbstractTableModel):
    contexts = []
    def __init__(self, filename):
        QAbstractTableModel.__init__(self)
        self.load_data(filename)

    # возвращаем число строк в данных в модели
    def rowCount(self, parent=QModelIndex()):
        return len(self.contexts)

    def columnCount(self, parent=QModelIndex()):
        return 2

    def get_context(self, index):
        return self.contexts[index.row()]

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
        # читаем файлы
        tree = ET.parse(filename)
        root = tree.getroot()
        for c in root:
            try:
                name = c.find('name').text
                context = ContextItem(name)
                for m in c.findall('message'):
                    source = m.find('source').text
                    # translate = m.find('translation').text
                    message = MessageItem(context)
                    message.set_source(source)
                    context.add_message(message)
                self.contexts.append(context)
            except AttributeError:
                continue

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