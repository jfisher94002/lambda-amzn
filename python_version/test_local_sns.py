#!/usr/bin/env python3
"""
Test script to run the Lambda function locally with mocked AWS services
"""
import json
import os
import datetime
from unittest.mock import patch, MagicMock

# Set up environment variables for testing
os.environ['SNS_TOPIC_ARN'] = 'arn:aws:sns:us-east-1:123456789012:amazon-stock-updates'

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

# Create a mock for the SNS publish method that records all messages
class MockSNSClient:
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
        
        return {"MessageId": "test-message-id-123456"}

def main():
    # Import the Lambda handler and module
    import lambda_function
    from lambda_function import lambda_handler
    
    # Create a mock SNS client
    mock_sns = MockSNSClient()
    
    # Run the function with mocked SNS
    print("Testing Lambda function locally with SNS simulation...")
    
    try:
        # Directly patch the SNS client in the lambda_function module
        with patch.object(lambda_function, 'sns', mock_sns):
            # Execute the Lambda function
            lambda_handler(mock_event, mock_context)
            
        print("Lambda function executed successfully")
        
        # Check if any SNS messages were published
        if mock_sns.published_messages:
            print(f"Successfully sent {len(mock_sns.published_messages)} SNS message(s)")
        else:
            print("No SNS messages were sent")
            
    except Exception as e:
        print(f"Error executing Lambda function: {e}")
        raise

if __name__ == "__main__":
    main()
