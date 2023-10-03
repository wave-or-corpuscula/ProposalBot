from tgbot.utils.db_api.sqlite import DataBase
from . import Config, load_config
import asyncio


async def test():

    print(db.get_types())

config = load_config("../../../.env")
loop = asyncio.get_event_loop()
db = DataBase(loop, config)
loop.run_until_complete(test())


