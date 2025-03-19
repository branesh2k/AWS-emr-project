# 🚀 AWS EMR Spark ETL Project

## 📝 Overview
This project demonstrates how to run a PySpark ETL job on AWS EMR to process NYC Green Taxi data.

## 📌 Workflow
1️⃣ **Data Source**: NYC TLC Green Taxi may2024 data  
2️⃣ **Processing**: ETL job in **PySpark** (running on EMR)  
3️⃣ **Execution**: Cluster created manually via **AWS Console**, and Spark job submitted via **SSH**  
4️⃣ **Logging**: Logs stored in **S3**  

## 📂 Folder Structure
- `script/etl_job.py`: PySpark job
- `docs/`: Data flow diagram
- `logs/README.md`: How to fetch logs from S3

## 🔥 Running the Project
### **1️⃣ Creating EMR Cluster (Manually via AWS Console)**
1. Go to [AWS EMR Console](https://console.aws.amazon.com/elasticmapreduce)
2. Click **"Create Cluster"**, select:
   - Release: **emr-7.8.0**
   - Applications: **Spark**
   - Instances: **1 Master (c5.xlarge), 1 Core (c5.xlarge), 1 (Task c5.xlarge)**
   - S3 Logs: **s3://emr-branesh-project-1/logs/**
3. Wait for the cluster to be **Running**  

### **2️⃣ Connecting to the Cluster via SSH**
```sh
ssh -i keypair.pem hadoop@your-emr-master-node


### **3️⃣ Submitting spark job**
```sh
spark-submit s3://your-bucket/scripts/etl_job.py \
--source_input1 s3://your-bucket/input/green_taxi_trip.csv \
--source_input2 s3://your-bucket/input/trip_type.csv \
--output_location s3://your-bucket/outputs/

