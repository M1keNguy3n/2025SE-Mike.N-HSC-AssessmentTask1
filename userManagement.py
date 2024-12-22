import sqlite3 as sql
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, password):
        self.id = id
        self.password = password

def list_diaries_collapsed():
	con = sql.connect(".databaseFiles/database.db")
	cur = con.cursor()
	data = cur.execute('SELECT developer, project, StartTime, Endtime FROM diaries').fetchall()
	con.close()
	return data

def insert_diaries(developer, 
                   project,
                   StartTime,
                   EndTime,
                   RepoURL,
                   DevNote,
                   CodeSnippet):
    con = sql.connect(".database/database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO diaries (developer, project, StartTime, EndTime, RepoURL, DevNote, CodeSnippet) VALUES (?,?,?,?,?,?,?)", (developer, project, StartTime, EndTime, RepoURL, DevNote, CodeSnippet))
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
