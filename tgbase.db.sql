BEGIN TRANSACTION;
INSERT INTO "Messages" ("message_id","user_id","topic_id","message","repsonse","message_date","pin_id") VALUES (41,709997550,1,'other',NULL,'2023-10-03 20:10:11',NULL),
 (52,709997550,2,'Question1',NULL,'2023-10-03 20:13:58',NULL),
 (54,709997550,2,'ddd',NULL,'2023-10-03 20:14:14',NULL),
 (58,709997550,2,'Question2',NULL,'2023-10-03 20:15:26',NULL),
 (60,709997550,3,'Proposal1',NULL,'2023-10-03 20:15:32',NULL),
 (62,709997550,1,'Other2',NULL,'2023-10-03 20:15:37',NULL);
INSERT INTO "Users" ("user_id","username","first_name","last_name","registered_date","is_banned") VALUES (709997550,'wave_or_corpuscula','Андрей','БАРАБАН','2023-10-03 19:35:25',0);
INSERT INTO "TopicTypes" ("topic_id","topic_name") VALUES (1,'Другое'),
 (2,'Вопрос');
COMMIT;
