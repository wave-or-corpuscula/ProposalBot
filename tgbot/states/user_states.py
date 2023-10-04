from aiogram.dispatcher.filters.state import State, StatesGroup


class UserStates(StatesGroup):
    
    choose_message_type = State()
    typeing_message = State()
