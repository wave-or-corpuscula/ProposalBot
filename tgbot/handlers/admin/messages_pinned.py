import logging

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from tgbot.states.admin_states import AdminStates
from tgbot.keyboards.inline.admin import messages_menu, admin_menu, back_button
from tgbot.utils.messages_paginator.messages_paginator import MessagesPaginator
from tgbot.handlers.admin.messages import show_message_menu


# Messages pagination

async def pinned_messages_paginate_show(call: types.CallbackQuery, state: FSMContext):
    messages = call.message.bot.db.get_pinned_messages()
    try:
        paginator = MessagesPaginator(messages, 
                                    have_answer_but=False)
        keyboard, message = paginator.get_page()

        await state.update_data(paginator=paginator)
        await AdminStates.pinned_messages_paginating.set()
        await call.message.edit_text(message, reply_markup=keyboard)
    except Exception:
        await AdminStates.messages_menu.set()
        await call.message.edit_text("<b>Избранные отсутствуют!</b>\nВыберите подходящий пункт:", reply_markup=messages_menu)


async def back_from_pinned_messages_pagination(call: types.CallbackQuery, state: FSMContext):
    await state.reset_data()
    await show_message_menu(call)


async def pinned_next_page(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    paginator: MessagesPaginator = data["paginator"]
    try:
        keyboard, message = paginator.next_page()
        await state.update_data(paginator=paginator)
        await call.message.edit_text(message, reply_markup=keyboard)
    except Exception:
        pass


async def pinned_prev_page(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    paginator: MessagesPaginator = data["paginator"]
    try:
        keyboard, message = paginator.prev_page()
        await state.update_data(paginator=paginator)
        await call.message.edit_text(message, reply_markup=keyboard)
    except Exception:
        pass

# Delete message

async def pinned_message_delete(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    paginator: MessagesPaginator = data["paginator"]
    mes_idtfrs = paginator.get_cur_message_identifiers()
    call.message.bot.db.del_message(mes_idtfrs["message_id"], mes_idtfrs["user_id"])
    try:
        paginator.del_cur_message()
        await state.update_data(paginator=paginator)
        keyboard, message = paginator.get_page()
        await call.message.edit_text("<b>Сообщение успешно удалено!</b>\n" + message, reply_markup=keyboard)
    except Exception:
        await state.reset_data()
        await show_message_menu(call)

# Pin/Unpin message

async def pinned_message_pin(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    paginator: MessagesPaginator = data["paginator"]
    user_message = paginator.get_cur_message()
    if not user_message["pin_id"]:
        call.message.bot.db.pin_message(user_message["message_id"], user_message["user_id"])
    else:
        call.message.bot.db.unpin_message(user_message["message_id"], user_message["user_id"])
    try:
        paginator.del_cur_message()
        keyboard, message = paginator.get_page()
        await state.update_data(paginator=paginator)
        await call.message.edit_text(message, reply_markup=keyboard)
    except Exception:
        await state.reset_data()
        await show_message_menu(call)

    

def register_messages_pinned(dp: Dispatcher):
    dp.register_callback_query_handler(pinned_messages_paginate_show,
                                       callback_data="saved",
                                       state=AdminStates.messages_menu)
    dp.register_callback_query_handler(back_from_pinned_messages_pagination,
                                       callback_data="back",
                                       state=AdminStates.pinned_messages_paginating)
    dp.register_callback_query_handler(pinned_next_page,
                                       callback_data="next",
                                       state=AdminStates.pinned_messages_paginating)
    dp.register_callback_query_handler(pinned_prev_page,
                                       callback_data="previous",
                                       state=AdminStates.pinned_messages_paginating)
    # Delete message
    dp.register_callback_query_handler(pinned_message_delete,
                                       callback_data="delete",
                                       state=AdminStates.pinned_messages_paginating)
    # Pin message
    dp.register_callback_query_handler(pinned_message_pin,
                                       callback_data="star",
                                       state=AdminStates.pinned_messages_paginating)
    
    