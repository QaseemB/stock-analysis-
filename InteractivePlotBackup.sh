#!/bin/bash

# Load environment variables
source ./.env

# Variables from .env
DB_NAME=$SQL_NAME
DB_USER=$SQL_USER
BUCKET_NAME=$S3_BUCKET


TABLE_NAME="stock_visualizations"
S3_DIR="interactive_plots"

# Fetch data from PostgreSQL and save each row as a JSON file
psql -U $DB_USER -d $DB_NAME -t -A -F "|" -c "SELECT symbol, interactive_plot FROM $TABLE_NAME;" | while IFS="|" read -r symbol json_data

do
    if [ -n "$symbol" ] && [ -n "$json_data" ]; then
        # Upload JSON directly to S3 using echo + aws s3
        echo "$json_data" | aws s3 cp - "s3://$BUCKET_NAME/$S3_DIR/$symbol.json" --content-type "application/json"
        echo "✅ Uploaded $symbol.json to S3"
    fi
done

echo "✅ All JSON files uploaded successfully!"