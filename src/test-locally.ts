// Test file to run the Lambda function locally
import { handler } from './index';
import { Context } from 'aws-lambda';
import { EventBridgeEvent } from 'aws-lambda';

// Create a simplified mock event
const mockEvent = {
  id: "test-event-id",
  "detail-type": "Scheduled Event",
  source: "aws.events",
  time: new Date().toISOString(),
  resources: []
} as any;

// Create a simplified mock context
const mockContext = {
  functionName: "amazon-stock-tracker",
  awsRequestId: "test-request-id",
  getRemainingTimeInMillis: () => 30000,
} as Context;

async function runTest() {
  console.log("Testing Lambda function locally...");
  try {
    await handler(mockEvent as any, mockContext);
    console.log("Lambda function executed successfully");
  } catch (error) {
    console.error("Error executing Lambda function:", error);
  }
}

runTest();
