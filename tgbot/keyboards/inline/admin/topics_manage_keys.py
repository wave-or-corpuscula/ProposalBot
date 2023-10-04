from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


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