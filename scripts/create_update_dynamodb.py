import boto3

# # Initialize DynamoDB client
dynamodb = boto3.client('dynamodb')

# # Define the table name
table_name = 'Students'

# # Define the item to add or update
item = {
    'id': {'S': '12345'},  # the primary key of the table
    'full_name': {'S': 'Example Student'},
    'personal_website': {'S': 'examplestudent2.cetystijuana.com'}
}

# # Define the update expression
update_expression = 'SET #fn = :full_name, #pw = :personal_website'
expression_attribute_names = {
    '#fn': 'full_name',
    '#pw': 'personal_website'
}
expression_attribute_values = {
    ':full_name': {'S': 'Example Student2'},
    ':personal_website': {'S': 'examplestudent2.cetystijuana.com'}
}

# Try to update the item, if it doesn't exist, add it
try:
    response = dynamodb.update_item(
        TableName=table_name,
        Key={'id': {'S': '12345'}},
        UpdateExpression=update_expression,
        ExpressionAttributeNames=expression_attribute_names,
        ExpressionAttributeValues=expression_attribute_values,
        ReturnValues='ALL_NEW'
    )
    print('Item updated:', response['Attributes'])
except dynamodb.exceptions.ClientError as e:
    if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
        # Item doesn't exist, add it
        response = dynamodb.put_item(
            TableName=table_name,
            Item=item
        )
        print('Item added:', item)
    else:
        raise e
