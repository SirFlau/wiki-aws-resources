from firebase_helper import db_connection


def lambda_handler(event, context):
    db = db_connection.get_db_connection()

    user = event['arguments']['user']
    existing_user = db.collection('User').where("email", "==", user["email"]).get()
    if len(existing_user) > 0:
        return f"A user with email {user['email']} already exists"

    account_name = user.pop("accountName", None)
    if not account_name:
        return "You must supply an account name with your user"

    new_user_ref = db.collection('User').add(user)[1]

    new_account_ref = db.collection("Account").add({
        "name": account_name,
        "owner": new_user_ref.id
    })[1]

    db.collection("Permissions").add(
        {
            "account": new_account_ref.id,
            "entity": new_account_ref.id,
            "entityType": "Account",
            "write": True,
            "delete": True,
            "read": True,
            "user": new_user_ref.id
        }
    )

    return "User account added"
