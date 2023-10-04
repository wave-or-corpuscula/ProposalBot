import logging

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from tgbot.states.admin_states import AdminStates
from tgbot.keyboards.inline.admin import messages_menu, admin_menu, back_button
from tgbot.utils.messages_paginator.messages_paginator import MessagesPaginator


async def show_message_menu(call: types.CallbackQuery):
    await AdminStates.messages_menu.set()
    await call.message.edit_text("Выберите подходящий пункт:", reply_markup=messages_menu)


async def back_to_admin_menu(call: types.CallbackQuery):
    await AdminStates.admin_main_menu.set()
    await call.message.edit_text("Выберите действие:", reply_markup=admin_menu)
    

async def show_unanswered_messages(call: types.CallbackQuery):
    keyboard = call.message.bot.kcreator.get_unanswered_messages_topics_keyboard()
    await AdminStates.unanswered_messages_show.set()
    await call.message.edit_text("Выберите тему:", reply_markup=keyboard)


async def back_from_unanswered_messages(call: types.CallbackQuery):
    await show_message_menu(call)


# Messages pagination

async def topic_messages_paginate_show(call: types.CallbackQuery, state: FSMContext):
    topic_id = call.data
    messages = call.message.bot.db.get_unanswered_messages(topic_id)
    paginator = MessagesPaginator(messages, with_answer=False)
    keyboard, message = paginator.get_page()

    await state.update_data(paginator=paginator, topic_id=topic_id)
    await AdminStates.topic_messages_paginating.set()
    await call.message.edit_text(message, reply_markup=keyboard)


async def back_from_messages_pagination(call: types.CallbackQuery, state: FSMContext):
    await state.reset_data()
    await show_unanswered_messages(call)


async def next_page(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    paginator: MessagesPaginator = data["paginator"]
    try:
        keyboard, message = paginator.next_page()
        await state.update_data(paginator=paginator)
        await call.message.edit_text(message, reply_markup=keyboard)
    except Exception:
        pass


async def prev_page(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    paginator: MessagesPaginator = data["paginator"]
    try:
        keyboard, message = paginator.prev_page()
        await state.update_data(paginator=paginator)
        await call.message.edit_text(message, reply_markup=keyboard)
    except Exception:
        pass

# Answer message        

async def answer_message(call: types.CallbackQuery, state: FSMContext):
    await AdminStates.answer_message_typing.set()
    await call.message.edit_text("Введите ответ для пользователя:", 
                                 reply_markup=back_button)


async def cancel_answer_message(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    paginator: MessagesPaginator = data["paginator"]
    keyboard, message = paginator.get_page()

    await AdminStates.topic_messages_paginating.set()
    await state.update_data(paginator=paginator)
    await call.message.edit_text(message, reply_markup=keyboard)


async def send_answer_message(message: types.Message, state: FSMContext):
    await AdminStates.topic_messages_paginating.set()
    data = data = await state.get_data()
    paginator: MessagesPaginator = data["paginator"]
    user_message = paginator.get_cur_message()
    answer = [
        f"Ваше сообщение на тему: <i>{user_message['topic_name']}</i>\n",
        user_message["message"],
        f"Ответ администрации:\n",
        f"<i>{message.text}</i>"
    ]
    message.bot.db.response_message(user_message["message_id"], user_message["user_id"], message.text)
    await state.update_data(paginator=paginator)
    try:
        paginator.del_cur_message()
        keyboard, page_message = paginator.get_page()
        await message.bot.send_message(user_message["user_id"], "\n".join(answer))
        await message.answer("<b>Ответ успешно отправлен!</b>\n" + page_message, reply_markup=keyboard)
    except Exception:
        keyboard = message.bot.kcreator.get_unanswered_messages_topics_keyboard()
        await AdminStates.unanswered_messages_show.set()
        await state.reset_data()
        await message.answer("Выберите тему:", reply_markup=keyboard)

# Delete message

async def delete_message(call: types.CallbackQuery, state: FSMContext):
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
        keyboard = call.message.bot.kcreator.get_unanswered_messages_topics_keyboard()
        await AdminStates.unanswered_messages_show.set()
        await call.message.answer("Выберите тему:", reply_markup=keyboard)

# Pin/Unpin message

async def pin_message(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    paginator: MessagesPaginator = data["paginator"]
    user_message = paginator.get_cur_message()
    if not user_message["pin_id"]:
        call.message.bot.db.pin_message(user_message["message_id"], user_message["user_id"])
    else:
        call.message.bot.db.unpin_message(user_message["message_id"], user_message["user_id"])
    paginator.change_message_pin()
    await state.update_data(paginator=paginator)
    keyboard, message = paginator.get_page()
    await call.message.edit_text(message, reply_markup=keyboard)

# Ban user

async def ban_user(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    paginator: MessagesPaginator = data["paginator"]
    user_message = paginator.get_cur_message()




def register_messages(dp: Dispatcher):
    dp.register_callback_query_handler(show_message_menu, 
                                       callback_data="messages",
                                       state=AdminStates.admin_main_menu)
    dp.register_callback_query_handler(back_to_admin_menu, 
                                       callback_data="back",
                                       state=AdminStates.messages_menu)
    dp.register_callback_query_handler(show_unanswered_messages, 
                                       callback_data="wait_for_answer",
                                       state=AdminStates.messages_menu)
    dp.register_callback_query_handler(back_from_unanswered_messages, 
                                       callback_data="back",
                                       state=AdminStates.unanswered_messages_show)
    dp.register_callback_query_handler(topic_messages_paginate_show, 
                                       state=AdminStates.unanswered_messages_show)
    # Messages pagination
    dp.register_callback_query_handler(back_from_messages_pagination,
                                       callback_data="back",
                                       state=AdminStates.topic_messages_paginating)
    dp.register_callback_query_handler(next_page,
                                       callback_data="next",
                                       state=AdminStates.topic_messages_paginating)
    dp.register_callback_query_handler(prev_page,
                                       callback_data="previous",
                                       state=AdminStates.topic_messages_paginating)
    # Answer message
    dp.register_callback_query_handler(answer_message,
                                       callback_data="answer",
                                       state=AdminStates.topic_messages_paginating)
    dp.register_callback_query_handler(cancel_answer_message,
                                       callback_data="back",
                                       state=AdminStates.answer_message_typing)
    dp.register_message_handler(send_answer_message,
                                state=AdminStates.answer_message_typing)
    # Delete message
    dp.register_callback_query_handler(delete_message,
                                       callback_data="delete",
                                       state=AdminStates.topic_messages_paginating)
    # Pin message
    dp.register_callback_query_handler(pin_message,
                                       callback_data="star",
                                       state=AdminStates.topic_messages_paginating)
