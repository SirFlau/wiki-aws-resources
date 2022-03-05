from firebase_helper import db_connection, authenticate, authorize


def lambda_handler(event, context):
    authenticated, token_data = authenticate.authenticate_user(event["arguments"]["token"])
    if not authenticated:
        return f"Authentication failed, jwt token not valid, {token_data['message']}"

    user_id = token_data["user"]

    db = db_connection.get_db_connection()

    event_page = event["arguments"]["page"]
    page_id = event_page.pop("id")

    authorized = authorize.authorize(user=user_id, account=token_data["account"], entity=page_id, permission="write", db_connection=db)
    if not authorized:
        return "Insufficient permissions to update page"

    db.collection("Page").document(page_id).update(event_page)

    return "Page updated"
