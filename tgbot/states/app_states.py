from aiogram.dispatcher.filters.state import State, StatesGroup


class AppStates(StatesGroup):
    
    # User states
    
    menu_choosing = State()
    choose_message_type = State()
    typeing_message = State()

    # Admin states

    admin_main_menu = State()

    # Topic manipulation
    topic_changing_menu = State()
    add_topic = State()
    del_topic = State()
    waiting_for_new_topic = State()

    # Statistics
    states_menu = State()
    topics_amount_view = State()
    week_topics_view = State()
