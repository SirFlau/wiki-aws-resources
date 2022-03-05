from firebase_helper import db_connection, authenticate, authorize


def lambda_handler(event, context):
    authenticated, token_data = authenticate.authenticate_user(event["arguments"]["token"])
    if not authenticated:
        return f"Authentication failed, jwt token not valid, {token_data['message']}"

    page_id = event["arguments"]["id"]

    db = db_connection.get_db_connection()

    if not authorize.authorize(user=token_data["user"], account=token_data["account"], entity=page_id, permission="delete", db_connection=db):
        return "You do not have permissions to delete this page"

    db.collection("Page").document(page_id).delete()
    permissions = db.collection("Permissions").where("entity", "==", page_id).stream()
    for perm in permissions:
        perm.reference.delete()

    return "page deleted"
