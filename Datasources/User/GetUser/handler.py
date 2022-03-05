from firebase_helper import db_connection, authenticate


def lambda_handler(event, context):
    authenticated, token_data = authenticate.authenticate_user(event["arguments"]["token"])
    if not authenticated:
        return {
            "message": "Authentication failed, jwt token not valid",
            "status": "Failed",
            "data": None
        }
    if event["arguments"]["id"] != token_data["user"]:
        return {
            "message": "Unauthorized, you do not have permissions to view this user",
            "status": "Failed",
            "data": None
        }

    db = db_connection.get_db_connection()

    return {
        "message": "",
        "status": "Success",
        "data": db.collection('User').document(event['arguments']['id']).get().to_dict()
    }
        
