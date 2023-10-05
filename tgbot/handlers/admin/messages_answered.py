import logging

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from tgbot.states.admin_states import AdminStates
from tgbot.keyboards.inline.admin import messages_menu, admin_menu, back_button
from tgbot.utils.messages_paginator.messages_paginator import MessagesPaginator
from tgbot.handlers.admin.messages import show_message_menu


# Messages pagination

async def answered_messages_paginate_show(call: types.CallbackQuery, state: FSMContext):
    messages = call.message.bot.db.get_answered_messages()
    try:
        paginator = MessagesPaginator(messages, 
                                    have_answer_but=False, 
                                    have_delete_but=False,
                                    have_star_but=False)
        keyboard, message = paginator.get_page()

        await state.update_data(paginator=paginator)
        await AdminStates.pinned_messages_paginating.set()
        await call.message.edit_text(message, reply_markup=keyboard)
    except Exception:
        await AdminStates.messages_menu.set()
        await call.message.edit_text("<b>Ответы отсутствуют!</b>\nВыберите подходящий пункт:", reply_markup=messages_menu)


async def back_from_answered_messages_pagination(call: types.CallbackQuery, state: FSMContext):
    await state.reset_data()
    await show_message_menu(call)


async def answered_next_page(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    paginator: MessagesPaginator = data["paginator"]
    try:
        keyboard, message = paginator.next_page()
        await state.update_data(paginator=paginator)
        await call.message.edit_text(message, reply_markup=keyboard)
    except Exception:
        pass


async def answered_prev_page(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    paginator: MessagesPaginator = data["paginator"]
    try:
        keyboard, message = paginator.prev_page()
        await state.update_data(paginator=paginator)
        await call.message.edit_text(message, reply_markup=keyboard)
    except Exception:
        pass
    

def register_messages_answered(dp: Dispatcher):
    dp.register_callback_query_handler(answered_messages_paginate_show,
                                       callback_data="answered",
                                       state=AdminStates.messages_menu)
    dp.register_callback_query_handler(back_from_answered_messages_pagination,
                                       callback_data="back",
                                       state=AdminStates.answered_messages_paginating)
    dp.register_callback_query_handler(answered_next_page,
                                       callback_data="next",
                                       state=AdminStates.answered_messages_paginating)
    dp.register_callback_query_handler(answered_prev_page,
                                       callback_data="previous",
                                       state=AdminStates.answered_messages_paginating)
    