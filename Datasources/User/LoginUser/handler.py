import jwt
from datetime import datetime, timedelta
from firebase_helper import db_connection
import os


def lambda_handler(event, context):
    db = db_connection.get_db_connection()

    request_user = event['arguments']['user']

    db_user = db.collection('User').where("email", "==", request_user["email"]).get()

    if len(db_user) != 1:
        return {
            "message": "No user with the given email was found",
            "status": "Failed",
            "token": None
        }

    if db_user.password != request_user.password:
        return {
            "message": "password did not match",
            "status": "Failed",
            "token": None
        }

    return {
        "message": "Logged in",
        "status": "Success",
        "token": jwt.encode({"expiration": (datetime.now() + timedelta(hours=3)).timestamp(),
                             "user": db_user[0].id
                             }, os.environ["JWTSECRET"], algorithm="HS256")
    }