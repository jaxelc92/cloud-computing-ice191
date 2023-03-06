import boto3

# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb')

# Get a reference to the table
table = dynamodb.Table('Students')

# Define the key and attributes of the item
id = '12345'
full_name = 'Example Student'
personal_website = 'examplestudent.cetystijuana.com'

# Define the expression attribute values
expression_attribute_values = {
    ':name': full_name,
    ':website': personal_website
}

# Create or update the item in the table
try:
    response = table.update_item(
        Key={'id': {'S': id}}, # Use 'S' type specifier to indicate that 'id' is a string
        UpdateExpression='SET full_name = :name, personal_website = :website',
        ExpressionAttributeValues=expression_attribute_values,

        # this allows to specify that the condition that must be true for the update to be applied
        # so the update operation will only be performed if this condition evaluates to true
        ConditionExpression='attribute_exists(id)'
    )
    print('Item created or updated successfully.')
except Exception as e:
    # Catch the exception if there is any error
    print('Error creating or updating item:', e)
