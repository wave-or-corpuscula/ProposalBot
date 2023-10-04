from aiogram.dispatcher.filters.state import State, StatesGroup


class AdminStates(StatesGroup):

    admin_main_menu = State()

    # Topic manipulation
    topic_changing_menu = State()
    waiting_for_new_topic_name = State()
    del_topic = State()

    # Statistics
    statistic_menu = State()
    topics_amount_view = State()
    week_topics_view = State()