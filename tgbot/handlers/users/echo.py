from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hcode


async def bot_echo(message: types.Message):
    await message.delete()
    # text = [
    #     "Эхо без состояния.",
    #     "Сообщение:",
    #     message.text,
    # ]
    # await message.answer("\n".join(text))
    
    
async def bot_echo_all(message: types.Message, state: FSMContext):
    await message.delete()
    # state_name = await state.get_state()
    # text = [
    #     f"Эхо в состоянии {hcode(state_name)}",
    #     "Содержание сообщения:",
    #     hcode(message.text)
    # ]
    # await message.answer("\n".join(text))


def register_echo(dp: Dispatcher):
    dp.register_message_handler(bot_echo, content_types=types.ContentTypes.ANY)
    dp.register_message_handler(bot_echo_all, state="*", content_types=types.ContentTypes.ANY)
