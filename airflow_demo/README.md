# Simple Airflow Demo 
This Airflow is just for demo purpose to help demonstrate Producation ETL design. One [Apache Airflow](https://airflow.apache.org) simple data pipeline (weather_bag) to fetch data from [Weather API](https://openweathermap.org/api), transform the data into a tabular structure (.csv), and store the transformed data on [Amazon S3](https://aws.amazon.com/s3/).

## Prerequisites
1. [Python 3.6](https://www.python.org/) and [Virtualenv](https://virtualenv.pypa.io/en/latest/)
2. [Docker](https://docs.docker.com/install/) and [Docker Compose](https://docs.docker.com/compose/install/)
3. A free [Weather API](https://openweathermap.org/api). The key is included in codes for demo purpose but recommended to register a new one to avoid reach usage limit. In production the key should be configured into environment variables.
4. A free [AWS Account](https://aws.amazon.com/s3/). The S3 access key is removed in codes for demo purpose but in production the key should be configured into environment variables.
    * One bucket is created to store transformed csv. 
    * **storeweather**: for data pipeline - weather_dag: Store daily weather data for Morse Store.

## Quickstart
1. Run `source env/bin/activate` to activate virtual environment
2. Run `make init` to download project dependencies.
3. Run `make test` to make sure all tests (No testing yet for this simple data pipeline) are passing.
4. Run `make run` with docker running to bring up airflow.
    * The Airflow UI/Admin Console should now be visible on [http://localhost:8080](http://localhost:8080).
    * There is one DAG named `weather_dag`
    * BAG is scheduled to run once a day at midnight

## Pipelines Overview
The pipelines are designed to use as few operations as possible to achieve the purpose. The file structures are designed as following: 

			├── <Store Name>
			│   ├── <pipeline_execution_date>_weather.csv
			│   ├── <pipeline_execution_date>_weather.csv
	
			.....


**Data Pipeline 1: weather_bag**

![alt text](https://github.com/xinlutu2/Data_Engineer_Sales_Weather/blob/master/Airflow_demo/images/bag1.png 'BAGs layout')

The result .csv files are uploaded to S3 in **storeweather** as following:

![alt text](https://github.com/xinlutu2/Data_Engineer_Sales_Weather/blob/master/Airflow_demo/images//bucket1.png 'bucket layout')

![alt text](https://github.com/xinlutu2/Data_Engineer_Sales_Weather/blob/master/Airflow_demo/images//bucket_csv.png 'csv layout')
