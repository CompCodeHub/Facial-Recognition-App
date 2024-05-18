import boto3
import json

# Initialize clients and resources
s3 = boto3.client('s3')
rekognition = boto3.client('rekognition', region_name='us-east-1')
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

# Set dynamodb table
dynamodbTableName='employee'
employeeTable = dynamodb.Table(dynamodbTableName)
bucketName = '...'

def lambda_handler(event, context):
    print(event)

    # Get object from visitor images bucket
    objectKey = event['queryStringParameters']['objectKey']
    image_bytes = s3.get_object(Bucket=bucketName, Key=objectKey)['Body'].read()

    # Search faces from collection
    response = rekognition.search_faces_by_image(
        CollectionId = 'employees',
        Image = {'Bytes': image_bytes}
    )


    for match in response['faceMatches']:
        print(match['Face']['FaceId'], match['Face']['Confidence'])

        # Check if face id in dynamodb
        face = employeeTable.get(
            Key={
                'rekognitionId': match['Face']['FaceId']
            }
        )

        # Respond ok if person found
        if 'Item' in face:
            print('Person found: ', face['Item'])
            return buildResponse(200, {
                'Message': 'Success',
                'firstName': face['Item']['firstName'],
                'lastName': face['Item']['lastName']
            })
        
    print('Person could not be recognized!')
    return buildResponse(404, {'Message': 'Person not found!'})

def buildResponse(statusCode, body=None):
    response = {
        'statusCode': statusCode,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }

    if body is not None:
        response['body'] = json.dumps(body)

    return response


