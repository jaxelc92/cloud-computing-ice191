import crud_dynamobd
import json

def lambda_handler(event, context):
    operation = event['httpMethod']

    if operation == 'POST':
        response = crud_dynamobd.create_resource(event, context)
    elif operation == 'GET':
        response = crud_dynamobd.get_resource(event, context)
    elif operation == 'PATCH':
        response = crud_dynamobd.update_resource(event, context)
    elif operation == 'DELETE':
        response = crud_dynamobd.delete_resource(event, context)
    else:
        response = {"statsCode": 400, "error": "Invalid Http method"}

    return {
        'statusCode': response['statusCode'],
        'body': json.dumps(response)
    }