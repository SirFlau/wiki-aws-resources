from firebase_helper import db_connection, authorize, authenticate


def lambda_handler(event, context):
    authenticated, token_data = authenticate.authenticate_user(event["arguments"]["token"])
    if not authenticated:
        return f"Authentication failed, jwt token not valid, {token_data['message']}"

    page = event["arguments"]["page"]

    db = db_connection.get_db_connection()

    authorized = authorize.authorize(user=token_data["user"], entity=token_data["account"], permission="write", db_connection=db)
    if not authorized:
        return "You do not have permissions to add a new page"

    page["account"] = token_data["account"]

    db.collection("Page").add(page)

    return "Page added"
