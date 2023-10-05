import logging
logger = logging.getLogger(__name__)

import sqlite3

from datetime import datetime

from . import Config


class DataBase:

    def __init__(self, config: Config):
        self.connection = sqlite3.connect(config.db.database)
        self.cursor = self.connection.cursor()

    def get_topic_name(self, topic_id: int):
        sql = "SELECT topic_name FROM TopicTypes WHERE topic_id=?;"
        self.cursor.execute(sql, (topic_id,))
        return self.cursor.fetchall()[0][0]
    
    def add_user(self, user_id: int, username, first_name, last_name):
        sql = """INSERT INTO Users (user_id, username, first_name, last_name) 
        VALUES (?, ?, ?, ?) """
        try:
            self.cursor.execute(sql, (user_id, username, first_name, last_name, ))
            self.connection.commit()
        except sqlite3.IntegrityError as e:
            logger.debug(f"Error while adding user {user_id}: {e}")

    def ban_user(self, user_id: int):
        sql = """UPDATE Users SET is_banned=1, ban_time=? WHERE user_id=?;"""
        self.cursor.execute(sql, (datetime.now(), user_id,))
        self.connection.commit()

    def unban_user(self, user_id: int):
        sql = """UPDATE Users SET is_banned=0 WHERE user_id=?;"""
        self.cursor.execute(sql, (user_id,))
        self.connection.commit()

    def add_message(self, message_id: int, user_id: int, topic_id: int, message: str):
        sql = """INSERT INTO Messages (message_id, user_id, topic_id, message) 
        VALUES (?, ?, ?, ?)"""
        try:
            self.cursor.execute(sql, (message_id, user_id, topic_id, message,))
            self.connection.commit()
        except Exception as e:
            print(e)

    def del_message(self, message_id: int, user_id: int):
        sql = """DELETE FROM Messages WHERE message_id=? AND user_id=?;"""
        self.cursor.execute(sql, (message_id, user_id,))
        self.connection.commit()
    
    def response_message(self, message_id: int, user_id: int, response: str):
        sql = """UPDATE Messages SET response=? WHERE user_id=? AND message_id=?;"""
        self.cursor.execute(sql, (response, user_id, message_id,))
        self.connection.commit()

    def pin_message(self, message_id: int, user_id: int):
        sql = """UPDATE Messages SET pin_id=1 WHERE user_id=? AND message_id=?;"""
        self.cursor.execute(sql, (user_id, message_id,))
        self.connection.commit()

    def unpin_message(self, message_id: int, user_id: int):
        sql = """UPDATE Messages SET pin_id=0 WHERE user_id=? AND message_id=?;"""
        self.cursor.execute(sql, (user_id, message_id,))
        self.connection.commit()

    def get_types(self):
        sql = "SELECT * FROM TopicTypes;"
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    def del_topic(self, topic_id: int):
        sql = "DELETE FROM TopicTypes WHERE topic_id=?"
        self.cursor.execute(sql, (topic_id,))
        self.connection.commit()

    def add_topic(self, topic_name: str):
        sql = "INSERT INTO TopicTypes (topic_name) VALUES (?);"
        self.cursor.execute(sql, (topic_name,))
        self.connection.commit()
    
    def get_min_max_date(self):
        sql = "SELECT min(message_date), max(message_date) FROM Messages;"
        self.cursor.execute(sql)
        return self.cursor.fetchall()[0]

    def get_week_topics_amount(self, time_start: datetime, time_end: datetime):
        sql = "SELECT \
                    topic_name, \
                    count(m.topic_id) \
                FROM Messages m \
                JOIN TopicTypes tt ON tt.topic_id = m.topic_id \
                WHERE message_date BETWEEN ? AND ? \
                GROUP BY topic_name; "
        self.cursor.execute(sql, (time_start, time_end))
        return self.cursor.fetchall()

    def get_topics_amount(self):
        sql = "SELECT \
                    topic_name, \
                    count(m.topic_id) \
                FROM Messages m \
                JOIN TopicTypes tt ON tt.topic_id = m.topic_id \
                GROUP BY topic_name;" 
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    def get_types(self):
        sql = "SELECT * FROM TopicTypes;"
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    def del_topic(self, topic_id: int):
        sql = "DELETE FROM TopicTypes WHERE topic_id=?"
        self.cursor.execute(sql, (topic_id,))
        self.connection.commit()

    def add_topic(self, topic_name: str):
        sql = "INSERT INTO TopicTypes (topic_name) VALUES (?);"
        self.cursor.execute(sql, (topic_name,))
        self.connection.commit()

    @staticmethod
    def form_message_dict(query_result: list):
        messages = []
        for mes in query_result:
            messages.append(
                {
                    "topic_name": mes[0],
                    "message": mes[1],
                    "response": mes[2],
                    "user_id": mes[3],
                    "message_id": mes[4],
                    "message_date": mes[5],
                    "pin_id": mes[6]
                }
            )
        return messages

    def get_topics_unanswered_messages(self):
        sql = """
            SELECT 
                topic_name,
                count(m.topic_id),
                m.topic_id
            FROM Messages m 
            JOIN TopicTypes tt ON tt.topic_id = m.topic_id
            WHERE m.response IS NULL
            GROUP BY topic_name, m.topic_id
            ORDER BY m.topic_id;
            """
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    def get_topics_pinned_messages(self):
        sql = """
            SELECT 
                topic_name,
                count(m.topic_id),
                m.topic_id
            FROM Messages m 
            JOIN TopicTypes tt ON tt.topic_id = m.topic_id
            WHERE m.pin_id
            GROUP BY topic_name, m.topic_id
            ORDER BY m.topic_id;
            """
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    def get_pinned_messages(self):
        sql = """
            SELECT 
                topic_name,
                message,
                response,
                m.user_id,
                m.message_id,
                m.message_date,
                m.pin_id
            FROM Messages m
            JOIN TopicTypes tt ON tt.topic_id = m.topic_id
            WHERE m.pin_id;
            """
        self.cursor.execute(sql)
        return DataBase.form_message_dict(self.cursor.fetchall())
    
    def get_unanswered_messages(self, topic_id: int):
        sql = """
            SELECT 
                topic_name,
                message,
                response,
                m.user_id,
                m.message_id,
                m.message_date,
                m.pin_id
            FROM Messages m
            JOIN TopicTypes tt ON tt.topic_id = m.topic_id
            WHERE m.topic_id=? AND m.response IS NULL;
            """
        self.cursor.execute(sql, (topic_id,))
        return DataBase.form_message_dict(self.cursor.fetchall())
    
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
                    "chat_id"	INTEGER,
                    "message_id"	INTEGER NOT NULL,
                    "user_id"	INTEGER,
                    "topic_id"	INTEGER NOT NULL,
                    "message"	TEXT NOT NULL,
                    "response"	TEXT DEFAULT NULL,
                    "message_date"	DATETIME DEFAULT CURRENT_TIMESTAMP,
                    "pin_id"	INTEGER,
                    FOREIGN KEY("topic_id") REFERENCES "TopicTypes"("topic_id") ON DELETE NO ACTION,
                    FOREIGN KEY("user_id") REFERENCES "Users"("user_id") ON DELETE SET NULL,
                    PRIMARY KEY("message_id","chat_id"),
                    FOREIGN KEY("pin_id") REFERENCES "PinTypes"("pin_id") ON DELETE NO ACTION
                );
                """]
        for sql in tables_sql: self.cursor.execute(sql)
        self.connection.commit()
        print("tables created")
