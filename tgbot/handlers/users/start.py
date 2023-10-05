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

async def help(message: types.Message):
    keyboard = message.bot.kcreator.get_types_keyboard()
    answer = [
        "Этот бот нужен для связи с администрацией университета.",
        "<b>Как это работает?</b>",
        "  <i>1. Сначала выберите тему сообщения.</i>",
        "  <i>2. Напишите сообщение и отправте его боту. Оно отобразится у администрации</i> <b><u>АНОНИМНО</u></b>.",
        "  <i>3. Можете ждать ответа, а можете написать ещё.</i>",
        "\nВыберите тип сообщения:"
    ]
    await message.answer("\n".join(answer), reply_markup=keyboard)

# async def admin_help(message: types.Message):
#     keyboard = message.bot.kcreator.get_types_keyboard()
#     answer = [
#         "Вы - администратор",
#         "Если у вас какие-то вопросы, свяжитесь с разработчиком данного бота:",
#         "@wave-or-corpuscula"
#     ]
#     await message.answer("\n".join(answer), reply_markup=keyboard)

def register_start(dp: Dispatcher):
    dp.register_message_handler(bot_start, CommandStart())
    dp.register_message_handler(help, commands=["help"], state=UserStates.choose_message_type)
