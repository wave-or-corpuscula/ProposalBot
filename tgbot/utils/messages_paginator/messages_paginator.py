from aiogram import types
from aiogram.types import (InlineKeyboardButton,
                           InlineKeyboardMarkup)


class MessagesPaginator():

    def __init__(self, 
                 messages: list, 
                 have_answer_but: bool = True,
                 have_star_but: bool = True,
                 have_delete_but: bool = True):
        if len(messages) == 0:
            raise Exception
        self.messages = messages
        self.current_page = 0
        self.messages_amount = len(messages)

        answer_but = InlineKeyboardButton(text="✉️", callback_data="answer")
        star_but = InlineKeyboardButton(text="⭐️", callback_data="star")
        delete_but = InlineKeyboardButton(text="❌", callback_data="delete")
        ban_but = InlineKeyboardButton(text="🚫", callback_data="ban")

        self.add_keyboard = []
        if have_answer_but:
            self.add_keyboard.append(answer_but)
        if have_star_but:
            self.add_keyboard.append(star_but)
        if have_delete_but: 
            self.add_keyboard.append(delete_but)

    def get_page(self):
        cur_mes = self.messages[self.current_page]

        next_but = InlineKeyboardButton(text="→", callback_data="next")
        prev_but = InlineKeyboardButton(text="←", callback_data="previous")
        current_position_but = InlineKeyboardButton(text=f"{self.current_page + 1}/{self.messages_amount}", callback_data="cur_pos")

        back_but = InlineKeyboardButton(text="Назад", callback_data="back")
        
        keys = [[prev_but, current_position_but, next_but], [back_but]]
        if len(self.add_keyboard) != 0:
            keys.insert(1, self.add_keyboard)

        keyboard = InlineKeyboardMarkup(3, keys)

        pin = " ⭐️" if cur_mes["pin_id"] else ""
        message = [
            f"Сообщения на тему: <i>{cur_mes['topic_name']}</i>{pin}\n",
            cur_mes["message"]
        ]
        if cur_mes["response"]:
            message.append(
                [
                    "<i>nОтвет:</i>\n",
                    cur_mes["response"]
                ]
            )

        return keyboard, "\n".join(message)
    
    def next_page(self):
        if self.messages_amount == 1:
            raise Exception
        self.current_page += 1
        if self.current_page == self.messages_amount:
            self.current_page = 0
        return self.get_page()
    
    def prev_page(self):
        if self.messages_amount == 1:
            raise Exception
        self.current_page -= 1
        if self.current_page == -1:
            self.current_page = self.messages_amount - 1
        return self.get_page()

    def get_cur_message_identifiers(self):
        cur_mes = self.messages[self.current_page]
        return {"message_id": cur_mes["message_id"], "user_id": cur_mes["user_id"]}
    
    def get_cur_message(self):
        cur_mes= self.messages[self.current_page]
        return cur_mes

    def del_cur_message(self):
        self.messages.pop(self.current_page)
        self.current_page = self.current_page - 1 if self.current_page - 1 > 0 else 0
        self.messages_amount -= 1
        if self.messages_amount == 0:
            raise Exception
        
    def change_message_pin(self):
        cur_mes = self.messages[self.current_page]
        cur_mes["pin_id"] = not cur_mes["pin_id"]

    def pin_cur_message(self):
        cur_mes = self.messages[self.current_page]
        cur_mes["pin_id"] = 1

    def unpin_cur_message(self):
        cur_mes = self.messages[self.current_page]
        cur_mes["pin_id"] = 0

