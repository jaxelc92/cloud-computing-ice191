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
    id = event.get('pathParameters', {}).get('id', None)
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
        payload = json.loads(event['body']) 
        get_response = get_resource(event) # validate if item exists in table
        if get_response['statusCode']==200: # If item exists do update
            id = event.get('pathParameters', {}).get('id', None)
            # Load corresponding data for the dynamodb update_item() method
            update_expression = 'SET #name = :full_name, #website = :personal_website'
            expression_attribute_names = {'#name': 'full_name', '#website': 'personal_website'}
            expression_attribute_values = {':full_name': payload['full_name'], ':personal_website': payload['personal_website']}
            response = dynamodb.update_item(
                TableName=table,
                Key={'id': {'S': id}}, # Use 'S' type specifier to indicate that 'id' is a string
                UpdateExpression=update_expression,
                ExpressionAttributeNames = expression_attribute_names,
                ExpressionAttributeValues=expression_attribute_values,
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
        get_response = get_resource(event) # Validate if item exists in table
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