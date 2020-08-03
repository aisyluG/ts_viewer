from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt, QVariant
from PyQt5.QtGui import QColor, QBrush
import xml.etree.ElementTree as ET
from ContextItem import ContextItem, MessageItem

class ContextsTableModel(QAbstractTableModel):
    def __init__(self):
        QAbstractTableModel.__init__(self)
        self.contexts = []
        self.encoding_info = ''
        self.version = ''

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
        with open(filename, 'r', encoding='utf-8') as file:
            self.encoding_info = self.encoding_info + file.readline()
        # оповещаем об изменении модели
        self.beginResetModel()
        # читаем файл
        tree = ET.parse(filename)
        root = tree.getroot()
        # узнаем язык переводов
        language = root.attrib['language']
        self.version = root.attrib['version']
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
                    for n, mes in enumerate(c.findall('message')):
                        source = mes.find('source').text
                        translation = mes.find('translation').text
                        # ищем в контексте сообщением с теми же исходными данными
                        message = context.findMessageInContext(source)
                        # если нет, то создаем новое сообщение
                        if message is None:
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
        if Qt_Orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if section == 0:
                return 'Контекст'
            else:
                return 'Записи'
        return QVariant()

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

    def add_context(self, name):
        count = len(self.contexts)
        self.beginInsertRows(QModelIndex(), count, count + 1)
        index = self.index(count, 0)
        self.setData(index, ContextItem(name))
        self.endInsertRows()

    def insert_context(self, name, index):
        self.beginInsertRows(QModelIndex(), index, index + 1)
        self.setData(self.index(index, 0), ContextItem(name))
        self.endInsertRows()

    def save_data(self, filename, language):
        if language.find('ru') == -1:
            mode = 'en_En'
        else:
            mode = 'ru_Ru'
        with open(filename, 'w', encoding='utf-8') as file:
            file.writelines(self.encoding_info)
            file.write('<TS language="{0}" version="{1}">\n'.format(mode, self.version))
            for context in self.contexts:
                file.write('<context>\n')
                file.write('{0}<name>{1}</name>\n'.format(' '*4, context.get_name()))
                for message in context.iterator():
                    file.write('{0}<message>\n'.format(' '*4))
                    file.write('{0}<source>{1}</source>\n'.format(' '*8, message.get_source()))
                    file.write('{0}<translation>{1}</translation>\n'.format(' '*8, message.get_translation(mode)))
                    file.write('{0}</message>\n'.format(' '*4))
                file.write('</context>\n')
            file.write('</TS>\n')



class MessagesTableModel(QAbstractTableModel):
    def __init__(self):
        QAbstractTableModel.__init__(self)
        self.context = None

    def isContextSetted(self):
        if self.context is None:
            return False
        return True

    def get_message_translations(self, index):
        row = index.row()
        return self.context.get_message(row).get_translations()

    def get_messages_count(self):
        if self.context is None:
            return 0
        return self.context.get_messages_count()

    def setContext(self, context):
        self.beginResetModel()
        self.context = context
        # for i in range(0, context.get_messages_count()):
        #     self.setData(self.index(i, 0), context.get_message(i))
        self.endResetModel()
        # self.messages = [context.get_message(i) for i in range(0, self.messages_count)]

    def setData(self, index, data, role=Qt.DisplayRole):
        # если элемент не редактируем, то изменения не вносятся
        if role != Qt.DisplayRole:
            return False
        self.context.insert_message(index.row(), data)
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

    def search_message(self, string):
        for n, message in enumerate(self.context.iterator()):
            print(message.get_source().lower().find('ct'))
            if message.get_source().lower().find(string.lower()) == -1:
                continue
            else:
                return self.index(n, 0)
        return None

    def set_message_translation(self, language, index, translation):
        self.context.get_message(index.row()).set_translation(translation, language)

    def set_message_source(self, index, source):
        self.context.get_message(index.row()).set_source(source)
        self.dataChanged.emit(index, index)

    def add_message(self, source):
        count = self.get_messages_count()
        self.beginInsertRows(QModelIndex(), count, count + 1)
        index = self.index(count, 0)
        message = MessageItem(self.context)
        message.set_source(source)
        self.setData(index, message)
        self.endInsertRows()

    def insert_message(self, source, index):
        self.beginInsertRows(QModelIndex(), index, index + 1)
        message = MessageItem(self.context)
        message.set_source(source)
        self.setData(self.index(index, 0), message)
        self.endInsertRows()