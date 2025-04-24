import dotenv from 'dotenv';

dotenv.config()

export const config = {
APIKEY: process.env.APIKEY,
APIKEY2: process.env.API_KEY2,
ATLASURI: process.env.ATLAS_URI,
PORT: process.env.PORT,
AWS_ACCESS_KEY_ID: process.env.AWS_ACCESS_KEY_ID,
AWS_SECRET_ACCESS_KEY: process.env.AWS_SECRET_ACCESS_KEY,
S3_REGION: process.env.S3_REGION,
S3_BUCKET: process.env.S3_BUCKET,
BASE_URL :'https://www.alphavantage.co/query',
DB_NAME: process.env.DB_NAME,
DB_Collection: process.env.DB_Raw_Collection,
environment: process.env.NODE_ENV || 'development',
FLASK_API_URL: 'https://stock-analysis-6age.onrender.com'
} 