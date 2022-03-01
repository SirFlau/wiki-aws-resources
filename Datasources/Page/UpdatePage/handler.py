from firebase_helper import db_connection, authenticate

def lambda_handler(event, context):
    authenticated, token_data = authenticate.authenticate_user(event["arguments"]["token"])
    if not authenticated:
        return "Unauthorized"

    db = db_connection.get_db_connection()
    

    page = event["arguments"]["page"]
    page["owner"] = token_data["user"]

    db.collection('Page').add(page)

    return "Page added"

