CREATE TABLE IF NOT EXISTS  "TopicTypes" (
	"topic_id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"topic_name"	TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS "PinTypes" (
	"pin_id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"pin_name"	VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS "Users" (
	"user_id"	INTEGER NOT NULL UNIQUE,
	"username"	VARCHAR(255),
	"first_name"	VARCHAR(255),
	"last_name"	VARCHAR(255),
	"registered_date"	DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"is_banned"	BOOLEAN NOT NULL DEFAULT 0,
	PRIMARY KEY("user_id")
);

CREATE TABLE IF NOT EXISTS "Messages" (
	"chat_id"	INTEGER,
	"message_id"	INTEGER NOT NULL,
	"user_id"	INTEGER,
	"topic_id"	INTEGER NOT NULL,
	"message"	TEXT NOT NULL,
	"repsonse"	TEXT DEFAULT NULL,
	"message_date"	DATETIME DEFAULT CURRENT_TIMESTAMP,
	"pin_id"	INTEGER,
	FOREIGN KEY("topic_id") REFERENCES "TopicTypes"("topic_id") ON DELETE NO ACTION,
	FOREIGN KEY("user_id") REFERENCES "Users"("user_id") ON DELETE SET NULL,
	PRIMARY KEY("message_id","chat_id"),
	FOREIGN KEY("pin_id") REFERENCES "PinTypes"("pin_id") ON DELETE NO ACTION
);