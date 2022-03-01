from firebase_helper import db_connection, authenticate, authorize


def lambda_handler(event, context):
    authenticated, token_data = authenticate.authenticate_user(event["arguments"]["token"])
    if not authenticated:
        print(token_data["message"])
        return {
            "message": "Authentication failed, jwt token not valid",
            "status": "Failed",
            "data": None
        }

    page_id = event["arguments"]["id"]

    db = db_connection.get_db_connection()
    #permissions = db.collection("Permissions").where("user", "==", token_data["user"]).where("entity", "==", page_id).get()[0].to_dict()

    if not authorize.authorize(user=token_data["user"], entity=page_id, permission="read", db_connection=db):
        return {
            "message": "Unauthorized, you do not have permissions to view this page",
            "status": "Failed",
            "data": None
        }

    return {
        "message": "",
        "status": "Success",
        "data": db.collection('Page').document(page_id).get().to_dict()
    }
