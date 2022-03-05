from firebase_helper import db_connection, authenticate, authorize


def lambda_handler(event, context):
    authenticated, token_data = authenticate.authenticate_user(event["arguments"]["token"])
    if not authenticated:
        return {
            "message": f"Authentication failed, jwt token not valid, {token_data['message']}",
            "status": "Failed",
            "data": None
        }

    db = db_connection.get_db_connection()

    pages_ref = db.collection("Page").where("account", "==", token_data["account"]).where("parentPage", "==", "").get()
    pages_view = []
    for page in pages_ref:
        if authorize.authorize(user=token_data["user"], account=token_data["account"], entity=page.id, permission="read", db_connection=db):
            page_dict = page.to_dict()
            page_dict["id"] = page.id
            page_dict["token"] = event["arguments"]["token"]
            pages_view.append(page_dict)

    return {
        "message": "",
        "status": "Success",
        "data": pages_view
    }
