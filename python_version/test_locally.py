import json
import datetime
import os
import sys
from unittest.mock import patch, MagicMock
import importlib

# Create a mock SNS client for local testing
class MockSNS:
    def __init__(self):
        self.published_messages = []
        
    def publish(self, **kwargs):
        print(f"\n--- SNS Message Would Be Sent ---")
        print(f"Topic ARN: {kwargs.get('TopicArn')}")
        print(f"Subject: {kwargs.get('Subject')}")
        print(f"Message: \n{kwargs.get('Message')}\n")
        print("--- End of SNS Message ---\n")
        
        self.published_messages.append({
            "TopicArn": kwargs.get('TopicArn'),
            "Subject": kwargs.get('Subject'),
            "Message": kwargs.get('Message')
        })
        
        return {"MessageId": "test-message-id"}

# Create a mock event and context
class LambdaContext:
    def __init__(self):
        self.function_name = "amazon-stock-tracker"
        self.function_version = "$LATEST"
        self.invoked_function_arn = "arn:aws:lambda:us-east-1:123456789012:function:amazon-stock-tracker"
        self.memory_limit_in_mb = "128"
        self.aws_request_id = "test-request-id"
        self.log_group_name = "/aws/lambda/amazon-stock-tracker"
        self.log_stream_name = "2023/06/01/[$LATEST]test"
        
    def get_remaining_time_in_millis(self):
        return 30000
        
# Set up environment variables for testing
os.environ['SNS_TOPIC_ARN'] = 'arn:aws:sns:us-east-1:123456789012:amazon-stock-updates'

# Set up mocks before importing the lambda function
mock_sns_client = MockSNS()

# Create a mock boto3 module
mock_boto3 = MagicMock()
mock_boto3.client.return_value = mock_sns_client

# Add the mock to sys.modules
sys.modules['boto3'] = mock_boto3

# Now import the lambda function (it will use the mocked boto3)
from lambda_function import lambda_handler

# Mock event
mock_event = {
    "version": "0",
    "id": "test-event-id",
    "detail-type": "Scheduled Event",
    "source": "aws.events",
    "account": "123456789012",
    "time": datetime.datetime.now().isoformat(),
    "region": "us-east-1",
    "resources": [
        "arn:aws:events:us-east-1:123456789012:rule/test-rule"
    ],
    "detail": {}
}

# Create context
mock_context = LambdaContext()

# Run the function with mocked SNS
print("Testing Lambda function locally with SNS simulation...")
mock_sns = MockSNS()

try:
    # Create a simple mock for boto3.client
    mock_client = MagicMock()
    mock_client.return_value = mock_sns
    
    # Patch boto3.client with our mock
    with patch('lambda_function.boto3.client', mock_client):
        lambda_handler(mock_event, mock_context)
        
    print("Lambda function executed successfully")
    
    if mock_sns.published_messages:
        print(f"Successfully sent {len(mock_sns.published_messages)} SNS message(s)")
    else:
        print("No SNS messages were sent")
        
except Exception as e:
    print(f"Error executing Lambda function: {e}")
