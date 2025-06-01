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