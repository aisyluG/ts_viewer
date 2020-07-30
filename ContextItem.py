from PyQt5.QtCore import QObject

class ContextItem(QObject):
    def __init__(self, contex_name):
        # self.parent_item = parent_item
        self.contex_name = contex_name
        self.message_items = []

    def get_name(self):
        return self.contex_name

    def get_messages_count(self):
        return len(self.message_items)

    def get_message(self, c):
        return self.message_items[c]

    def add_message(self, message):
        self.message_items.append(message)

    def insert_message(self, message, index):
        self.message_items.insert(index, message)


class MessageItem(QObject):
    def __init__(self, parent):
        self.parent = parent
        self.source = ''
        self.translation_ru = ''
        self.translation_en = ''


    def set_source(self, string):
        self.source = string

    def set_ru_translation(self, string):
        self.translation_ru = string

    def set_en_translation(self, string):
        self.translation_en = string

    def get_source(self):
        return self.source

    def get_translations(self):
        return self.translation_ru, self.translation_en


