# Setting up SNS for Amazon Stock Tracker Lambda

This guide will help you set up Amazon SNS (Simple Notification Service) to receive stock price updates from your Lambda function.

## 1. Create an SNS Topic

### Using the AWS Console:

1. Sign in to the [AWS Management Console](https://console.aws.amazon.com/)
2. Navigate to the SNS service
3. Click on "Topics" in the left sidebar
4. Click "Create topic"
5. Choose "Standard" type
6. Enter a name like "amazon-stock-updates"
7. Click "Create topic"
8. Note down the Topic ARN (it looks like: `arn:aws:sns:us-east-1:123456789012:amazon-stock-updates`)

```bash
aws sns create-topic --name amazon-stock-updates
```

## 2. Subscribe to the SNS Topic

### For Email Notifications:

1. On the topic details page, click "Create subscription"
2. Choose "Email" as the protocol
3. Enter your email address
4. Click "Create subscription"
5. Confirm the subscription by clicking the link in the email you receive

### Using the AWS CLI:

```bash
aws sns subscribe \
  --topic-arn arn:aws:sns:REGION:ACCOUNT_ID:amazon-stock-updates \
  --protocol email \
  --notification-endpoint your-email@example.com
```

## 3. Set Environment Variables for Lambda Function

### Using the AWS Console:

1. Navigate to Lambda service
2. Select your `amazon-stock-tracker` function
3. Go to the "Configuration" tab
4. Select "Environment variables"
5. Click "Edit"
6. Add a new variable:
   - Key: `SNS_TOPIC_ARN`
   - Value: Your SNS topic ARN (e.g., `arn:aws:sns:us-east-1:123456789012:amazon-stock-updates`)
7. Click "Save"

### Using the AWS CLI:

```bash
aws lambda update-function-configuration \
  --function-name amazon-stock-tracker \
  --environment "Variables={SNS_TOPIC_ARN=arn:aws:sns:REGION:ACCOUNT_ID:amazon-stock-updates}"
```

For a more restrictive policy (recommended for production), create a custom policy:

```bash
cat > sns-policy.json << EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "sns:Publish"
      ],
      "Resource": "arn:aws:sns:REGION:ACCOUNT_ID:amazon-stock-updates"
    }
  ]
}
EOF

aws iam create-policy \
  --policy-name lambda-sns-publish-policy \
  --policy-document file://sns-policy.json

aws iam attach-role-policy \
  --role-name lambda-stock-tracker-role \
  --policy-arn arn:aws:iam::ACCOUNT_ID:policy/lambda-sns-publish-policy
```

```bash
aws iam attach-role-policy \
  --role-name lambda-stock-tracker-role \
  --policy-arn arn:aws:iam::aws:policy/AmazonSNSFullAccess
```

## 4. Update Lambda IAM Role Permissions

Add SNS permissions to your Lambda execution role:

### Using the AWS Console:

1. Navigate to the IAM console
2. Select "Roles" from the left sidebar
3. Find and click on your Lambda execution role
4. Click "Add permissions" and then "Attach policies"
5. Search for and select "AmazonSNSFullAccess" (or create a more restrictive custom policy)
6. Click "Add permissions"

### Using the AWS CLI:

## 5. Test the Setup

1. Deploy your updated Lambda function
2. Invoke it manually or wait for the scheduled execution
3. Check your email for the stock price notification

## Troubleshooting

- If you don't receive notifications, check CloudWatch Logs for your Lambda function
- Ensure your SNS topic ARN is correctly set in the environment variables
- Verify your IAM role has the correct permissions to publish to SNS
- Check if you've confirmed the subscription to the SNS topic

aws sns create-topic --name amazon-stock-updates

```bash


8. Note down the Topic ARN (it looks like: `arn:aws:sns:us-east-1:123456789012:amazon-stock-updates`)
7. Click "Create topic"
6. Enter a name like "amazon-stock-updates"
5. Choose "Standard" type
4. Click "Create topic"
3. Click on "Topics" in the left sidebar
2. Navigate to the SNS service
1. Sign in to the [AWS Management Console](https://console.aws.amazon.com/)


## 1. Create an SNS Topic

This guide will help you set up Amazon SNS (Simple Notification Service) to receive stock price updates from your Lambda function.
 Setting up SNS for Amazon Stock Tracker Lambda
```