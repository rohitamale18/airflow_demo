# Airflow Demo
A project to give a demo of basic functionalities within Airflow and how to leverage those. Contents include, 

1. The project contains 3 DAGS. Each DAG is developed with an intent to give a basic idea of the Airflow Operators, Tasks, How to execute those tasks, How to set Upstream and Downstream Task dependencies
2. The DAGS cover simple arithematic operations as well as an example of using spark-submit to submit spark applications on remote cluster

## Installation:

### Development and Deployment:
The project requires Docker to be installed on Host. Deployment can be done using command prompt, 
    /path/to/airflow_demo: docker-compose up -d

This will,
1. Download relevant docker images (if not already present on system)
2. Build 3 Docker containers - Airflow, Spark-Master and Spark-Worker
3. Start all the containers

All the containers will be on a default bridge network.

The Airflow and Spark's web UI can be accessed at localhost:8080 and localhost:9090 respectively.

TODO: Figure out a way to set up a separate dev environment for development with Pycharm.

## Docker Images:
1. This project uses a pre-built Docker image  spydernaz/spark-master for spark cluster. 
2. For Airflow, the standard image  puckel/docker-airflow has been modified in a way such that it has spark dependencies installed.

Setting up of the containers is included in the docker-compose.yml file.

## Airflow S3 Connection:
As of now, the AWS connection is achieved through manually adding a connection for AWS S3 hook through Airflow UI. This, however, needs to be changed for a more secure and automated way
