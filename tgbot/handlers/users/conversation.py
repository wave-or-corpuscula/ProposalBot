import logging

from tgbot.states.app_states import AppStates

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext


async def choose_message_type(call: types.CallbackQuery, state: FSMContext):
    topic_name = call.message.bot.db.get_topic_name(call.data)
    await state.update_data(topic_id=call.data, 
                            topic_name=topic_name)
    await state.set_state(AppStates.typeing_message)
    await call.message.edit_text("Введите сообщение на тему: " + topic_name)

async def add_message_to_db(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    keyboard = message.bot.db.get_types_keyboard()

    message.bot.db.add_message(message.message_id,
                               message.from_user.id, 
                               user_data["topic_id"],
                               message.text)
    answer = [
        "<i>Сообщение успешно отправлено!</i>",
        "Чтобы отправить еще одно, выберите тему сообщения:"
    ]
    await state.set_state(AppStates.choose_message_type)
    await message.answer("\n".join(answer), reply_markup=keyboard)


def register_conversation(dp: Dispatcher):
    dp.register_callback_query_handler(choose_message_type, state=AppStates.choose_message_type)
    dp.register_message_handler(add_message_to_db, state=AppStates.typeing_message)
