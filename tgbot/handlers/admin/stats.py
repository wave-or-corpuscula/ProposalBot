import logging

from datetime import timedelta, datetime

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from tgbot.states.admin_states import AdminStates
from tgbot.keyboards.inline.admin import admin_menu, statistics_menu, back_button


async def get_stats(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Выберите пункт для отображения:", reply_markup=statistics_menu)
    await state.set_state(AdminStates.statistic_menu)


async def get_topics_amount(call: types.CallbackQuery, state: FSMContext):
    topics_amount = call.message.bot.db.get_topics_amount()
    min_max_date = call.message.bot.db.get_min_max_date()
    answer = [f"<b>Сообщения в период с {min_max_date[0]} по {min_max_date[1]}:</b>"]
    for topic in topics_amount:
        answer.append(f"<i>{topic[0]}</i>: {topic[1]}")
    await state.set_state(AdminStates.topics_amount_view)
    await call.message.edit_text("\n".join(answer), reply_markup=back_button)


async def back_from_topics_amount(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Выберите пункт для отображения:", reply_markup=statistics_menu)
    await state.set_state(AdminStates.statistic_menu)


async def get_week_topics(call: types.CallbackQuery, state: FSMContext):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    topics_amount = call.message.bot.db.get_week_topics_amount(start_date, end_date)
    answer = [f"<b>Сообщения за 7 дней:</b>"]
    for topic in topics_amount:
        answer.append(f"<i>{topic[0]}</i>: {topic[1]}")
    await state.set_state(AdminStates.week_topics_view)
    await call.message.edit_text("\n".join(answer), reply_markup=back_button)


async def back_from_week_topics(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Выберите пункт для отображения:", reply_markup=statistics_menu)
    await state.set_state(AdminStates.statistic_menu)


async def back_to_main_menu(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Выберите действие:", reply_markup=admin_menu)
    await state.set_state(AdminStates.admin_main_menu)


def register_stats(dp: Dispatcher):
    dp.register_callback_query_handler(get_stats, callback_data="stats", state=AdminStates.admin_main_menu)
    dp.register_callback_query_handler(get_topics_amount, callback_data="topics_messages", state=AdminStates.statistic_menu)
    dp.register_callback_query_handler(back_from_topics_amount, callback_data="back", state=AdminStates.topics_amount_view)
    dp.register_callback_query_handler(get_week_topics, callback_data="week_messages", state=AdminStates.statistic_menu)
    dp.register_callback_query_handler(back_from_week_topics, callback_data="back", state=AdminStates.week_topics_view)
    dp.register_callback_query_handler(back_to_main_menu, callback_data="back", state=AdminStates.statistic_menu)