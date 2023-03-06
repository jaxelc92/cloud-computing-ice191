import crud_dynamobd
import json

def lambda_handler(event, context):
    operation = event.get('operation')
    payload = event.get('payload')

    if operation == 'create':
        response = crud_dynamobd.create_resource(payload)
    elif operation == 'read':
        response = crud_dynamobd.get_resource(payload)
    elif operation == 'update':
        response = crud_dynamobd.update_resource(payload)
    elif operation == 'delete':
        response = crud_dynamobd.delete_resource(payload)
    else:
        response = {"statsCode": 400, "error": "Invalid operation"}

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }