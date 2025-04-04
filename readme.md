# Stock Market Analysis Dashboard

## Overview

The **Stock Market Analysis System**  is a data engineering platform designed to capture, analyze, and present over two decades of stock market data. This robust system utilizes Node.js to fetch real-time stock data, storing the raw input in MongoDB for high-performance data retrieval.

Key System Capabilities:

Comprehensive Data Fetching: Utilizes Node.js to efficiently gather stock data, ensuring comprehensive coverage and timeliness.
Dynamic Data Processing: Ingests raw stock data into a Python-based analysis framework where it undergoes rigorous processing. Utilizing sophisticated algorithms, the system calculates key financial indicators such as Bollinger Bands, Moving Averages, Trading Volume, and MACD to ensure accuracy and relevance.
Advanced Data Storage: Processed data is meticulously stored in PostgreSQL, providing a structured and scalable solution for handling complex data sets.
Data Visualization: Generates a variety of visualization outputs including PDF reports, CSV files for data manipulation, and JPEG images for quick visual references, facilitating diverse analytical needs.
Secure Data Backup: Ensures data integrity and availability with comprehensive backups to Amazon S3, preserving both raw and processed data along with all visual outputs.
Intuitive Dashboard Interface: Data is funneled into a frontend dashboard that provides easy-to-digest summaries and visual data representations, designed for optimal user experience.
Scalability and Performance: Currently, the system manages an extensive dataset comprising over 150 stocks spanning more than 20 years, demonstrating remarkable scalability and robust data handling capabilities.


Ideal for Financial Analysts and Data Scientists: This system is tailored for financial analysts, data scientists, and market enthusiasts who require reliable, processed data for detailed market analysis and decision-making processes

---

## Features

- **Stock Data Fetching**: Fetches historical stock data (up to 20 years) for multiple stock symbols using a Node.js backend.
- **Data Storage**: Data is stored and managed in **MongoDB**.
- **Data Analysis**: Python and **Flask** are used to analyze stock data, calculate technical indicators, and generate charts.
- **Interactive Graphs**: Dynamic visualizations of stock performance with:
  - Moving Averages (3-month, 6-month)
  - Bollinger Bands
  - Trading Volume
  - MACD (Moving Average Convergence Divergence)
- **Stock Summary**: Displays summary statistics such as:
  - Latest Open/Close prices
  - Monthly return
  - Moving averages for short-term and long-term trends
- **Responsive Dashboard**: The dashboard adapts to different screen sizes for a smooth user experience.

---

## Tech Stack

- **Frontend**: React, Plotly.js, TailwindCSS
- **Backend**: Node.js, Express.js
- **Data Analysis**: Python, Flask (for data processing and generating charts)
- **Data Storage**: MongoDB, PostgreSQL, Amazon S3 (for backups)
- **Visualizations**: Plotly for interactive graphs, static images generated via Python/Flask (Bollinger Bands, Moving Average, MACD), and PDF/CSV reports generated via Python/Flask

---

## Getting Started

### Prerequisites

Ensure you have the following installed:

- Node.js (v14.x or higher)
- MongoDB
- Python 3.x
- pip (for Python package management)
- Flask (Python web framework)

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/QaseemB/stock-market-analysis-dashboard.git
   cd stock-market-analysis-dashboard

2. **Install dependencies**:
    for frontend
     ```bash
     cd client
    npm install

    for backend
    ```bash
    cd Server
    npm install

3. setup python enviroment:
    ```bash
    install the necssary python libraries:
    pip install -r requirements.txt

4. run the backend
    start the flask server (ensure MongoDb is running locally or through a cloud service):
    bash
    python app.py

5. run the frontend 
    in the client directory:
    bash
    npm start

    ## usage

    Once the application is running, navigate to <http://localhost:3000> in your browser.
    Select a stock symbol from the dropdown to see its historical performance, including moving averages, Bollinger bands, and trading volume.
    View the interactive charts and read the stock summary to gain insights into the stock’s current performance.

    ## Future Development
    Scalability: Extend the project to fetch and analyze data for hundreds of stocks over multiple decades.
    ETL Pipeline: Create more advanced ETL pipelines to handle larger datasets efficiently.
    Cloud Deployment: Deploy the application using cloud services (AWS, GCP, Azure) for better performance and scalability.
    Automated Alerts: Implement features to send alerts when stocks reach certain thresholds (e.g., price, volume).

    ## license
    MIT License
    You can copy this content into a file named **`README.md`** in your project's root directory. This will provide a clear and professional overview of your project for others to easily understand and contribute to it.


