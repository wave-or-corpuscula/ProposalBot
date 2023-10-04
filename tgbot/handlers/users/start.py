import logging

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext

from tgbot.states.user_states import UserStates


async def bot_start(message: types.Message, state: FSMContext):

    keyboard = message.bot.kcreator.get_types_keyboard()
    message.bot.db.add_user(message.from_user.id, 
                            message.from_user.username, 
                            message.from_user.first_name, 
                            message.from_user.last_name)

    await state.set_state(UserStates.choose_message_type)
    await message.answer("Выберите тип сообщения:", reply_markup=keyboard)

    
def register_start(dp: Dispatcher):
    dp.register_message_handler(bot_start, CommandStart())
