from telegram.ext import Filters


class SpecificTextHandler(Filters._Text):
    name = 'Filters.specific_text'

    def __init__(self, command_text):
        self.command_text = command_text

    def filter(self, message):  # noqa
        return super().filter(message) and message.text == self.command_text
