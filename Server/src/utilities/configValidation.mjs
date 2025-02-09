import { config } from "./config.mjs"; // Import your config utility

export const validateConfig = () => {
  const requiredVars = [
    "APIKEY", "BASE_URL",'S3_REGION', 
    'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY'
  ];

  const missingVars = requiredVars.filter(key => !config[key]);

  if (missingVars.length > 0) {
    console.error(`Configuration Error: Missing the following environment variables: ${missingVars.join(', ')}`);
    process.exit(1); // Exit the application with an error code
  };

  console.log("Configuration validated successfully!");
};