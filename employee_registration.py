import boto3

# Initialize clients and resources
s3 = boto3.client('s3')
rekognition = boto3.client('rekognition', region_name='us-east-1')
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

# Set dynamodb table
dynamodbTableName='employee'
employeeTable = dynamodb.Table(dynamodbTableName)

def lambda_handler(event, context):
    print(event)

    # Get bucket name and key
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    try:
        # Index the new image into dynamodb
        response = index_employee_name(bucket, key)
        print(response)

        # Register employee on successful indexing
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            faceId = response['FaceRecords'][0]['Face']['FaceId']
            name = key.split('.')[0].split('_') # Naming convention: FirstName_LastName.jpg
            firstName = name[0]
            lastName = name[1]
            register_employee(faceId, firstName, lastName)
        
        return response

    except Exception as e:
        # handle as needed
        print(e)
        print(f'Error processing employee image {key} from bucket {bucket}')
        raise e

def index_employee_name(bucket, key):
    response = rekognition.index_faces(
        Image = {
            'S3Object':
            {
                'Bucket': bucket,
                'Name': key
            }
        },
        CollectionId="employees"
    )

    return response

def register_employee(faceId, firstName, lastName):
    employeeTable.put_item(
        Item={
            'rekognitionId': faceId,
            'firstName': firstName,
            'lastName': lastName
        }
    )