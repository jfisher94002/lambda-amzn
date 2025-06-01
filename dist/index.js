"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.handler = void 0;
const axios_1 = __importDefault(require("axios"));
const cheerio = __importStar(require("cheerio"));
/**
 * Lambda function that queries Amazon (AMZN) stock value daily using Google Finance data
 */
const handler = async (event, context) => {
    console.log('Amazon stock tracker lambda function executed!');
    try {
        const symbol = 'AMZN'; // Amazon stock symbol
        const url = `https://www.google.com/finance/quote/${symbol}:NASDAQ`;
        console.log(`Fetching stock data from Google Finance: ${url}`);
        const response = await axios_1.default.get(url);
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
    }
    catch (error) {
        console.error('Error fetching Amazon stock data:', error);
        // Rethrow the error so AWS Lambda can handle it
        throw error;
    }
};
exports.handler = handler;
//# sourceMappingURL=index.js.map