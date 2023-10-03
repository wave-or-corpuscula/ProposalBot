import asyncio

import nest_asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from tgbot.config import load_config

from tgbot.handlers.users.echo import register_echo
from tgbot.handlers.users.admin import register_admin, notify_admins
from tgbot.handlers.users.start import register_start
from tgbot.handlers.users.conversation import register_conversation

from tgbot.handlers.errors.error_handler import register_error_handler

from tgbot.filters.admin import AdminFilter
from tgbot.filters.is_reply_forwarded import IsReplyForwarded
from tgbot.filters.support_answer import ReplyToBot, ReplyToUser
from tgbot.filters.callback_data import CallbackDataFilter
from tgbot.filters.text import TextFilter

from tgbot.utils.db_api.sqlite import DataBase


async def on_startup(dp: Dispatcher, db: DataBase):
    db.create_tables()
    await notify_admins(dp)


def register_all_handlers(dp):
    register_admin(dp)
    register_start(dp)
    register_conversation(dp)
    register_error_handler(dp)
    register_echo(dp)


def register_all_filters(dp: Dispatcher):
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(CallbackDataFilter)
    dp.filters_factory.bind(IsReplyForwarded)
    dp.filters_factory.bind(TextFilter)
    dp.filters_factory.bind(ReplyToUser)
    dp.filters_factory.bind(ReplyToBot)


async def main():

    nest_asyncio.apply()
    
    config = load_config(".env")

    loop = asyncio.get_event_loop()
    
    storage  = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    dp = Dispatcher(bot, storage=storage, loop=loop)
    db = DataBase(config)

    bot["config"] = config
    bot.db = db

    register_all_filters(dp)
    register_all_handlers(dp)

    try: 
        await on_startup(dp, db)
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped!")
