from firebase_helper import db_connection, authenticate, authorize


def lambda_handler(event, context):
    token = event["source"]["token"]
    authenticated, token_data = authenticate.authenticate_user(token)
    if not authenticated:
        return {
            "message": f"Authentication failed, jwt token not valid, {token_data['message']}",
            "status": "Failed",
            "data": None
        }

    db = db_connection.get_db_connection()

    pages_ref = db.collection("Page").where("parentPage", "==", event["source"]["id"]).get()
    pages_view = []
    for page in pages_ref:
        if authorize.authorize(user=token_data["user"], account=token_data["account"], entity=page.id, permission="read", db_connection=db):
            page_dict = page.to_dict()
            page_dict["id"] = page.id
            pages_view.append(page_dict)

    return pages_view
