from firebase_helper import db_connection


def lambda_handler(event, context):
    db = db_connection.get_db_connection()

    user = event["arguments"]["login"]

    db_user = db.collection("User").where("email", "==", user["email"]).get()
    user_id = db_user[0].id

    if len(db_user) != 1:
        return {
            "message": "No user with the given email was found",
            "status": "Failed",
            "data": []
        }

    if db_user[0].to_dict()["password"] != user["password"]:
        return {
            "message": "password did not match",
            "status": "Failed",
            "data": []
        }

    permissions = db.collection("Permissions").where("entityType", "==", "Account").where("user", "==", user_id).get()
    accounts = []
    for perm in permissions:
        account_id = perm.to_dict()["entity"]
        ref = db.collection("Account").document(account_id).get()
        account_name = ref.to_dict()["name"]
        accounts.append({"name": account_name,
                         "id": account_id})

    return {
        "message": "Logged in",
        "status": "Success",
        "data": accounts
    }
