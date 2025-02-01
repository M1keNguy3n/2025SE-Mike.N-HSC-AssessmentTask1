from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import userManagement as dbHandler
from werkzeug.security import check_password_hash
import base64

api = Flask(__name__)
cors = CORS(api)
api.config["CORS_HEADERS"] = "Content-Type"
api_key = "Z6AxW9oTk9fXB8Kp"
limiter = Limiter(
    get_remote_address,
    app=api,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

def check_api_key():
    auth_key = request.headers.get("Authorization")
    if auth_key and auth_key.startswith("Bearer "):
        auth_key = auth_key.split(" ")[1]
        if auth_key == api_key:
            return None
    return jsonify({"error": "Invalid API key"}), 401


@api.route("/get_entry", methods=["GET"])
@limiter.limit("3/second", override_defaults=False)
def get_entry():
    api_key_error = check_api_key()
    if api_key_error:
        return api_key_error
    
    column_name = request.args.get('column_name')
    value = request.args.get('value')
    if not column_name or not value:
        return jsonify({"error": "Missing column_name or value parameter"}), 400
    data = dbHandler.get_diaries_by_column(column_name, value)
    return jsonify(data), 200


@api.route("/add_entry", methods=["POST"])
@limiter.limit("1/second", override_defaults=False)
def add_entry():
    api_key_error = check_api_key()
    if api_key_error:
        return api_key_error
    credentials_error = check_credentials()

    if credentials_error:
        return credentials_error
    
    data = request.get_json()
    response = dbHandler.insert_diaries_api(data)
    return response


if __name__ == "__main__":
    api.run(debug=True, host="0.0.0.0", port=3000)