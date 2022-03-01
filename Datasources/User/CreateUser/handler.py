from firebase_helper import db_connection


def lambda_handler(event, context):
    db = db_connection.get_db_connection()

    user = event['arguments']['user']
    existing_user = db.collection('User').where("email", "==", user["email"]).get()
    if len(existing_user) > 0:
        return f"A user with email {user['email']} already exists"

    db.collection('User').add(user)

    return "User added"

