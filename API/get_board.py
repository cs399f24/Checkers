import boto3
import json
import os

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        # Extract GameID from the query parameters
        game_id = event['queryStringParameters']['GameID']

        # Retrieve the item from DynamoDB
        response = table.get_item(Key={'GameID': game_id})
        item = response.get('Item', None)

        if not item:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'GameID not found'})
            }

        return {
            'statusCode': 200,
            'body': json.dumps(item)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }