import boto3
import json

# # Initialize DynamoDB client
dynamodb = boto3.client('dynamodb')

# # Define the table name
table = 'Students'

# # Function to create (C) an item
def create_resource(payload):
    try:
        response = dynamodb.put_item(
            TableName=table,
            Item=payload
        )
        print(f"Student with id:{payload.get('id')} successfully created.")
        return {'statusCode': 200, 'body': json.dumps(response)}
    except Exception as e:
        return {'statusCode': 500, 'body': str(e)}

# # Function to find or read (R) an item
def get_resource(payload):
    try:
        response = dynamodb.get_item(
            TableName=table,
            Key={
            'id': {'S': payload.get('id')}
            })
        if 'Item' in response.keys():
            return {'statusCode': 200, 'body': json.dumps(response)}
        else:
            return {'statusCode': 404, 'body': 'Item not found'}
    except Exception as e:
        return {'statusCode': 500, 'body': str(e)}
    
# # Function to update (U) an item
def update_resource(payload):
    try:
        id = payload.get('id')
        update_expression = payload.get('updateExpression')
        expression_attribute_values = payload.get('expression_attribute_values')
        response = dynamodb.update_item(
            TableName=table,
            Key={'id': {'S': id}},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ConditionExpression='attribute_exists(id)',
            ReturnValues='ALL_NEW'
        )
        if 'Item' in response.keys():
            return {"statusCode": 200, "body": json.dumps(response)}
        else:
            return {"statusCode": 404, "body": "Item does not exist"}
    except Exception as e:
        return {"statusCode": 500, "body": str(e)}
    
# # Function to delete (D) an item
def delete_resource(payload):
    try:
        response = dynamodb.delete_item(
            TableName=table,
            Key={'id': {'S': payload.get('id')}}
            )
        if 'Item' in response.keys():
            print('Item deleted successfully:')
            return {"statusCode": 200, "body": json.dumps(response)}
        else:
            return {'statusCode': 404, 'body': 'Item does not exist'}
    except Exception as e:
        return {"statusCode": 500, "body": str(e)}
    

    