#!/bin/bash
# Script to package and deploy the Lambda function to AWS

# Set variables
FUNCTION_NAME="amazon-stock-tracker"
RUNTIME="python3.9"
HANDLER="lambda_function.lambda_handler"
REGION="us-east-1"  # Change to your AWS region

# Create a temporary directory for packaging
mkdir -p build
rm -rf build/*

echo "Installing dependencies..."
pip install -t build/ -r requirements.txt

echo "Copying function code..."
cp lambda_function.py build/

echo "Creating deployment package..."
cd build && zip -r ../deployment_package.zip . && cd ..

echo "Deployment package created: deployment_package.zip"

# Ask if the user wants to deploy to AWS Lambda
read -p "Do you want to deploy to AWS Lambda? (y/n): " DEPLOY

if [ "$DEPLOY" = "y" ]; then
    # Check if the function already exists
    aws lambda get-function --function-name $FUNCTION_NAME --region $REGION > /dev/null 2>&1
    
    if [ $? -eq 0 ]; then
        echo "Updating existing Lambda function..."
        aws lambda update-function-code \
            --function-name $FUNCTION_NAME \
            --zip-file fileb://deployment_package.zip \
            --region $REGION
    else
        echo "Creating new Lambda function..."
        echo "Please enter your AWS Lambda execution role ARN:"
        read ROLE_ARN
        
        aws lambda create-function \
            --function-name $FUNCTION_NAME \
            --runtime $RUNTIME \
            --handler $HANDLER \
            --zip-file fileb://deployment_package.zip \
            --role $ROLE_ARN \
            --region $REGION
    fi
    
    echo "Do you want to set up a daily schedule for this Lambda function? (y/n): "
    read SCHEDULE
    
    if [ "$SCHEDULE" = "y" ]; then
        RULE_NAME="DailyAmazonStockCheck"
        
        echo "Creating EventBridge rule..."
        aws events put-rule \
            --name $RULE_NAME \
            --schedule-expression "cron(0 16 * * ? *)" \
            --region $REGION
        
        echo "Adding permission for EventBridge to invoke Lambda..."
        aws lambda add-permission \
            --function-name $FUNCTION_NAME \
            --statement-id EventBridgeInvoke \
            --action lambda:InvokeFunction \
            --principal events.amazonaws.com \
            --source-arn $(aws events describe-rule --name $RULE_NAME --region $REGION --query 'Arn' --output text) \
            --region $REGION
        
        echo "Setting Lambda as target for EventBridge rule..."
        aws events put-targets \
            --rule $RULE_NAME \
            --targets Id=1,Arn=$(aws lambda get-function --function-name $FUNCTION_NAME --region $REGION --query 'Configuration.FunctionArn' --output text) \
            --region $REGION
        
        echo "Schedule set up successfully!"
    fi
    
    echo "Do you want to set up SNS notifications for stock updates? (y/n): "
    read SNS
    
    if [ "$SNS" = "y" ]; then
        SNS_TOPIC_NAME="amazon-stock-updates"
        
        echo "Creating SNS topic..."
        SNS_TOPIC_ARN=$(aws sns create-topic --name $SNS_TOPIC_NAME --region $REGION --query 'TopicArn' --output text)
        
        echo "Topic ARN: $SNS_TOPIC_ARN"
        
        echo "Please enter your email address for notifications: "
        read EMAIL
        
        echo "Subscribing $EMAIL to the SNS topic..."
        aws sns subscribe \
            --topic-arn $SNS_TOPIC_ARN \
            --protocol email \
            --notification-endpoint $EMAIL \
            --region $REGION
            
        # Get current environment variables
        echo "Getting current environment variables..."
        ENV_VARS=$(aws lambda get-function-configuration \
            --function-name $FUNCTION_NAME \
            --query "Environment.Variables" \
            --output json \
            --region $REGION 2>/dev/null || echo "{}")
        
        if [ "$ENV_VARS" == "{}" ]; then
            # No existing environment variables
            echo "Setting SNS_TOPIC_ARN environment variable for Lambda function..."
            aws lambda update-function-configuration \
                --function-name $FUNCTION_NAME \
                --environment "Variables={SNS_TOPIC_ARN=$SNS_TOPIC_ARN}" \
                --region $REGION
        else
            # Merge with existing environment variables
            echo "Updating SNS_TOPIC_ARN environment variable for Lambda function..."
            # Add SNS_TOPIC_ARN to existing variables
            UPDATED_ENV_VARS=$(echo $ENV_VARS | jq --arg arn "$SNS_TOPIC_ARN" '. + {"SNS_TOPIC_ARN": $arn}')
            
            # Update the function configuration
            aws lambda update-function-configuration \
                --function-name $FUNCTION_NAME \
                --environment "Variables=$UPDATED_ENV_VARS" \
                --region $REGION
        fi
            
        echo "Adding SNS publish permissions to Lambda role..."
        # Get the role ARN from the Lambda function
        ROLE_ARN=$(aws lambda get-function --function-name $FUNCTION_NAME --region $REGION --query 'Configuration.Role' --output text)
        ROLE_NAME=$(echo $ROLE_ARN | awk -F/ '{print $NF}')
        
        # Create inline policy for the role
        POLICY_DOCUMENT='{
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": "sns:Publish",
                    "Resource": "'$SNS_TOPIC_ARN'"
                }
            ]
        }'
        
        aws iam put-role-policy \
            --role-name $ROLE_NAME \
            --policy-name LambdaSNSPublish \
            --policy-document "$POLICY_DOCUMENT"
            
        echo "SNS setup completed! Please check your email to confirm the subscription."
        echo "After confirming, you'll start receiving stock price notifications."
    fi
    
    echo "Deployment completed!"
else
    echo "Deployment package created but not deployed to AWS."
fi
