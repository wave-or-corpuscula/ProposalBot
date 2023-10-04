import logging

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from tgbot.states.admin_states import AdminStates
from tgbot.keyboards.inline.admin import messages_menu, admin_menu
from tgbot.handlers.admin.messages import show_unanswered_messages






def register_messages_pagination(dp: Dispatcher):
    pass