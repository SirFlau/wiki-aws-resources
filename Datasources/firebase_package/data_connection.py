import firebase_admin
from firebase_admin import credentials, firestore


def get_db_connection():
    cred = credentials.Certificate("./firebase_credentials.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db
