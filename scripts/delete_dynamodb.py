import boto3

# Initialize the DynamoDB client
dynamodb = boto3.client('dynamodb')

# Get a reference to the table
table = dynamodb.Table('Students')

# Define the item ID to delete
id = '00001'

# Try to delete the item with the specified ID
try:
    response = table.delete_item(
        Key={'id': {'S': id}}  # Use 'S' type specifier to indicate that 'id' is a string
    )
    print('Item deleted successfully:', response)
except dynamodb.exceptions.ConditionalCheckFailedException:
    # Catch the exception if there item does not exist
    print(f'Item with id={id} does not exist')
