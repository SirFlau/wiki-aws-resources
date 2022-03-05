from firebase_helper import db_connection, authenticate, authorize


def lambda_handler(event, context):
    authenticated, token_data = authenticate.authenticate_user(event["arguments"]["token"])
    if not authenticated:
        return {
            "message": f"Authentication failed, jwt token not valid, {token_data['message']}",
            "status": "Failed",
            "data": None
        }

    page_id = event["arguments"]["id"]

    db = db_connection.get_db_connection()

    if not authorize.authorize(user=token_data["user"], account=token_data["account"], entity=page_id, permission="read", db_connection=db):
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
