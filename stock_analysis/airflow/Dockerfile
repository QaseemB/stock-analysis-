FROM apache/airflow:2.8.1

USER root
WORKDIR /stock_analysis/airflow

# Install your custom Python dependencies
COPY ../../requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Optional: set the project root for your codebase
ENV PYTHONPATH=/opt/stock_analysis

USER airflow