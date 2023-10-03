import logging

from tgbot.states.app_states import AppStates

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import ChatNotFound


async def choose_message_type(call: types.CallbackQuery, state: FSMContext):
    topic_name = call.message.bot.db.get_type_name(call.data)
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
        "Сообщение успешно отправлено!",
        "Чтобы отправить еще одно, выберите тему сообщения:"
    ]
    await message.answer("\n".join(answer), reply_markup=keyboard)


async def answer_message(message: types.Message):

    # await message.reply_to_message.delete()
    # await message.delete()
    
    user_id = message.reply_to_message.forward_from.id
    text = f"Текст вопроса: {message.reply_to_message.text}\n\n" \
                f"Ответ: {message.text}"
    await message.bot.send_message(user_id, text)

def register_conversation(dp: Dispatcher):
    dp.register_callback_query_handler(choose_message_type, state=AppStates.choose_message_type)
    dp.register_message_handler(add_message_to_db, state=AppStates.typeing_message)
    dp.register_message_handler(answer_message, is_reply_forwarded=True, state="*", is_admin=True)
