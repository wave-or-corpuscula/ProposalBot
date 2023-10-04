from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


admin_menu = InlineKeyboardMarkup(
    inline_keyboard= 
    [
        [
            InlineKeyboardButton(
                text="Сообщения",
                callback_data="messages"
            )
        ],
        [
            InlineKeyboardButton(
                text="Статистика",
                callback_data="stats"
            )
        ],
        [
        
            InlineKeyboardButton(
                text="Редактировать темы",
                callback_data="edit_topics"
                )
        ],
        [
            InlineKeyboardButton(
                text="Заблокированные пользователи",
                callback_data="banned_users"
                )
        ]
    ]
)


back_button = InlineKeyboardMarkup(
        inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Назад", 
                callback_data="back"
                )
        ]
    ]
)