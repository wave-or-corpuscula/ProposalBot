CREATE TABLE "TopicTypes" (
	"topic_id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"topic_name"	TEXT NOT NULL
);

CREATE TABLE "PinTypes" (
	"pin_id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"pin_name"	VARCHAR(255) NOT NULL
);

CREATE TABLE "Users" (
	"user_id"	INTEGER NOT NULL UNIQUE,
	"username"	VARCHAR(255),
	"first_name"	VARCHAR(255),
	"last_name"	VARCHAR(255),
	"registered_date"	DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"is_banned"	BOOLEAN NOT NULL DEFAULT 0,
	PRIMARY KEY("user_id")
);

CREATE TABLE "Messages" (
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
