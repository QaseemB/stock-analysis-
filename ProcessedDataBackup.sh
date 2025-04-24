#!/bin/bash

# Load environment variables
source ./.env

# Variables from .env
DB_NAME=$SQL_NAME
BUCKET_NAME=$S3_BUCKET
S3_DIR="processed-data"

# Define backup filename
BACKUP_FILE="processedDataBackup_$(date +%Y-%m-%d_%H%M%S).sql"


# Create a backup
pg_dump -U $SQL_USER -h $SQL_HOST $SQL_NAME > $BACKUP_FILE


# Compress the backup
# gzip $BACKUP_FILE

# Upload to S3
aws s3 cp "$BACKUP_FILE" s3://$BUCKET_NAME/$S3_DIR/
echo "Backup completed successfully and uploaded to S3"