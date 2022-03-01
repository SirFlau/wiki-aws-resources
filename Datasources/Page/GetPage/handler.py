from firebase_helper import db_connection


def lambda_handler(event, context):

    db = db_connection.get_db_connection()

    return db.collection('User').document(event['arguments']['id']).get().to_dict()
