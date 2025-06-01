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
    
    echo "Deployment completed!"
else
    echo "Deployment package created but not deployed to AWS."
fi
