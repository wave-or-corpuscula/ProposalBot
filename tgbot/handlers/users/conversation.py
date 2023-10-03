import logging

from tgbot.states.app_states import AppStates

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext


async def choose_message_type(call: types.CallbackQuery, state: FSMContext):
    type_name = call.message.bot.db.get_type_name(call.data)
    await state.update_data(type_id=call.data, 
                            type_name=type_name)
    await state.set_state(AppStates.typeing_message)
    await call.message.edit_text("Введите сообщение на тему: " + type_name)

async def send_message_to_buliga(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    username = f"@{message.from_user.username}"

    keyboard = message.bot.db.get_types_keyboard()
    config = message.bot.get("config")
    for admin in config.tg_bot.admin_ids:
        try:
            await message.bot.forward_message(admin, message.chat.id, message.message_id)
        except Exception as e:
            print(e)
            logging.warning(f"Cannot send message to admin {admin}")
            answer = [
                "Ошибка при отправке сообщения!",
                "Можете попробовать еще раз:"
            ]
            await message.answer("\n".join(answer), reply_markup=keyboard)
            await state.set_state(AppStates.choose_message_type)
            return
        finally:
            await state.set_state(AppStates.choose_message_type)

    answer = [
        "Сообщение успешно отправлено!",
        "Чтобы отправить еще одно, выберите тему сообщения:"
    ]
    await message.answer("\n".join(answer), reply_markup=keyboard)
    
    message.bot.db.add_message(message.from_user.id, username, message.text, user_data["type_id"])


async def answer_message(message: types.Message):

    # await message.reply_to_message.delete()
    # await message.delete()
    
    user_id = message.reply_to_message.forward_from.id
    text = f"Текст вопроса: {message.reply_to_message.text}\n\n" \
                f"Ответ: {message.text}"
    await message.bot.send_message(user_id, text)

def register_conversation(dp: Dispatcher):
    dp.register_callback_query_handler(choose_message_type, state=AppStates.choose_message_type)
    dp.register_message_handler(send_message_to_buliga, state=AppStates.typeing_message)
    dp.register_message_handler(answer_message, is_reply_forwarded=True, state="*", is_admin=True)
