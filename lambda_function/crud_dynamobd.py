import boto3
import json

# # Initialize DynamoDB client
dynamodb = boto3.client('dynamodb')

# # Define the table name
table = dynamodb.Table('Students')

# # Function to create (C) an item
def create_resource(payload):
    try:
        response = table.put_item(
            Item=payload
        )
        print(f"Student with id:{payload.get('id')} successfully created.")
        return {'statusCode': 200, 'body': json.dumps(response)}
    except Exception as e:
        return {'statusCode': 500, 'body': str(e)}

# # Function to find or read (R) an item
def get_resource(payload):
    try:
        response = table.get_item(
            Key={
            'id': {'S': payload.get('id')}
            })
        item=response.get('Item')
        if item:
            return {'statusCode': 200, 'body': json.dumps(item)}
        else:
            return {'statusCode': 404, 'body': 'Item not found'}
    except Exception as e:
        return {'statusCode': 500, 'body': str(e)}
    
# # Function to update (U) an item
def update_resource(payload):
    try:
        response = table.update_item(
            Key={'id': {'S': payload.get('id')}},
            UpdateExpression=payload.get('UpdateExpression'),
            ExpressionAttributeValues=payload.get('expression_attribute_values'),
            ConditionExpression=payload.get('conditionExpression'),
            ReturnValues='ALL_NEW'
        )
        item = response.get('Item')
        if item:
            return {"statusCode": 200, "body": json.dumps(response)}
        else:
            return {"statusCode": 404, "body": "Item does not exist"}
    except Exception as e:
        return {"statusCode": 500, "body": str(e)}
    
# # Function to delete (D) an item
def delete_resource(payload):
    try:
        response = table.delete_item(
        Key={'id': {'S': payload.get('id')}}
        )
        item = response.get('Item')
        if item:
            print('Item deleted successfully:')
            return {"statusCode": 200, "body": json.dumps(response)}
        else:
            return {'statusCode': 404, 'body': 'Item does not exist'}
    except Exception as e:
        return {"statusCode": 500, "body": str(e)}
    

    