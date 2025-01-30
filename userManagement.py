import sqlite3 as sql
from flask_login import UserMixin
from jsonschema import validate
from flask import current_app
import pyotp

class User(UserMixin):
    def __init__(self, id, password, otp_secret):
        self.id = id
        self.password = password
        self.otp_secret = otp_secret
    def get_totp_uri(self):
        return f"otpauth://totp/Diary:{self.id}?secret={self.otp_secret}&issuer=Diary"
    def verify_totp(self, token):
        totp = pyotp.TOTP(self.otp_secret)
        return totp.verify(token)
    

def list_diaries():
	con = sql.connect(".databaseFiles/database.db")
	cur = con.cursor()
	data = cur.execute('SELECT * FROM diaries').fetchall()
	con.close()
	return data

def get_diaries_by_column(column_name, value):
    con = sql.connect(".databaseFiles/database.db")
    cur = con.cursor()
    query = f'SELECT * FROM diaries WHERE {column_name} = ?'
    data = cur.execute(query, (value,)).fetchall()
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
    otp_secret = pyotp.random_base32()
    con = sql.connect(".databaseFiles/database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO users (email, password) VALUES (?,?,?)", (email, password, otp_secret))
    con.commit()
    con.close()
    

def get_users(email):
    con = sql.connect(".databaseFiles/database.db")
    cur = con.cursor()
    user = cur.execute("SELECT id, email, password, otp_secret FROM users WHERE email = ?", (email,)).fetchone()
    con.close()
    if user:
        return {"id": user[0], "email": user[1], "password": user[2], "otp_secret": user[3]}
    return None

def get_user_by_id(user_id):
    con = sql.connect(".databaseFiles/database.db")
    cur = con.cursor()
    user = cur.execute("SELECT id, email, password, otp_secret FROM users WHERE id = ?", (user_id,)).fetchone()
    con.close()
    if user:
        return {"id": user[0], "email": user[1], "password": user[2], "otp_secret": user[3]}
    return None


def insert_diaries_api(data):
    if validate_json(data):
        con = sql.connect(".databaseFiles/database.db")
        cur = con.cursor()
        cur.execute('''
                INSERT INTO diaries (developer, project, start_time, end_time, repo_url, dev_note, code_snippet, language)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (data["developer"], data["project"], data["start_time"], data["end_time"], data["repo_url"], data["dev_note"], data["code_snippet"], data["language"]))
        cur.execute("UPDATE diaries SET time_worked = ROUND((strftime('%s', end_time) - strftime('%s', start_time)) / 60.0 / 15);")
        cur.execute("UPDATE diaries SET time_worked = printf('%d:%02d', (time_worked * 15) / 60, (time_worked * 15) % 60);")
        con.commit()
        con.close()
        return {"message": "Diary entry added successfully"}, 201
    else:
        return {"error": "Invalid JSON"}, 400

schema = {
    "type": "object",
    "validationLevel": "strict",
    "properties": {
        "developer": {
            "type": "string",
            "minLength": 1,
            "maxLength": 50
        },
        "project": {
            "type": "string",
            "minLength": 1,
            "maxLength": 100
        },
        "start_time": {
            "type": "string",
            "pattern": "^\d{4}\-\d{2}\-\d{2} \d{2}:\d{2}:\d{2}"
        },
        "end_time": {
            "type": "string",
            "pattern": "^\d{4}\-\d{2}\-\d{2} \d{2}:\d{2}:\d{2}"
        },
        "repo_url": {
            "type": "string",
            "pattern": "^https:\/\/github\.com\/[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+\/?$"
        },
        "dev_note": {
            "type": "string",
            "minLength": 1,
            "maxLength": 500
        },
        "code_snippet": {
            "type": "string",
            "minLength": 1,
            "maxLength": 2000
        },
        "language": {
            "type": "string",
            "enum": ["PYTHON", "CPP", "BASH", "SQL", "HTML", "CSS", "JAVASCRIPT"]
        }
    },
    "required": ["developer", "project", "start_time", "end_time", "repo_url", "dev_note", "code_snippet", "language"]
}

def validate_json(json_data):
    try:
        validate(instance=json_data, schema=schema)
        return True
    except:
        return False
    