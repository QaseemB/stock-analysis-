FROM apache/airflow:2.8.1-python3.10

# Allow root operations
# ARG AIRFLOW_UID=50000
USER root

WORKDIR /opt/airflow


COPY requirements.txt .


ENV PYTHONPATH=/opt/stock_analysis

USER airflow
