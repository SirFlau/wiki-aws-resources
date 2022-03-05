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

    # check the account being updated is also the account logged into
    if permissions["entityType"] == "Account":
        if users_account.id != permissions["entity"]:
            return "You do not have permissions to change permissions on this account"
    # check the page being updated belongs to the account logged into
    elif permissions["entityType"] == "Page":
        page = db.collection("Page").document(permissions["entity"]).get().to_dict()
        if page["account"] != token_data["account"]:
            return "You do not have permissions to change permissions on this account"

    user = db.collection("User").where("email", "==", permissions.pop("email")).get()
    if len(user) == 0:
        return "Could not find user"

    permissions["user"] = user.id
    permissions["account"] = token_data["account"]

    db.collection("Permissions").add(permissions)

    return "Permissions added"
