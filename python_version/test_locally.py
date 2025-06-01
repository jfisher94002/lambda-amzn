import json
import datetime
from lambda_function import lambda_handler

# Create a mock event and context
class LambdaContext:
    def __init__(self):
        self.function_name = "amazon-stock-tracker"
        self.function_version = "$LATEST"
        self.invoked_function_arn = "arn:aws:lambda:us-east-1:123456789012:function:amazon-stock-tracker"
        self.memory_limit_in_mb = 128
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

# Run the function
print("Testing Lambda function locally...")
try:
    lambda_handler(mock_event, mock_context)
    print("Lambda function executed successfully")
except Exception as e:
    print(f"Error executing Lambda function: {e}")
