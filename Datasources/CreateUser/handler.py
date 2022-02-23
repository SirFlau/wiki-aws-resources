import firebase_admin
from firebase_admin import credentials, firestore


def lambda_handler(event, context):
    cred = credentials.Certificate("./firebase_credentials.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    user = event['arguments']['user']
    existing_user = db.collection('User').where("email", "==", user["email"]).get()
    if len(existing_user) > 0:
        return f"A user with email {user['email']} already exists"

    db.collection('User').add(user)

    return "User added"
