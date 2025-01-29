import sqlite3 as sql
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, password):
        self.id = id
        self.password = password

def list_diaries():
	con = sql.connect(".databaseFiles/database.db")
	cur = con.cursor()
	data = cur.execute('SELECT * FROM diaries').fetchall()
	con.close()
	return data

def insert_diaries(developer, 
                   project,
                   start_time,
                   end_time,
                   repo_url,
                   dev_note,
                   code_snippet,
                   language):
    con = sql.connect(".databaseFiles/database.db")
    cur = con.cursor()
    cur.execute('''
            INSERT INTO diaries (developer, project, start_time, end_time, repo_url, dev_note, code_snippet, language)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (developer, project, start_time, end_time, repo_url, dev_note, code_snippet, language))
    cur.execute("UPDATE diaries SET time_worked = ROUND((strftime('%s', end_time) - strftime('%s', start_time)) / 60.0 / 15);")
    cur.execute("UPDATE diaries SET time_worked = printf('%d:%02d', (time_worked * 15) / 60, (time_worked * 15) % 60);")
    con.commit()
    con.close()

def insert_users(email, password):
    con = sql.connect(".databaseFiles/database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO users (email, password) VALUES (?,?)", (email, password))
    con.commit()
    con.close()
    

def get_users(email):
    con = sql.connect(".databaseFiles/database.db")
    cur = con.cursor()
    user_data = cur.execute("SELECT id, email, password FROM users WHERE email = ?", (email,)).fetchone()
    con.close()
    if user_data:
        user_id, email, hashed_password = user_data
        return User(user_id, hashed_password)
    return None

def get_user_by_id(user_id):
    con = sql.connect(".databaseFiles/database.db")
    cur = con.cursor()
    user_data = cur.execute("SELECT id, email, password FROM users WHERE id = ?", (user_id,)).fetchone()
    con.close()
    if user_data:
        user_id, email, hashed_password = user_data
        return User(user_id, hashed_password)
    return None
