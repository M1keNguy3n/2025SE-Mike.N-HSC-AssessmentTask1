import sqlite3 as sql
from flask_login import UserMixin
from jsonschema import validate
import pyotp

class User(UserMixin):
    def __init__(self, id, email, password, otp_secret, api_key, api_key_expiration):
        self.id = id
        self.email = email
        self.password = password
        self.otp_secret = otp_secret
        self.api_key = api_key
        self.api_key_expiration = api_key_expiration

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

def insert_user(email, password, otp_secret, api_key, api_key_expiration):
    con = sql.connect(".databaseFiles/database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO users (K3hq4_email, 55ama_password, vx6rf_otp_secret, UsA17_api_key, 0RIEp_api_key_expiration) VALUES (?, ?, ?, ?, ?)", (email, password, otp_secret, api_key, api_key_expiration))
    con.commit()
    con.close()

def get_user_by_column(column_name, value):
    con = sql.connect(".databaseFiles/database.db")
    cur = con.cursor()
    query = f'SELECT * FROM users WHERE {column_name} = ?'
    user = cur.execute(query, (value,)).fetchone()
    con.close()
    if user:
        return User(user[0], user[1], user[2], user[3], user[4], user[5])
    return None

def get_diary_by_id(entry_id):
    con = sql.connect(".databaseFiles/database.db")
    cur = con.cursor()
    query = 'SELECT * FROM diaries WHERE HAUIe_id = ?'
    entry = cur.execute(query, (entry_id,)).fetchone()
    con.close()
    return entry

def delete_diary(entry_id):
    con = sql.connect(".databaseFiles/database.db")
    cur = con.cursor()
    cur.execute('DELETE FROM diaries WHERE HAUIe_id = ?', (entry_id,))
    con.commit()
    con.close()

def update_user_api_key(user_id, api_key, api_key_expiration):
    con = sql.connect(".databaseFiles/database.db")
    cur = con.cursor()
    cur.execute("UPDATE users SET UsA17_api_key = ?, 0RIEp_api_key_expiration = ? WHERE xpp9x_id = ?", (api_key, api_key_expiration, user_id))
    con.commit()
    con.close()

def update_user_otp_secret(user_id, otp_secret):
    con = sql.connect(".databaseFiles/database.db")
    cur = con.cursor()
    cur.execute("UPDATE users SET vx6rf_otp_secret = ? WHERE xpp9x_id = ?", (otp_secret, user_id))
    con.commit()
    con.close()

def insert_diaries_api(data):
    print(data)
    if validate_json(data):
        con = sql.connect(".databaseFiles/database.db")
        cur = con.cursor()
        cur.execute('''
                INSERT INTO diaries (Nzdvy_developer, hBbdT_project, uYCKJ_start_time, MbOId_end_time, Aiiyt_repo_url, LaH8Y_dev_note, qVKdx_code_snippet, xI1ka_language, FVtfU_owner)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (data["developer"], data["project"], data["start_time"], data["end_time"], data["repo_url"], data["dev_note"], data["code_snippet"], data["language"], data["owner"]))
        cur.execute("UPDATE diaries SET vTJWO_time_worked = ROUND((strftime('%s', MbOId_end_time) - strftime('%s', uYCKJ_start_time)) / 60.0 / 15);")
        cur.execute("UPDATE diaries SET vTJWO_time_worked = printf('%d:%02d', (vTJWO_time_worked * 15) / 60, (vTJWO_time_worked * 15) % 60);")
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
        },
        "owner":{
            "type": "number"
        }
    },
    "required": ["developer", "project", "start_time", "end_time", "repo_url", "dev_note", "code_snippet", "language", "owner"]
}

def validate_json(json_data):
    try:
        validate(instance=json_data, schema=schema)
        return True
    except:
        return False
    