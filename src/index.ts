import { ScheduledEvent, Context, ScheduledHandler } from 'aws-lambda';
import axios from 'axios';
import * as cheerio from 'cheerio';

/**
 * Lambda function that queries Amazon (AMZN) stock value daily using Google Finance data
 */
export const handler: ScheduledHandler = async (event: ScheduledEvent, context: Context) => {
  console.log('Amazon stock tracker lambda function executed!');
  
  try {
    const symbol = 'AMZN'; // Amazon stock symbol
    const url = `https://www.google.com/finance/quote/${symbol}:NASDAQ`;
    
    console.log(`Fetching stock data from Google Finance: ${url}`);
    const response = await axios.get(url);
    
    if (response.status !== 200) {
      throw new Error(`Failed to fetch data: HTTP status ${response.status}`);
    }
    
    const html = response.data;
    const $ = cheerio.load(html);
    
    // Extract the current price (Google Finance structure might change over time)
    const priceElement = $('div[data-last-price]');
    const stockPrice = priceElement.attr('data-last-price') || priceElement.text().trim();
    
    if (!stockPrice) {
      throw new Error('Could not extract stock price from Google Finance');
    }
    
    // Get the current date for the data point
    const today = new Date();
    const stockDate = today.toISOString().split('T')[0]; // YYYY-MM-DD format
    
    console.log(`Amazon (AMZN) stock price on ${stockDate}: $${stockPrice}`);
    
    // You can add code here:
    // - Store the data in a database
    // - Send alerts if price crosses thresholds
    // - Send email notifications with the stock price
    
    // Log success message
    console.log('Amazon stock price retrieved successfully', {
      symbol: 'AMZN',
      price: stockPrice,
      date: stockDate
    });
    
    // Lambda function doesn't need to return anything for scheduled events
    return;
  } catch (error) {
    console.error('Error fetching Amazon stock data:', error);
    
    // Rethrow the error so AWS Lambda can handle it
    throw error;
  }
};
