from aiogram.dispatcher.filters.state import State, StatesGroup


class AdminStates(StatesGroup):

    admin_main_menu = State()

    # Topic manipulation
    del_topic = State()
    topic_changing_menu = State()
    waiting_for_new_topic_name = State()

    # Statistics
    statistic_menu = State()
    week_topics_view = State()
    topics_amount_view = State()

    # Messages
    messages_menu = State()
    answer_message_typing = State()
    unanswered_messages_show = State()
    unanswered_messages_paginating = State()

    # Pinned
    pinned_messages_paginating = State()

    # Answered
    answered_messages_paginating = State()
