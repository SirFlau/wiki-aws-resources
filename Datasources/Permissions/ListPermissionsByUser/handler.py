from firebase_helper import db_connection, authenticate


def lambda_handler(event, context):
    authenticated, token_data = authenticate.authenticate_user(event["arguments"]["token"])
    if not authenticated:
        return {
            "message": f"Authentication failed, jwt token not valid, {token_data['message']}",
            "status": "Failed",
            "data": None
        }

    db = db_connection.get_db_connection()

    permissions_ref = db.collection("Permissions").where("user", "==", token_data["user"]).get()
    permissions_view = []
    for perm in permissions_ref:
        permissions_view.append(perm.to_dict())

    return {
        "message": "",
        "status": "Success",
        "data": permissions_view
    }
