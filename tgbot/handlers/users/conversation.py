import logging

from tgbot.states.user_states import UserStates

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext


async def choose_message_type(call: types.CallbackQuery, state: FSMContext):
    topic_name = call.message.bot.db.get_topic_name(call.data)
    await state.update_data(topic_id=call.data, 
                            topic_name=topic_name)
    await state.set_state(UserStates.typeing_message)
    await call.message.edit_text("Введите сообщение на тему: " + topic_name)

async def add_message_to_db(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    keyboard = message.bot.kcreator.get_types_keyboard()

    message.bot.db.add_message(message.message_id,
                               message.from_user.id, 
                               user_data["topic_id"],
                               message.text)
    answer = [
        "<b>Сообщение успешно отправлено!</b>",
        "<i>Ответ администрации отобразится здесь же</i>",
        "Чтобы отправить еще одно, выберите тему сообщения:"
    ]
    await state.set_state(UserStates.choose_message_type)
    await message.answer("\n".join(answer), reply_markup=keyboard)


def register_conversation(dp: Dispatcher):
    dp.register_callback_query_handler(choose_message_type, state=UserStates.choose_message_type)
    dp.register_message_handler(add_message_to_db, state=UserStates.typeing_message)
