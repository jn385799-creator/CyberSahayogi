import boto3
import bcrypt
import jwt
import datetime
import os
from moto import mock_aws
from boto3.dynamodb.conditions import Key

# नक्कली क्रेडेन्सियल्स
os.environ["AWS_ACCESS_KEY_ID"] = "testing"
os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
os.environ["AWS_SECURITY_TOKEN"] = "testing"
os.environ["AWS_SESSION_TOKEN"] = "testing"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

SECRET_KEY = "shield_auth_1M_secret"

def run_shield_system():
    # १. mock_aws को कन्ट्याक्स्ट भित्र सबै काम गर्ने
    with mock_aws():
        db = boto3.resource('dynamodb', region_name='us-east-1')
        
        # २. टेबल बनाउने
        table = db.create_table(
            TableName='ShieldAuthUsers',
            KeySchema=[{'AttributeName': 'PK', 'KeyType': 'HASH'}],
            AttributeDefinitions=[
                {'AttributeName': 'PK', 'AttributeType': 'S'},
                {'AttributeName': 'email', 'AttributeType': 'S'}
            ],
            GlobalSecondaryIndexes=[{
                'IndexName': 'EmailIndex',
                'KeySchema': [{'AttributeName': 'email', 'KeyType': 'HASH'}],
                'Projection': {'ProjectionType': 'ALL'}
            }],
            BillingMode='PAY_PER_REQUEST'
        )

        # ३. साइन-अप फङ्सन
        email = "test@gmail.com"
        password = "Nepal@123"
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        table.put_item(Item={
            'PK': f"GMAIL#{email}",
            'email': email,
            'password': hashed.decode('utf-8')
        })
        print(f"✅ साइन-अप सफल: {email}")

        # ४. लगइन फङ्सन
        print("लगइन प्रयास गर्दै...")
        response = table.query(
            IndexName='EmailIndex',
            KeyConditionExpression=Key('email').eq(email)
        )
        
        if response['Items']:
            user = response['Items'][0]
            if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                token = jwt.encode({
                    'user_id': user['PK'],
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
                }, SECRET_KEY, algorithm='HS256')
                print(f"🔓 लगइन सफल! JWT टोकन तयार भयो।")
                print(f"टोकनको केही अंश: {token[:30]}...")
            else:
                print("❌ गलत पासवर्ड!")
        else:
            print("❌ प्रयोगकर्ता भेटिएन!")

if __name__ == '__main__':
    run_shield_system()
