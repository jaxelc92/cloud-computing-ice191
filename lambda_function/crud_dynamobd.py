import boto3
import json

# # Initialize DynamoDB client
dynamodb = boto3.client('dynamodb')

# # Define the table name
table = 'Students'

# # Function to create (C) an item
def create_resource(event, context):
    try:
        # Load json object from the input format of lambda integration proxy
        # from API request calling the Lambda function
        item = json.loads(event['body'])
        response = dynamodb.put_item(
            TableName=table,
            Item=item
        )
        # if item successfully created
        print(f"Student with id:{item['id']} successfully created.")
        return {
                'statusCode': 200,
                'body': response
                }
    except Exception as e:
        # Catch exception if there is any error
        return {
            'statusCode': 500,
            'body': str(e)
            }

# # Function to find or read (R) an item
def get_resource(event, context):
    id = event.get('pathParameters').get('id')
    if not id:
        return {
            'statusCode': 400,
            'body': 'Need to input an id'
        }
    try:
        response = dynamodb.get_item(
            TableName=table,
            Key={
            # Use 'S' type specifier to indicate that 'id' is a string
            'id': {'S': id} # get the id from the path parameter in the API Gateway URL
            })
        if "Item" in response:
            return {
                'statusCode': 200,
                'body': response
                }
        else:
            return {
                'statusCode': 404,
                'body': 'Item not found'
                }
    except Exception as e:
        return {
            'body': str(e)
        }
    
# # Function to update (U) an item
def update_resource(event, context):
    try:
        # Load json object from the input format of lambda integration proxy
        # from API request calling the Lambda function
        get_response = get_resource(event, context) # validate if item exists in table
        if get_response['statusCode']==200: # If item exists do update
            id = event.get('pathParameters').get('id')
            item = json.loads(event['body'])
            response = dynamodb.update_item(
                TableName=table,
                Key={'id': {'S': id}}, # Use 'S' type specifier to indicate that 'id' is a string
                UpdateExpression = item['UpdateExpression'],
                ExpressionAttributeValues = {":name": item["payload"]["full_name"], ":website": item["payload"]["personal_website"], ":city": item["payload"]["city"]},
                ConditionExpression='attribute_exists(id)',
                ReturnValues='ALL_NEW'
            )
            return {
                'statusCode': 200,
                'body': response
                }
        else:
            return {
                'statusCode': 404,
                'body': 'Item does not exist'
                }
    except Exception as e:
        # Catch exception if there is any error
        return {
            'statusCode': 500,
            'body': str(e)
            }
    
# # Function to delete (D) an item
def delete_resource(event, context):
    id = event.get('pathParameters').get('id')
    if not id:
        return {
            'statusCode': 400,
            'body': 'Need to input an id'
        }
    try:
        get_response = get_resource(event, context) # Validate if item exists in table
        if get_response['statusCode']==200: # If item exists do delete
            response = dynamodb.delete_item(
                TableName=table,
                # Use 'S' type specifier to indicate that 'id' is a string
                Key={'id': {'S': id}}
                )
            print('Item deleted successfully:')
            return {
                'statusCode': 200,
                'body': response
                }
    except KeyError as e:
        # Catch exception if there is any error
        return {
            'statusCode': 404,
            'body': 'Item does not exist'
            }