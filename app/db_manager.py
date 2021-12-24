from tinydb import TinyDB, Query
from tinydb.operations import increment, set
db = TinyDB('chats_db.json')

User = Query()


def insert_user(chat, date):
    print("INSERT USER::", chat, date)
    if chat.type == 'private':
        db.insert({'id': chat.id, 'userType': chat.type,
                  'username': chat.username, 'name': chat.first_name, 'date_activity': date, 'action_count': 1})
    elif chat.type == 'supergroup':
        db.insert({'id': chat.id, 'userType': chat.type,
                  'username': chat.username, 'name': chat.title, 'date_activity': date, 'action_count': 1})
    else:
        db.insert({'userType:': 'unknown', 'id': chat.id,
                  'data': chat, 'date_activity': date, 'action_count': 1})


def log_activity(userId, date):
    print("Log Activtiy::", userId, date)
    db.update(set('date_activity', date), User.id == userId)
    db.update(increment('action_count'), User.id == userId)


def log_user(chat, date):
    print("log_user::", chat.id, date)
    if db.search(User.id == chat.id):
        print("IF::", chat.id, date)
        log_activity(chat.id, date)
    else:
        print("ELSE ::", chat.id, date)
        insert_user(chat, date)
