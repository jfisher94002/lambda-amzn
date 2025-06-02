import json
import logging
import requests
import boto3
from bs4 import BeautifulSoup
from datetime import datetime
from botocore.exceptions import ClientError

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize SNS client
sns = boto3.client('sns')

def get_sns_topic_arn(context):
    """
    Get SNS topic ARN from environment variables or use a default based on region.
    
    Args:
        context: The Lambda context object that contains runtime information
        
    Returns:
        str: The SNS topic ARN or None if not configured
    """
    import os
    
    # Try to get the SNS topic ARN from environment variables
    sns_topic_arn = os.environ.get('SNS_TOPIC_ARN')
    
    if sns_topic_arn:
        return sns_topic_arn
    
    # If environment variable not set, try to construct a default ARN
    logger.warning("SNS_TOPIC_ARN environment variable not set")
    
    # Construct a default ARN if you have a known topic
    # Format: arn:aws:sns:<region>:<account-id>:<topic-name>
    try:
        region = context.invoked_function_arn.split(":")[3]
        account_id = context.invoked_function_arn.split(":")[4]
        topic_name = "amazon-stock-updates"
        default_arn = f"arn:aws:sns:{region}:{account_id}:{topic_name}"
        logger.info(f"Constructed default SNS Topic ARN: {default_arn}")
        return default_arn
    except (IndexError, AttributeError) as e:
        logger.error(f"Could not construct default SNS Topic ARN: {e}")
    
    return None

def lambda_handler(event, context):
    """
    AWS Lambda function that queries Amazon (AMZN) stock value daily using Google Finance data
    
    Args:
        event: The event dict that contains the parameters sent when the function is invoked
        context: The context object that contains runtime information
        
    Returns:
        None
    """
    logger.info('Amazon stock tracker lambda function executed!')
    
    try:
        symbol = 'AMZN'  # Amazon stock symbol
        url = f'https://www.google.com/finance/quote/{symbol}:NASDAQ'
        
        logger.info(f'Fetching stock data from Google Finance: {url}')
        response = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract the current price (Google Finance structure might change over time)
        price_element = soup.select_one('div[data-last-price]')
        
        if price_element:
            stock_price = price_element.get('data-last-price') or price_element.text.strip()
        else:
            # Try an alternative selector if the first one doesn't work
            price_div = soup.select_one('.YMlKec.fxKbKc')
            if price_div:
                stock_price = price_div.text.strip()
            else:
                raise Exception('Could not extract stock price from Google Finance')
        
        # Get the current date for the data point
        today = datetime.now()
        stock_date = today.strftime('%Y-%m-%d')  # YYYY-MM-DD format
        
        logger.info(f'Amazon (AMZN) stock price on {stock_date}: ${stock_price}')
        
        # Create message for SNS
        subject = f"Amazon Stock Update - {stock_date}"
        message = (
            f"Amazon (AMZN) Stock Price Update\n\n"
            f"Date: {stock_date}\n"
            f"Current Price: ${stock_price}\n\n"
            f"This is an automated message from your AWS Lambda function."
        )
        
        # Get SNS topic ARN from environment variable or use parameter
        topic_arn = get_sns_topic_arn(context)
        
        # Send message to SNS topic
        try:
            if topic_arn:
                logger.info(f"Attempting to publish to SNS topic: {topic_arn}")
                response = sns.publish(
                    TopicArn=topic_arn,
                    Message=message,
                    Subject=subject
                )
                logger.info(f"Message sent to SNS topic: {response['MessageId']}")
            else:
                logger.warning("SNS topic ARN not configured - notification not sent")
        except Exception as e:
            # Catch all exceptions, not just ClientError
            logger.error(f"Failed to send SNS notification: {str(e)}")
            # Continue execution even if SNS fails
        
        # Log success message
        logger.info('Amazon stock price retrieved successfully', extra={
            'symbol': 'AMZN',
            'price': stock_price,
            'date': stock_date
        })
        
        return  # Lambda function doesn't need to return anything for scheduled events
        
    except Exception as error:
        logger.error(f'Error fetching Amazon stock data: {error}')
        # Rethrow the error so AWS Lambda can handle it
        raise
