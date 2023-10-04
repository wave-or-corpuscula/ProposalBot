import logging

from datetime import timedelta, datetime

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from tgbot.states.admin_states import AdminStates
from tgbot.keyboards.inline.admin import admin_menu, types_edit_menu


async def admin_started(message: types.Message):
    await AdminStates.admin_main_menu.set()
    await message.answer("Выберите действие:", reply_markup=admin_menu)


async def notify_admins(dp: Dispatcher):
    for admin in dp.bot.get("config").tg_bot.admin_ids:
        try:
            await dp.bot.send_message(admin, "Бот запущен!")
        except Exception:
            logging.warning(f"Cannot send message to admin {admin}")


async def topics_main_menu(call: types.CallbackQuery):
    await AdminStates.topic_changing_menu.set()
    await call.message.edit_text("Выберите подходящее:", reply_markup=types_edit_menu)


async def back_from_topic_changing(call: types.CallbackQuery):
    await AdminStates.admin_main_menu.set()
    await call.message.edit_text("Выберите действие:", reply_markup=admin_menu)


async def list_delete_topics(call: types.CallbackQuery):
    keyboard = call.message.bot.db.get_types_edit_keyboard()
    await AdminStates.del_topic.set()
    await call.message.edit_text("Выберите тему для удаления:", reply_markup=keyboard)


async def delete_topic(call: types.CallbackQuery):
    call.message.bot.db.del_topic(call.data)
    answer = [
        "<i>Тема успешно удалена!</i>",
        "Выберите действие:"
    ]
    await AdminStates.admin_main_menu.set()
    await call.message.edit_text("\n".join(answer), reply_markup=admin_menu)


async def forbidden_to_delete_topic(call: types.CallbackQuery):
    keyboard = call.message.bot.db.get_types_edit_keyboard()
    answer = [
        "<i>Вы не можете удалить <u>эту</u> тему!</i>",
        "Выберите <b>другую</b> тему для удаления: " 
    ]
    await AdminStates.del_topic.set()
    await call.message.edit_text("\n".join(answer), reply_markup=keyboard)    


async def abort_delete_topic(call: types.CallbackQuery):
    answer = [
        "<i>Удаление отменено!</i>",
        "Выберите действие:"
    ]
    await AdminStates.admin_main_menu.set()
    await call.message.edit_text("\n".join(answer), reply_markup=admin_menu)


async def send_new_topic_name(call: types.CallbackQuery):
    await AdminStates.waiting_for_new_topic_name.set()
    await call.message.edit_text("Введите название новой темы (или 'Назад', для отмены):", reply_markup=None)


async def add_topic(message: types.Message):
    
    if message.text.lower() == "назад":
        answer = [
        "<i>Добавление отменено!</i>",
        "Выберите действие:"
        ]
    else:
        message.bot.db.add_topic(message.text)
        answer = [
            "<i>Тема успешно добавлена!</i>",
            "Выберите действие:"
        ]
    await AdminStates.admin_main_menu.set()
    await message.answer("\n".join(answer), reply_markup=admin_menu)


def register_topics_managing(dp: Dispatcher):
    dp.register_message_handler(admin_started, commands=["start"], state="*", is_admin=True)
    dp.register_callback_query_handler(topics_main_menu, callback_data="edit_topics", state=AdminStates.admin_main_menu)
    dp.register_callback_query_handler(list_delete_topics, callback_data="del_topic", state=AdminStates.topic_changing_menu)
    dp.register_callback_query_handler(send_new_topic_name, callback_data="add_topic", state=AdminStates.topic_changing_menu)
    dp.register_message_handler(add_topic, state=AdminStates.waiting_for_new_topic_name)
    dp.register_callback_query_handler(back_from_topic_changing, callback_data="back", state=AdminStates.topic_changing_menu)
    dp.register_callback_query_handler(abort_delete_topic, callback_data="back", state=AdminStates.del_topic)
    dp.register_callback_query_handler(forbidden_to_delete_topic, callback_data="1", state=AdminStates.del_topic)
    dp.register_callback_query_handler(delete_topic, state=AdminStates.del_topic)
    