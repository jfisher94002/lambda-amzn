#!/usr/bin/env python3
"""
Test script for the Amazon Stock Tracker Lambda function with SNS integration
"""

import os
import boto3
import json
from datetime import datetime
from unittest.mock import patch, MagicMock
import argparse

# Import the Lambda function
import lambda_function

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Test Amazon Stock Tracker Lambda function with SNS')
parser.add_argument('--topic-arn', help='SNS Topic ARN to use for testing')
parser.add_argument('--real-sns', action='store_true', help='Use real SNS instead of mocking')
args = parser.parse_args()

# Configure SNS Topic ARN
if args.topic_arn:
    sns_topic_arn = args.topic_arn
    os.environ['SNS_TOPIC_ARN'] = sns_topic_arn
    print(f"Using provided SNS Topic ARN: {sns_topic_arn}")
else:
    sns_topic_arn = os.environ.get('SNS_TOPIC_ARN')
    if sns_topic_arn:
        print(f"Using SNS Topic ARN from environment: {sns_topic_arn}")
    else:
        sns_topic_arn = "arn:aws:sns:us-east-1:123456789012:amazon-stock-updates"
        os.environ['SNS_TOPIC_ARN'] = sns_topic_arn
        print(f"No SNS Topic ARN provided, using default: {sns_topic_arn}")

# Create mock event and context
class MockContext:
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

mock_event = {
    "version": "0",
    "id": "test-event-id",
    "detail-type": "Scheduled Event",
    "source": "aws.events",
    "account": "123456789012",
    "time": datetime.now().isoformat(),
    "region": "us-east-1",
    "resources": [
        "arn:aws:events:us-east-1:123456789012:rule/test-rule"
    ],
    "detail": {}
}

# Mock SNS client
class MockSNS:
    def __init__(self):
        self.published_messages = []
        
    def publish(self, **kwargs):
        print("\n--- SNS Message Would Be Sent ---")
        print(f"Topic ARN: {kwargs.get('TopicArn')}")
        print(f"Subject: {kwargs.get('Subject')}")
        print(f"Message: \n{kwargs.get('Message')}\n")
        print("--- End of SNS Message ---\n")
        
        self.published_messages.append(kwargs)
        return {"MessageId": "test-message-id-12345"}

# Run the Lambda function
def test_lambda():
    mock_context = MockContext()
    
    if args.real_sns:
        print("Testing with real SNS service...")
        # Let the function use the real boto3 client
        lambda_function.lambda_handler(mock_event, mock_context)
    else:
        print("Testing with mock SNS service...")
        mock_sns = MockSNS()
        
        # Patch the specific sns client in the lambda_function module
        with patch.object(lambda_function, 'sns', mock_sns):
            lambda_function.lambda_handler(mock_event, mock_context)
            
            if mock_sns.published_messages:
                print(f"Successfully sent {len(mock_sns.published_messages)} mock SNS message(s)")
            else:
                print("No SNS messages were sent")

if __name__ == "__main__":
    test_lambda()
