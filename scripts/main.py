import json
import boto3
import urllib3
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    dynamo = boto3.resource("dynamodb")
    students_table = dynamo.Table("Students")
    matricula = event["id"]

    if matricula:
        try:
            student = students_table.get_item(Key={"id": matricula})
            api_key = get_secret()
            weather = get_weather(student, api_key)
            success_response = {
                "id": matricula,
                "full_name": student["Item"]["full_name"],
                "city": student["Item"]["city"],
                "weather": json.loads(weather)
            }
            return get_response(200, success_response)
        except ClientError as error:
            raise error
    else:
        return get_response(400, {"message": "Missing required field id"})


def get_weather(student, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather?q={0}&appid={1}"
    if "city" in student["Item"].keys():
        http = urllib3.PoolManager()
        response = http.request('GET', base_url.format(student["Item"]["city"], api_key))
        return response.data
    else:
        return json.dumps("No city assigned to student")


def get_secret():
    secretsmanager = boto3.client(service_name='secretsmanager')
    secret_name = "weather_api_profe"
    secrets_response = secretsmanager.get_secret_value(SecretId=secret_name)
    return secrets_response['SecretString']


def get_response(code, body):
    return {
        "statusCode": code,
        "body": body
    }