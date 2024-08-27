# Top Crypto Exchanges Project

## Introduction
The "Top Crypto Exchanges Project" is designed to automate the collection and transformation of data from cryptocurrency exchange APIs. Utilizing Docker for containerization, Airflow for workflow orchestration, and MinIO for scalable storage, the project streamlines data management and integration. Dash and Plotly are employed to build interactive dashboards that provide up-to-date insights from daily data updates.

## Technologies Used
1. Programming Language - Python
2. Data Storage - MinIO (S3-compatible)
3. Workflow Management - Apache Airflow
4. Data Visualization - Dash, Plotly
5. Container Platform - Docker

## Architecture
image here

DAG Tasks:
1. Scrape data from [APIs](https://api.coincap.io/v2/exchanges).
2. Transform and load data to [S3(Minio)](https://min.io/docs/minio/container/index.html).

   
