import os
from datetime import datetime, timedelta

import jwt
from firebase_helper import db_connection, authorize


def lambda_handler(event, context):
    db = db_connection.get_db_connection()

    request_login = event["arguments"]["login"]

    db_user = db.collection("User").where("email", "==", request_login["email"]).get()
    user_id = db_user[0].id

    if len(db_user) != 1:
        return {
            "message": "No user with the given email was found",
            "status": "Failed",
            "token": None
        }

    if db_user[0].to_dict()["password"] != request_login["password"]:
        return {
            "message": "password did not match",
            "status": "Failed",
            "token": None
        }

    db_account = db.collection("Account").document(request_login["account"]).get().to_dict()

    authorized = authorize.authorize(user=user_id, account=request_login["account"], entity=request_login["account"], permission="read", db_connection=db)
    if db_account["owner"] != user_id and not authorized:
        return {
            "message": "You do not have access to the given account",
            "status": "Failed",
            "token": None
        }

    return {
        "message": "Logged in",
        "status": "Success",
        "token": jwt.encode({"expiration": (datetime.now() + timedelta(hours=3)).timestamp(),
                             "user": db_user[0].id,
                             "account": request_login["account"]
                             }, os.environ["JWTSECRET"], algorithm="HS256")
    }
