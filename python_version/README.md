# 

- Adding error handling and retry logic
- Setting up SNS notifications for price alerts
- Adding code to store the data in DynamoDB
- Changing the stock symbol

You can customize this Lambda function by:

## Customizing

```html
  --targets '{"Id": "1", "Arn": "arn:aws:lambda:REGION:ACCOUNT_ID:function:amazon-stock-tracker"}'
  --rule DailyAmazonStockCheck \
aws events put-targets \
```

3. Configure the rule to target your Lambda function:

```sh
  --source-arn arn:aws:events:REGION:ACCOUNT_ID:rule/DailyAmazonStockCheck
  --principal events.amazonaws.com \
  --action lambda:InvokeFunction \
  --statement-id EventBridgeInvoke \
  --function-name amazon-stock-tracker \
aws lambda add-permission \
```

4. Add permission for EventBridge to invoke your Lambda:

```sh
  --schedule-expression "cron(0 16 * * ? *)"  # Runs daily at 4 PM UTC
  --name "DailyAmazonStockCheck" \
aws events put-rule \
```

5. Create an EventBridge (formerly CloudWatch Events) rule using AWS Console or AWS CLI:

## Scheduling the Lambda Function

```sh
  --zip-file fileb://deployment_package.zip
  --function-name amazon-stock-tracker \
aws lambda update-function-code \
```

3. Update an existing function:

```sh
  --role arn:aws:iam::ACCOUNT_ID:role/lambda-execution-role
  --zip-file fileb://deployment_package.zip \
  --handler lambda_function.lambda_handler \
  --runtime python3.9 \
  --function-name amazon-stock-tracker \
aws lambda create-function \
```

4. Deploy using AWS CLI:

5. Create a deployment package as shown above

#### Option 2: Deploy using AWS CLI

2. Upload the `deployment_package.zip` file to AWS Lambda through the AWS Console

```sh
cd package && zip -r ../deployment_package.zip .
cp lambda_function.py package/
pip install -t package/ -r requirements.txt
```

3. Create a deployment package:

#### Option 1: Deploy using AWS Console

### Deploying to AWS Lambda

```sh
python test_locally.py
```

4. Run the function locally:

```sh
pip install -r requirements.txt
```

5. Install dependencies:

```sh
source venv/bin/activate  # On Windows: venv\Scripts\activate
python -m venv venv
```

6. Create a virtual environment and activate it:

7. Make sure you have Python 3.8+ installed

### Local Development

## Setup Instructions

- Can be extended to store data in a database, send alerts, etc.
- Runs on a scheduled basis (e.g., daily) using AWS EventBridge
- Fetches Amazon stock price data using Google Finance

## Features

This AWS Lambda function retrieves the current Amazon (AMZN) stock price from Google Finance and logs the information.
Amazon Stock Tracker Lambda Function (Python)

## AWS CLI Commands Reference

These AWS CLI commands can be used to manage and troubleshoot your Amazon Stock Tracker Lambda function:

### Lambda Function Management

```bash
# List Lambda functions in a region
aws lambda list-functions --region us-east-1 --query "Functions[].FunctionName" --output text

# Get Lambda function configuration
aws lambda get-function-configuration --function-name amazon-stock-tracker --region us-east-1 --query "Environment" --output json

# Invoke the Lambda function for testing
aws lambda invoke --function-name amazon-stock-tracker --region us-east-1 --payload '{}' --cli-binary-format raw-in-base64-out /tmp/lambda-output.txt && cat /tmp/lambda-output.txt
```

### SNS Management

```bash
# List SNS topics that contain 'amazon-stock-updates'
aws sns list-topics --region us-east-1 --query "Topics[?contains(TopicArn, 'amazon-stock-updates')].TopicArn" --output text

# Store SNS ARN in a variable and update Lambda function with it
SNS_ARN=$(aws sns list-topics --region us-east-1 --query "Topics[?contains(TopicArn, 'amazon-stock-updates')].TopicArn" --output text)
aws lambda update-function-configuration --function-name amazon-stock-tracker --region us-east-1 --environment "Variables={SNS_TOPIC_ARN=$SNS_ARN}"

# List SNS subscriptions for the topic
aws sns list-subscriptions-by-topic --topic-arn "$SNS_ARN" --region us-east-1
```

### IAM Policy Management

```bash
# Get Lambda function's execution role
aws lambda get-function --function-name amazon-stock-tracker --region us-east-1 --query "Configuration.Role" --output text

# List policies attached to the Lambda execution role
aws iam list-role-policies --role-name lambda-eventbridge-role
```

### CloudWatch Logs

```bash
# List CloudWatch log groups for the Lambda function
aws logs describe-log-groups --region us-east-1 --query "logGroups[?contains(logGroupName, 'amazon-stock-tracker')].logGroupName" --output text

# Get the most recent log stream
aws logs describe-log-streams --log-group-name /aws/lambda/amazon-stock-tracker --region us-east-1 --order-by LastEventTime --descending --limit 1 --query "logStreams[0].logStreamName" --output text

# List all log streams for the Lambda function
aws logs describe-log-streams --log-group-name /aws/lambda/amazon-stock-tracker --region us-east-1 --order-by LastEventTime --descending --limit 5

# Filter logs for specific content
aws logs filter-log-events --log-group-name /aws/lambda/amazon-stock-tracker --filter-pattern "SNS" --region us-east-1 --limit 10
aws logs filter-log-events --log-group-name /aws/lambda/amazon-stock-tracker --filter-pattern "Message sent" --region us-east-1 --limit 10
```

### EventBridge

```bash
# Describe the EventBridge rule
aws events describe-rule --name DailyAmazonStockCheck --region us-east-1

# List targets for the EventBridge rule
aws events list-targets-by-rule --rule DailyAmazonStockCheck --region us-east-1
```