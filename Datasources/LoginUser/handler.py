import firebase_admin
from firebase_admin import credentials, firestore
import jwt
from datetime import datetime, timedelta

def lambda_handler(event, context):
    cred = credentials.Certificate("./firebase_credentials.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()

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
                             }, "secret_key_123", algorithm="HS256")
    }