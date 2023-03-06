import boto3


# Create a DynamoDB client object
dynamodb = boto3.resource('dynamodb')

# Define the name of the table we want to work with
table = dynamodb.Table('Students')

# Define the value of the id attribute for the item we want to find
id = '12345'

try:
    response = table.get_item(
        # Use the S type specifier to indicate that the id attribute is a string
        Key={'id': {'S': id}} 
        )
    if 'Item' in response:
        item = response['Item']
        print(f'Item with ID {id} was found: {item}')
    else:
        print(f'Item with ID {id} was not found in the table.')
    
except dynamodb.exceptions.ResourceNotFoundException:
    # If the table does not exist, output an error message
    print(f'Table "{table}" does not exist')

except dynamodb.exceptions.DynamoDBKeyNotFoundError:
    # If the item with the specified id does not exist, output an error message
    print(f'Item with ID {id} not found')
    
except Exception as e:
    # If an unknown error occurs, output the details of the exception
    print(f'Error: {e}')
