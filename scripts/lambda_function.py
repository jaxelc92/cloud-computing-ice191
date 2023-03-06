import crud_dynamobd
import json

def lambda_handler(event, context):
    operation = event['operation']

    if operation == 'create':
        response = crud_dynamobd.create_resource(Item=event['payload'])
    elif operation == 'read':
        response = crud_dynamobd.get_resource(Key=event['payload'])
    elif operation == 'update':
        response = crud_dynamobd.update_resource(**event['payload'])
    elif operation == 'delete':
        response = crud_dynamobd.delete_resource(Key=event['payload'])
    else:
        response = {"statsCode": 400, "error": "Invalid operation"}

    return {
        'statusCode': 200,
        'body': json.dump(response)
    }