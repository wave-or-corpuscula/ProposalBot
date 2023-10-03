import typing

from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message


class IsReplyForwarded(BoundFilter):
    key = "is_reply_forwarded"


    def __init__(self, is_reply_forwarded: typing.Optional[bool] = None):
        self.is_reply_forwarded = is_reply_forwarded

    async def check(self, obj: Message):
        if obj.reply_to_message is None:
            return False
        if obj.reply_to_message.forward_from is None:
            return False
        else:
            return True