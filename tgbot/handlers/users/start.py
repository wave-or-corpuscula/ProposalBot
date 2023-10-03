import logging

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext

from tgbot.states.app_states import AppStates


async def bot_start(message: types.Message, state: FSMContext):
    keyboard = message.bot.db.get_types_keyboard()

    await state.set_state(AppStates.choose_message_type)
    await message.answer("Выберите тип сообщения:", reply_markup=keyboard)

    
def register_start(dp: Dispatcher):
    dp.register_message_handler(bot_start, CommandStart())
