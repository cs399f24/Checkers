import boto3
import json
import os
import logging

# Initialize logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table_name = os.environ['checkersboard']
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    # Extract HTTP method
    http_method = event['httpMethod']
    
    if http_method == 'GET':
        return get_board(event)
    elif http_method == 'POST':
        return update_board(event)
    else:
        return {
            'statusCode': 405,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'message': 'Method Not Allowed'})
        }

def get_board(event):
    try:
        game_id = event['queryStringParameters']['GameID']
        response = table.get_item(Key={'GameID': game_id})
        item = response.get('Item', {})
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(item)
        }
    except Exception as e:
        logger.error(f"Error getting board: {e}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'message': 'Internal Server Error'})
        }

def update_board(event):
    try:
        body = json.loads(event['body'])
        game_id = body['GameID']
        board_state = body['BoardState']
        turn = body['Turn']
        table.put_item(
            Item={
                'GameID': game_id,
                'BoardState': board_state,
                'Turn': turn
            }
        )
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'message': 'Board updated successfully'})
        }
    except Exception as e:
        logger.error(f"Error updating board: {e}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'message': 'Internal Server Error'})
        }