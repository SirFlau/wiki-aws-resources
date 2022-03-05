from firebase_helper import db_connection, authorize, authenticate


def lambda_handler(event, context):
    authenticated, token_data = authenticate.authenticate_user(event["arguments"]["token"])
    if not authenticated:
        return f"Authentication failed, jwt token not valid, {token_data['message']}"

    page = event["arguments"]["page"]

    db = db_connection.get_db_connection()

    authorized = authorize.authorize(user=token_data["user"], account=token_data["account"], entity=token_data["account"], permission="write", db_connection=db)
    if not authorized:
        return "You do not have permissions to add a new page"

    page["account"] = token_data["account"]
    page["parentPage"] = page.get("parentPage", "")

    new_page_ref = db.collection("Page").add(page)[1]
    db.collection("Permissions").add(
        {
            "account": token_data["account"],
            "entity": new_page_ref.id,
            "entityType": "Page",
            "write": True,
            "delete": True,
            "read": True,
            "user": token_data["user"]
        }
    )

    account_obj = db.collection("Account").document(page["account"]).get().to_dict()
    if token_data["user"] != account_obj["owner"]:
        db.collection("Permissions").add(
            {
                "account": token_data["account"],
                "entity": new_page_ref.id,
                "entityType": "Page",
                "write": True,
                "delete": True,
                "read": True,
                "user": account_obj["owner"]
            }
        )

    return "Page added"
