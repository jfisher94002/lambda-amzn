# 

- Ensure your Lambda function has the necessary permissions to publish to the SNS topic
- Make sure the SNS topic exists in your AWS account
- Replace `us-east-1` with your AWS region
- Replace `123456789012` with your AWS account ID

## Notes

```sh
python test_sns.py --topic-arn "arn:aws:sns:us-east-1:123456789012:amazon-stock-updates" --real-sns
```bash
3. Use the `--real-sns` flag to test with the actual AWS SNS service (requires AWS credentials):

```

python test_sns.py --topic-arn "arn:aws:sns:us-east-1:123456789012:amazon-stock-updates"

```bash
2. Pass the ARN directly to the test script:

```

python test_sns.py
export SNS_TOPIC_ARN=arn:aws:sns:us-east-1:123456789012:amazon-stock-updates

```bash
1. Set the environment variable before running the test script:

When testing locally, you can:

## Option 4: Testing Locally

When you run the `deploy.sh` script, it will prompt you to set up SNS notifications and will automatically set this environment variable for you.

## Option 3: Using the Deploy Script

```

--environment "Variables={SNS_TOPIC_ARN=arn:aws:sns:us-east-1:123456789012:amazon-stock-updates}"
--function-name amazon-stock-tracker   
aws lambda update-function-configuration \

```bash

## Option 2: Using the AWS CLI

6. Click "Save"
   - Value: Your SNS topic ARN (e.g., `arn:aws:sns:us-east-1:123456789012:amazon-stock-updates`)
   - Key: `SNS_TOPIC_ARN`
5. Click "Edit" and add a new variable:
4. Go to the Configuration tab and click on Environment variables
3. Select your `amazon-stock-tracker` function
2. Navigate to the Lambda service
1. Sign in to the [AWS Management Console](https://console.aws.amazon.com/)

## Option 1: Using the AWS Console

To set the SNS Topic ARN for the Amazon Stock Tracker Lambda function, you have several options:
 Setting SNS Topic ARN Environment Variable
```