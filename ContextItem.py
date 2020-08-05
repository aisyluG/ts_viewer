from PyQt5.QtCore import QObject

class ContextItem(QObject):
    def __init__(self, contex_name, messages=None):
        # имя контекста
        self.contex_name = contex_name
        # сообщения контекста
        if messages is None:
            self.message_items = []
        else:
            self.message_items = messages

    # имя контекста
    def get_name(self):
        return self.contex_name

    # переименовывание контекста
    def rename(self, name):
        self.contex_name = name

    # число сообщений контекста
    def get_messages_count(self):
        return len(self.message_items)

    # сообщение контекста но номеру
    def get_message(self, c):
        return self.message_items[c]

    # добавление нового сообщения в конец списка
    def add_message(self, message):
        self.message_items.append(message)

    # вставка нового сообщения по индексу
    def insert_message(self, index, message):
        self.message_items.insert(index, message)

    # поиск сообщения по исходному тексту
    # возвращает номер контекста
    def searchMessageInContext(self, source):
        for n, m in enumerate(self.message_items):
            if m.get_source() == source:
                return n
        return None

    # итератор по списку сообщений контекста
    def iterator(self):
        return iter(self.message_items)

    # удаление сообщения по заданному номеру
    def delete_message(self, index):
        self.message_items.pop(index)

    # поиск сообщений, содержащих заданную подстроку в исходном тексте или подстроке
    def search_messages(self, string):
        found = []
        for message in self.iterator():
            if message.find(string) == True:
                found.append(message)
        return found


class MessageItem(QObject):
    def __init__(self, parent):
        # родительский контекст сообщений
        self.parent = parent
        # исходный текст
        self.source = ''
        # перевод на русский
        self.translation_ru = ''
        # перевод на английский
        self.translation_en = ''

    # родительский контекст сообщения
    def get_parent(self):
        return self.parent

    # задание исходного текста сообщения
    def set_source(self, string):
        self.source = string

    # задание перевода сообщения
    def set_translation(self, string, language):
        if string is not None:
            if language.find('ru') != -1:
                self.translation_ru = string
            else:
                self.translation_en = string

    # исходный текст
    def get_source(self):
        return self.source

    # переводы
    def get_translations(self):
        return self.translation_ru, self.translation_en

    # перевод на конкретном языке
    def get_translation(self, language):
        if language.find('ru') == -1:
            return self.translation_en
        else:
            return self.translation_ru

    # поиск подстроки в исходном тексте и переводах сообщения
    def find(self, string):
        s = string.lower()
        if self.source.lower().find(s) == -1 and self.translation_ru.lower().find(s) == -1 and self.translation_en.lower().find(s) == -1:
            return False
        return True


