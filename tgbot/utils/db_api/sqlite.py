import sqlite3

from datetime import datetime

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from . import Config


class DataBase:

    def __init__(self, config: Config):
        self.connection = sqlite3.connect(config.db.database)
        self.cursor = self.connection.cursor()

    def get_type_name(self, type_id: int):
        sql = "SELECT type_name FROM MessageTypes WHERE type_id={}".format(type_id)
        self.cursor.execute(sql)
        return self.cursor.fetchall()[0][0]
    
    def get_min_max_date(self):
        sql = "SELECT min(date), max(date) FROM UsersMessages;"
        self.cursor.execute(sql)
        return self.cursor.fetchall()[0]

    def get_week_topics_amount(self, time_start: datetime, time_end: datetime):
        sql = "SELECT \
                    type_name, \
                    count(um.type_id) \
                FROM UsersMessages um \
                JOIN MessageTypes mt ON mt.type_id = um.type_id \
                WHERE date BETWEEN ? AND ? \
                GROUP BY type_name; "
        self.cursor.execute(sql, (time_start, time_end))
        return self.cursor.fetchall()

    def get_topics_amount(self):
        sql = "SELECT \
                    type_name, \
                    count(um.type_id) \
                FROM UsersMessages um \
                JOIN MessageTypes mt ON mt.type_id = um.type_id \
                GROUP BY type_name;" 
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    def get_types(self):
        sql = "SELECT * FROM MessageTypes;"
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    def del_topic(self, topic_id: int):
        sql = "DELETE FROM MessageTypes WHERE type_id=?"
        self.cursor.execute(sql, (topic_id,))
        self.connection.commit()

    def add_topic(self, topic_name: str):
        sql = "INSERT INTO MessageTypes (type_name) VALUES (?);"
        self.cursor.execute(sql, (topic_name,))
        self.connection.commit()

    def get_types_keyboard(self):
        types = self.get_types()
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

    def add_message(self, user_id: int, username: str, message: str, type_id: int):
        sql = F"INSERT INTO UsersMessages (user_id, user_tag, message, type_id) VALUES (?, ?, ?, ?)"
        data_typle = (user_id, username, message, type_id)
        try:
            self.cursor.execute(sql, data_typle)
            self.connection.commit()
        except Exception as e:
            print(e)

    def get_types_edit_keyboard(self):
        types = self.get_types()
        buttons = []
        for topic_type in types:
            buttons.append(
                [
                    InlineKeyboardButton(text=f"{topic_type[1]} ❌",
                                         callback_data=topic_type[0])
                ]
            )
        buttons.append([InlineKeyboardButton(text="Назад", callback_data="back")])
        return InlineKeyboardMarkup(1, buttons)
