from PyQt5.QtCore import QObject

class ContextItem(QObject):
    def __init__(self, contex_name):
        # self.parent_item = parent_item
        self.contex_name = contex_name
        self.message_items = []

    def get_name(self):
        return self.contex_name

    def rename(self, name):
        self.contex_name = name

    def get_messages_count(self):
        return len(self.message_items)

    def get_message(self, c):
        return self.message_items[c]

    def add_message(self, message):
        self.message_items.append(message)

    def insert_message(self, index, message):
        self.message_items.insert(index, message)

    def findMessageInContext(self, source):
        for m in self.message_items:
            if m.get_source() == source:
                return m
        return None

    def iterator(self):
        return iter(self.message_items)

    def delete_message(self, index):
        self.message_items.pop(index)


class MessageItem(QObject):
    def __init__(self, parent):
        self.parent = parent
        self.source = ''
        self.translation_ru = ''
        self.translation_en = ''


    def set_source(self, string):
        self.source = string

    def set_translation(self, string, language):
        if language.find('ru') != -1:
            self.translation_ru = string
        else:
            self.translation_en = string

    def get_source(self):
        return self.source

    def get_translations(self):
        return self.translation_ru, self.translation_en

    def get_translation(self, language):
        if language.find('ru') == -1:
            return self.translation_en
        else:
            return self.translation_ru


