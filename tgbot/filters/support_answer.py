import typing 

from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message


class ReplyToBot(BoundFilter):
    key = "reply_to_bot"


    def __init__(self, reply_to_bot: typing.Optional[bool] = None):
        self.reply_to_bot = reply_to_bot

    async def check(self, obj: Message):
        if obj.reply_to_message is None:
            return False
        return obj.reply_to_message.from_user.is_bot


class ReplyToUser(BoundFilter):
    key = "reply_to_user"


    def __init__(self, reply_to_user: typing.Optional[bool] = None):
        self.reply_to_user = reply_to_user

    async def check(self, obj: Message):
        if obj.reply_to_message is None:
            return False
        return obj.reply_to_message.from_user.is_bot
