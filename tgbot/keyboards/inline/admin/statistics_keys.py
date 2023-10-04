from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


statistics_menu = InlineKeyboardMarkup(1,
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Сообщения на темы", 
                callback_data="topics_messages"
                )
        ],
        [
            InlineKeyboardButton(
                text="Сообщения за неделю", 
                callback_data="week_messages"
                )
        ],
        [
            InlineKeyboardButton(
                text="Назад", 
                callback_data="back"
                )
        ]
    ])