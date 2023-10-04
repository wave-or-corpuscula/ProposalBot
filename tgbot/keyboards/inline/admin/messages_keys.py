from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


messages_menu = InlineKeyboardMarkup(1,
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Ожидают ответа",
                callback_data="wait_for_answer"
            )
        ],
        [
            InlineKeyboardButton(
                text="Сохраненные",
                callback_data="saved"
            )
        ],
        [
            InlineKeyboardButton(
                text="Мои ответы",
                callback_data="answered"
            )
        ],
        [
            InlineKeyboardButton(
                text="Назад",
                callback_data="back"
            )
        ],
    ]
)