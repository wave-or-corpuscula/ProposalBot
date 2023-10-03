from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class TextFilter(BoundFilter):
    key: str = 'text'

    def __init__(self, text: str):
        self.text = text

    async def check(self, obj: types.Message):
        return obj.text.lower() == self.text
    