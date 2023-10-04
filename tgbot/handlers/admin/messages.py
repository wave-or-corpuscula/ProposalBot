import logging

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from tgbot.states.admin_states import AdminStates
from tgbot.keyboards.inline.admin import messages_menu, admin_menu


async def show_message_menu(call: types.CallbackQuery):
    await AdminStates.messages_menu.set()
    await call.message.edit_text("Выберите подходящий пункт:", reply_markup=messages_menu)

async def back_to_admin_menu(call: types.CallbackQuery):
    await AdminStates.admin_main_menu.set()
    await call.message.edit_text("Выберите действие:", reply_markup=admin_menu)
    


def register_messages(dp: Dispatcher):
    dp.register_callback_query_handler(show_message_menu, 
                                       callback_data="messages",
                                       state=AdminStates.admin_main_menu)
    dp.register_callback_query_handler(back_to_admin_menu, 
                                       callback_data="back",
                                       state=AdminStates.messages_menu)