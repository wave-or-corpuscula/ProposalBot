import logging

import sqlite3

from datetime import datetime

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from . import Config


class DataBase:

    def __init__(self, config: Config):
        self.connection = sqlite3.connect(config.db.database)
        self.cursor = self.connection.cursor()

    def get_type_name(self, topic_id: int):
        sql = "SELECT topic_name FROM TopicTypes WHERE topic_id={}".format(topic_id)
        self.cursor.execute(sql)
        return self.cursor.fetchall()[0][0]
    
    def add_user(self, user_id: int, username, first_name, last_name):
        sql = """INSERT INTO Users (user_id, username, first_name, last_name) 
        VALUES (?, ?, ?, ?) """
        try:
            self.cursor.execute(sql, (user_id, username, first_name, last_name, ))
            self.connection.commit()
        except sqlite3.IntegrityError as e:
            logging.warning(f"Error while adding user {user_id}: {e}")

    def add_message(self, message_id: int, user_id: int, topic_id: int, message: str):
        sql = """INSERT INTO Messages (message_id, user_id, topic_id, message) 
        VALUES (?, ?, ?, ?)"""
        data_typle = (message_id, user_id, topic_id, message)
        try:
            self.cursor.execute(sql, data_typle)
            self.connection.commit()
        except Exception as e:
            print(e)
    
    def create_tables(self):
        tables_sql = ["""
                CREATE TABLE IF NOT EXISTS  "TopicTypes" (
                    "topic_id"	INTEGER PRIMARY KEY AUTOINCREMENT,
                    "topic_name"	TEXT NOT NULL
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS "PinTypes" (
                    "pin_id"	INTEGER PRIMARY KEY AUTOINCREMENT,
                    "pin_name"	VARCHAR(255) NOT NULL
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS "Users" (
                    "user_id"	INTEGER NOT NULL UNIQUE,
                    "username"	VARCHAR(255),
                    "first_name"	VARCHAR(255),
                    "last_name"	VARCHAR(255),
                    "registered_date"	DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    "is_banned"	BOOLEAN NOT NULL DEFAULT 0,
                    PRIMARY KEY("user_id")
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS "Messages" (
                    "message_id"	INTEGER NOT NULL UNIQUE,
                    "user_id"	INTEGER,
                    "topic_id"	INTEGER NOT NULL,
                    "message"	TEXT NOT NULL,
                    "repsonse"	TEXT,
                    "message_date"	DATETIME DEFAULT CURRENT_TIMESTAMP,
                    "pin_id"	INTEGER,
                    FOREIGN KEY("pin_id") REFERENCES "PinTypes"("pin_id") ON DELETE NO ACTION,
                    PRIMARY KEY("message_id"),
                    FOREIGN KEY("user_id") REFERENCES "Users"("user_id") ON DELETE SET NULL,
                    FOREIGN KEY("topic_id") REFERENCES "TopicTypes"("topic_id") ON DELETE NO ACTION
                );
                """]
        for sql in tables_sql: self.cursor.execute(sql)
        self.connection.commit()
        print("tables created")

    
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
        sql = "SELECT * FROM TopicTypes;"
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
