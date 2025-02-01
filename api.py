import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import userManagement as dbHandler
import os


api = Flask(__name__)
cors = CORS(api)
api.config["CORS_HEADERS"] = "Content-Type"
auth_key = "Z6AxW9oTk9fXB8Kp"
limiter = Limiter(
    get_remote_address,
    app=api,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)


@api.route("/get_entry", methods=["GET"])
@limiter.limit("3/second", override_defaults=False)
def get_entry():
    column_name = request.args.get('column_name')
    value = request.args.get('value')
    if not column_name or not value:
        return jsonify({"error": "Missing column_name or value parameter"}), 400
    data = dbHandler.get_diaries_by_column(column_name, value)
    return jsonify(data), 200


@api.route("/add_entry", methods=["POST"])
@limiter.limit("1/second", override_defaults=False)
def add_entry():
    if  request.headers.get("Authorization") == auth_key:
        data = request.get_json()
        response = dbHandler.insert_diaries_api(data)
        return response
    return jsonify({"error": "Unauthorized access"}), 401


if __name__ == "__main__":
    api.run(debug=True, host="0.0.0.0", port=3000)