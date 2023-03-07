import boto3
import json

# # Initialize DynamoDB client
dynamodb = boto3.client('dynamodb')

# # Define the table name
table = 'Students'

# # Function to create (C) an item
def create_resource(event):
    try:
        response = dynamodb.put_item(
            TableName=table,
            Item=event.get('body')
        )
        print(f"Student with id:{event.get('body').get('id')} successfully created.")
        return {'statusCode': 200, 'body': json.dumps(response)}
    except Exception as e:
        return {'statusCode': 500, 'body': str(e)}

# # Function to find or read (R) an item
def get_resource(event):
    try:
        response = dynamodb.get_item(
            TableName=table,
            Key={
            'id': {'S': event.get('pathParameters').get('id')}
            })
        if 'Item' in response.keys():
            return {'statusCode': 200, 'body': json.dumps(response)}
        else:
            return {'statusCode': 404, 'body': 'Item not found'}
    except Exception as e:
        return {'statusCode': 500, 'body': str(e)}
    
# # Function to update (U) an item
def update_resource(event):
    try:
        payload = json.loads(event['body'])
        get_response = get_resource(event)
        item = get_response.get('Item')
        if item:
            id = event.get('pathParameters').get('id')
            update_expression = 'SET #name = :full_name, #website = :personal_website'
            expression_attribute_names = {'#name': 'full_name', '#website': 'personal_website'}
            expression_attribute_values = {':full_name': payload['full_name'], ':personal_website': payload['personal_website']}
            response = dynamodb.update_item(
                TableName=table,
                Key={'id': {'S': id}},
                UpdateExpression=update_expression,
                ExpressionAttributeNames = expression_attribute_names,
                ExpressionAttributeValues=expression_attribute_values,
                ConditionExpression='attribute_exists(id)',
                ReturnValues='ALL_NEW'
            )
            return {"statusCode": 200, "body": json.dumps(response)}
        else:
            return {"statusCode": 404, "body": "Item does not exist"}
    except Exception as e:
        return {"statusCode": 500, "body": str(e)}
    
# # Function to delete (D) an item
def delete_resource(event):
    try:
        get_response = get_resource(event)
        item = get_response.get('Item')
        if item:
            response = dynamodb.delete_item(
                TableName=table,
                Key={'id': {'S': event.get('body').get('id')}}
                )
            print('Item deleted successfully:')
            return {"statusCode": 200, "body": json.dumps(response)}
        else:
            return {'statusCode': 404, 'body': 'Item does not exist'}
    except Exception as e:
        return {"statusCode": 500, "body": str(e)}
    

    