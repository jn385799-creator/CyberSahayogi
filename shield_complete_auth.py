import boto3
import bcrypt
import jwt
import datetime
import os
from moto import mock_aws
from boto3.dynamodb.conditions import Key

# १. नक्कली AWS साँचोहरू सेट गर्ने (यो त्रुटि हटाउनको लागि अनिवार्य छ)
os.environ["AWS_ACCESS_KEY_ID"] = "testing"
os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
os.environ["AWS_SECURITY_TOKEN"] = "testing"
os.environ["AWS_SESSION_TOKEN"] = "testing"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

SECRET_KEY = "shield_auth_1M_secret"

@mock_aws
class ShieldAuthSystem:
    def __init__(self):
        # २. डाटाबेस सेटअप
        self.db = boto3.resource('dynamodb', region_name='us-east-1')
        self.table = self.db.create_table(
            TableName='ShieldAuthUsers',
            KeySchema=[{'AttributeName': 'PK', 'KeyType': 'HASH'}],
            AttributeDefinitions=[
                {'AttributeName': 'PK', 'AttributeType': 'S'},
                {'AttributeName': 'email', 'AttributeType': 'S'}
            ],
            GlobalSecondaryIndexes=[{
                'IndexName': 'EmailIndex',
                'KeySchema': [{'AttributeName': 'email', 'KeyType': 'HASH'}],
                'Projection': {'ProjectionType': 'ALL'},
                'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
            }],
            BillingMode='PAY_PER_REQUEST'
        )

    def signup(self, email, password):
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.table.put_item(Item={
            'PK': f"GMAIL#{email}",
            'email': email,
            'password': hashed.decode('utf-8'),
            'created_at': str(datetime.datetime.now())
        })
        print(f"✅ साइन-अप सफल: {email}")

    def login(self, email, password):
        response = self.table.query(
            IndexName='EmailIndex',
            KeyConditionExpression=Key('email').eq(email)
        )
        
        if not response['Items']:
            return "❌ प्रयोगकर्ता भेटिएन!"

        user = response['Items'][0]
        stored_hash = user['password'].encode('utf-8')

        if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
            token = jwt.encode({
                'user_id': user['PK'],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }, SECRET_KEY, algorithm='HS256')
            return f"🔓 लगइन सफल! टोकन: {token[:25]}..."
        else:
            return "❌ गलत पासवर्ड!"

# ३. टेस्ट रन
system = ShieldAuthSystem()
my_email = "test@gmail.com"
system.signup(my_email, "Nepal@123")

print("\nलगइन प्रयास गर्दै...")
print(system.login(my_email, "Nepal@123"))
