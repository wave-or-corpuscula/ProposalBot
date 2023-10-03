from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


admin_menu = InlineKeyboardMarkup(
    inline_keyboard= 
    [
        [
            InlineKeyboardButton(
                text="Редактировать темы",
                callback_data="edit_topics"
                )
        ],
        [
            InlineKeyboardButton(
                text="Статистика",
                callback_data="stats"
        )
        ],
        # [
        #     InlineKeyboardButton(
        #         text="Закрыть меню",
        #         callback_data="close_menu"
        #     )
        # ]
    ]
)
types_edit_menu = InlineKeyboardMarkup(
    inline_keyboard= 
    [
        [
            InlineKeyboardButton(
                text="Добавить тему",
                callback_data="add_topic"
                )
        ],
        [
            InlineKeyboardButton(
                text="Удалить тему",
                callback_data="del_topic"
            )
        ],
        [
            InlineKeyboardButton(
                text="Назад",
                callback_data="back"
            )
        ]
    ]
)

back_button = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Назад", callback_data="back")
                    ]
                ]
)

stat_menu = InlineKeyboardMarkup(1,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Сообщения на темы", 
                                 callback_data="topics_messages")
        ],
        [
            InlineKeyboardButton(text="Сообщения за неделю", 
                                 callback_data="week_messages")
        ],
        [
            InlineKeyboardButton(text="Назад", 
                                 callback_data="back")
        ]
    ])