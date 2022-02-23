import firebase_admin
from firebase_admin import credentials, firestore


def lambda_handler(event, context):
    cred = credentials.Certificate("./firebase_credentials.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    return db.collection('User').document(event['arguments']['id']).get().to_dict()