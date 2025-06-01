import json
import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

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
        
        # You can add code here:
        # - Store the data in a database (e.g., DynamoDB)
        # - Send alerts if price crosses thresholds
        # - Send email notifications with the stock price
        
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
