from firebase_helper import db_connection, authenticate


def lambda_handler(event, context):
    authenticated, token_data = authenticate.authenticate_user(event["arguments"]["token"])
    if not authenticated:
        return f"Authentication failed, jwt token not valid, {token_data['message']}"

    db = db_connection.get_db_connection()
    # check the user owns the account they are logged into
    users_account = db.collection("Account").document(token_data["account"]).get()
    if users_account.to_dict()["owner"] != token_data["user"]:
        return "Only the owner of an account can update the permissions"

    permissions = event["arguments"]["permissions"]

    db_permissions = db.collection("Permissions").where("user", "==", permissions["user"]).where("account", "==", token_data["account"]).where("entity", "==", permissions["entity"]).get()
    if len(db_permissions) != 1:
        return "Could not find permissions to update"

    db_permissions[0].update(permissions)

    return "Permissions updated"
