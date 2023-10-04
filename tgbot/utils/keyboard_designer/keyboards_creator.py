from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tgbot.utils.db_api.sqlite import DataBase


class KeyboardsCreator():

    def __init__(self, db: DataBase):
        self.db = db

    def get_types_keyboard(self):
        types = self.db.get_types()
        types_triple = []
        row_count = 3
        index = 0
        go_on = True
        while go_on:
            triplet = []
            for _ in range(row_count):
                try:
                    triplet.append(InlineKeyboardButton(callback_data=types[index][0], text=types[index][1]))
                    index += 1
                except Exception:
                    go_on = False
                    break
            types_triple.append(triplet)
        return InlineKeyboardMarkup(3, inline_keyboard=types_triple)

    def get_types_edit_keyboard(self):
        types = self.db.get_types()
        buttons = []
        for topic_type in types:
            buttons.append(
                [
                    InlineKeyboardButton(
                        text=f"{topic_type[1]} ❌",
                        callback_data=topic_type[0]
                    )
                ]
            )
        buttons.append([InlineKeyboardButton(text="Назад", callback_data="back")])
        return InlineKeyboardMarkup(1, buttons)
    
    def get_unanswered_messages_topics_keyboard(self):
        topics = self.db.get_topics_unanswered_messages()
        buttons = []
        for topic in topics:
            buttons.append(
                [
                    InlineKeyboardButton(
                        text=f"{topic[0]}: {topic[1]}",
                        callback_data=topic[2]
                    )
                ]
            )
        buttons.append([InlineKeyboardButton(text="Назад", callback_data="back")])
        return InlineKeyboardMarkup(1, inline_keyboard=buttons)
    
    def form_topics_paginate_keyboard(self, amount: int, current_page: int):
        next_but = InlineKeyboardButton(text="→", callback_data="next")
        prev_but = InlineKeyboardButton(text="←", callback_data="previous")
        current_position_but = InlineKeyboardButton(text=f"{current_page}/{amount}", callback_data="cur_pos")

        answer_but = InlineKeyboardButton(text="✉️", callback_data="answer")
        star_but = InlineKeyboardButton(text="⭐️", callback_data="star")
        delete_but = InlineKeyboardButton(text="❌", callback_data="delete")
        ban_but = InlineKeyboardButton(text="🚫", callback_data="ban")

        back_but = InlineKeyboardButton(text="Назад", callback_data="back")

        return InlineKeyboardMarkup(3, [[prev_but, current_position_but, next_but], [answer_but, star_but, delete_but, ban_but], [back_but]])
