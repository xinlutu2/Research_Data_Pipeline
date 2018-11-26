# Sample Airflow Demo 
This sample Airflow data pipeline is for demo purpose to help demonstrate how to convert ETL python scripts to production data pipeline. One [Apache Airflow](https://airflow.apache.org) data pipeline (research_bag) to fetch research data (articles and journals) from [PLOS Search API](http://api.plos.org/solr/examples) and [DOAJ API](https://doaj.org/api/v1/docs#!/Search/get_api_v1_search_articles_search_query), transform the data into a tabular structure (.csv), and store the transformed data on [Amazon S3](https://aws.amazon.com/s3/).

## Prerequisites
1. [Python 3.6](https://www.python.org/) and [Conda](https://conda.io/docs/)
	* Airflow has not fully compatible with the Python 3.7 so a conda python 3.6 environment has created to running Airflow under Python 3.6
2. [Docker](https://docs.docker.com/install/) and [Docker Compose](https://docs.docker.com/compose/install/)
3. A free [PLOS Search API](http://api.plos.org/solr/examples). The key is included in codes for demo purpose but recommended to register a new one to avoid reach usage limit. In production the key should be configured into environment variables.
4. Create a free [AWS Account](https://aws.amazon.com/s3/) and S3 bucket named **storeresearch**. The S3 access key is removed in codes for confidential purpose.
    * One bucket is created to store transformed csv. 
    * **storeresearchh**: for data pipeline - research_dag: Store daily research data for given keyword.

## Quickstart
1. Under env virtual environment: Run `conda activate test_env` to activate conda Python 3.6 environment
	* The environment should look similar to `(test_env) (env) USC02X47A1JG5J:airflow_demo xinlutu$`
	* Run `conda deactivate test_env` to deactivate conda Python 3.6 environment
	* Run `conda remove -n test_env --all` to delete conda Python 3.6 environment
	* Run `conda create -n test_env python=3.6.3 anaconda ` to create new conda Python 3.6 environment
2. Run `make init` to download project dependencies.
3. Run `make test` to make sure all tests (No testing yet for this sample data pipeline) are passing.
4. Run `make run` with docker running to bring up airflow.
    * The Airflow UI/Admin Console should now be visible on [http://localhost:8080](http://localhost:8080).
    * There is one DAG named `research_dag`
    * BAG is scheduled to run once a day at midnight

## Pipeline Overview
The pipelines are designed to use as few operations as possible to achieve the purpose. The file structures are designed as following: 

			├── <Keyword>
			│   ├── <pipeline_execution_date>_research.csv
			│   ├── <pipeline_execution_date>_research.csv
	
			.....


**Data Pipeline: research_bag**

![alt text](https://github.com/xinlutu2/research_data_pipeline/blob/master/airflow_demo/images/bag1.png 'BAGs layout')

The result .csv files are uploaded to S3 in **storeresearch** as following:

![alt text](https://github.com/xinlutu2/research_data_pipeline/blob/master/airflow_demo/images/bucket1.png 'bucket layout')

![alt text](https://github.com/xinlutu2/research_data_pipeline/blob/master/airflow_demo/images/bucket_csv.png 'csv layout')
