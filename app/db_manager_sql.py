import sqlite3
sqliteConnection = sqlite3.connect('user_logs.db')

cur = sqliteConnection.cursor()
cur.execute(
    '''CREATE TABLE IF NOT EXISTS users (id integer primary key autoincrement, chat_id INTEGER, usertype TEXT, username TEXT, name TEXT, actioncount INT, datecreated datetime )''')
cur.execute(
    '''CREATE TABLE IF NOT EXISTS user_trans_log (id integer primary key autoincrement, userid INTEGER, message TEXT, datecreated datetime)''')


def insert_user(chat, text, date):
    print("[insert_user]-", chat)
    try:
        sqliteConnection = sqlite3.connect('user_logs.db')
        cur = sqliteConnection.cursor()
        if chat.type == 'private':
            cur.execute(
                f"INSERT INTO users (chat_id,usertype,username,name,actioncount,datecreated) VALUES ({chat.id}, '{chat.type}', '{chat.username}', '{chat.first_name}', 1, {date})")
        elif chat.type == 'supergroup':
            cur.execute(
                f"INSERT INTO users (chat_id,usertype,username,name,actioncount,datecreated) VALUES ({chat.id}, '{chat.type}', '{chat.username}', '{chat.title}', 1, {date})")
        else:
            cur.execute(
                f'INSERT INTO users (chat_id,usertype,username,name,actioncount,datecreated) VALUES ({chat.id}, null, null, null, 1, {date})')
        cur.execute(
            f"INSERT INTO user_trans_log (userid, message, datecreated) VALUES ({chat.id},'{text}',{date})")
        sqliteConnection.commit()
        sqliteConnection.close()
    except sqlite3.Error as error:
        print("[insert_user]-Failed to update sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("[insert_user]-The sqlite connection is closed")


def log_activity(id, text, date):
    try:
        sqliteConnection = sqlite3.connect('user_logs.db')
        cur = sqliteConnection.cursor()
        print("[log_activity]-Connected to SQLite")
        cur.execute(
            f"INSERT INTO user_trans_log (userid, message, datecreated) VALUES ({id},'{text}',{date})")
        cur.execute(
            f'UPDATE users SET actioncount = actioncount + 1 where id in ({id})')
        print("Record Updated successfully")
        sqliteConnection.commit()
        sqliteConnection.close()
    except sqlite3.Error as error:
        print("[log_activity]-Failed to update sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("[log_activity]-The sqlite connection is closed")


def log_user(chat, text, date):
    print("log_user::", chat.id, text, date)
    try:
        sqliteConnection = sqlite3.connect('user_logs.db')
        cur = sqliteConnection.cursor()
        print("[log_user]-Connected to SQLite")
        cur.execute('SELECT * FROM users WHERE chat_id=?', (chat.id,))
        row = cur.fetchone()
        print("RPW", row)
        if row is None:
            insert_user(chat, text, date)
        else:
            log_activity(chat.id, text, date)
    except sqlite3.Error as error:
        print("[log_user]-Failed to update sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("[log_user]-The sqlite connection is closed")
