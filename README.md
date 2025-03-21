# 🚀 AWS EMR Spark ETL Project

## 📝 Overview
This project demonstrates how to run a PySpark ETL job on AWS EMR to process NYC Green Taxi data.

## 📌 Workflow
1️⃣ **Data Source**: NYC TLC Green Taxi may2024 data  
2️⃣ **Processing**: ETL job in **PySpark** (running on EMR)  
3️⃣ **Execution**: Cluster created manually via **AWS Console**, and Spark job submitted via **SSH**  
4️⃣ **Logging**: Logs stored in **S3** and monitored in **cloudwatch**  

## 📂 Folder Structure
- `input_data` : sample data
- `src/etl_job.py`: PySpark job
- `src/cloudwatch_config` : cloudwatch config file & bootstrap script
- `docs/`: Data flow diagram
- `logs/README.md`: Info about logs

## 🔥 Running the Project
### **1️⃣ Creating EMR Cluster (Manually via AWS Console)**
1. Go to [AWS EMR Console](https://console.aws.amazon.com/elasticmapreduce)
2. Click **"Create Cluster"**, select:
   - Release: **emr-7.8.0**
   - Applications: **Spark**
   - Instances: **1 Master (c5.xlarge), 1 Core (c5.xlarge), 1 (Task c5.xlarge)**
   - (updated to cloudwatch) S3 Logs: **s3://emr-branesh-project-1/logs/**
3. **Bootstrap Actions**:
   - Add a **Bootstrap Script** for installing and configuring the CloudWatch agent during cluster creation.
   - The script will install the CloudWatch agent, download the configuration file from **S3**, and start the agent to collect logs.
4. Wait for the cluster to be **Running**  
#### **Bootstrap Script to Install and Configure CloudWatch Agent**

The following script is uploaded to **S3** and added as a bootstrap action during cluster creation. It installs the CloudWatch agent and configures it to monitor the necessary logs.

```bash
echo "Installing CloudWatch Agent..."
sudo yum install -y amazon-cloudwatch-agent

echo "Creating directory for CloudWatch config..."
sudo mkdir -p /opt/aws/amazon-cloudwatch-agent/etc
sudo chown root:root /opt/aws/amazon-cloudwatch-agent/etc   #Ensure proper ownership
sudo chmod 755 /opt/aws/amazon-cloudwatch-agent/etc  # Set proper permissions

echo "Downloading CloudWatch config from S3..."
sudo aws s3 cp s3://emr-branesh-project-1/cloudwatch/cloudwatch-config.json /opt/aws/amazon-cloudwatch-agent/etc/cloudwatch-config.json

echo "Starting CloudWatch Agent..."
sudo amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -c file:/opt/aws/amazon-cloudwatch-agent/etc/cloudwatch-config.json -s
```  
**The configuration file** *(cloudwatch-config.json)* is stored in S3 and used by the CloudWatch agent to monitor specific logs on the EMR cluster. This configuration collects logs from various services, such as Spark and YARN.

```json
{
  "logs": {
    "logs_collected": {
      "files": {
        "collect_list": [
          {
            "file_path": "/var/log/spark/*.out",
            "log_group_name": "SparkHistoryServerLogs",
            "log_stream_name": "{instance_id}"
          },
          {
            "file_path": "/var/log/hadoop-yarn/hadoop-yarn-resourcemanager*.out",
            "log_group_name": "YARNResourceManagerLogs",
            "log_stream_name": "{instance_id}"
          },
          {
            "file_path": "/mnt/var/log/hadoop/steps/*",
            "log_group_name": "EMRStepLogs",
            "log_stream_name": "{instance_id}"
          }
        ]
      }
    }
  }
}
```

### **2️⃣ Connecting to the Cluster via SSH**
```sh
ssh -i keypair.pem hadoop@your-emr-master-node
```

### **3️⃣ Submitting spark job**
```
spark-submit s3://emr-branesh-project-1/script/etl_job.py \
--source_input1 s3://emr-branesh-project-1/input_datas/green_taxi_trip_may_2024.csv \
--source_input2 s3://emr-branesh-project-1/input_datas/trip_type.csv \
--output_location s3://emr-branesh-project-1/outputs/
```
