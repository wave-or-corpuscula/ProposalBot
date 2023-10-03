import re

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class CallbackDataFilter(BoundFilter):
    key: str = 'callback_data'

    def __init__(self, callback_data: str):
        self.callback_data = callback_data

    async def check(self, obj: types.CallbackQuery):
        try:
            return self.callback_data == obj.data
        except Exception:
            return False
    