from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt, QVariant
from PyQt5.QtGui import QColor, QBrush
from ContextItem import MessageItem

class MessagesTableModel(QAbstractTableModel):
    def __init__(self):
        QAbstractTableModel.__init__(self)
        self.context = None

    def isContextSetted(self):
        if self.context is None:
            return False
        return True

    def get_context_name(self):
        return self.context.get_name()

    def get_message(self, index):
        row = index.row()
        return self.context.get_message(row)

    def get_messages_count(self):
        if self.context is None:
            return 0
        return self.context.get_messages_count()

    def setContext(self, context):
        self.beginResetModel()
        self.context = context
        self.endResetModel()

    def setData(self, index, data, role=Qt.DisplayRole):
        # если элемент не редактируем, то изменения не вносятся
        if role != Qt.EditRole:
            return False
        self.context.get_message(index.row()).set_source(data)
        self.dataChanged.emit(index, index)
        return True

    def columnCount(self, parent=QModelIndex()):
        return 1

    def rowCount(self, parent=QModelIndex()):
        return self.get_messages_count()

    def data(self, index, role=Qt.DisplayRole):
        row = index.row()
        if self.context is None:
            return QVariant()
        # если отображаемые или редактируемые данные
        if role == Qt.EditRole or role == Qt.DisplayRole:
            return self.context.get_message(row).get_source()
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
        if Qt_Orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return 'Cooбщение'
        return QVariant()

    def messages_to_hide(self, string):
        hide = []
        for n, message in enumerate(self.context.iterator()):
            if message.find(string) == False:
                hide.append(n)
        return hide

    def set_message_translation(self, language, index, translation):
        self.context.get_message(index.row()).set_translation(translation, language)

    def set_message_source(self, index, source):
        self.context.get_message(index.row()).set_source(source)
        self.dataChanged.emit(index, index)

    def add_message(self, source):
        count = self.get_messages_count()
        self.beginInsertRows(QModelIndex(), count, count)
        index = self.index(count, 0)
        message = MessageItem(self.context)
        message.set_source(source)
        self.context.add_message(message)
        self.endInsertRows()

    def insert_message(self, source, index):
        self.beginInsertRows(QModelIndex(), index, index)
        message = MessageItem(self.context)
        message.set_source(source)
        self.context.insert(index, message)
        self.endInsertRows()

    def delete_message(self, row):
        self.beginRemoveRows(QModelIndex(), row, row)
        self.context.delete_message(row)
        self.endRemoveRows()

    # метод, возвращающийкомбинацию флагов, соответствующую каждому элементу
    def flags(self, index):
        # если элемент в столбце с пересчитываемыми значениями, то он нередактируем
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable
