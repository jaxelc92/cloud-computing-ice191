import boto3

# Initialize the DynamoDB client
dynamodb = boto3.client('dynamodb')

# Define the table name and the item ID to delete
table_name = 'Students'

# Try to delete the item with the specified ID
try:
    response = dynamodb.delete_item(
        TableName=table_name,
        Key={'id': {'S': '12345'}}
    )
    print('Item deleted successfully:', response)
except dynamodb.exceptions.ConditionalCheckFailedException:
    print(f'Item with id={id} does not exist')
