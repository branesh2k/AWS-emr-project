# 📝 Spark Job Logs

## 📌 Where Logs Are Stored
All logs from the Spark job execution are stored in **Amazon S3**.  
- **Log Path:** `s3://emr-branesh-project-1/logs/`
- **Types of Logs:**
  - `stdout.gz` and `stderr.gz` logs for Spark job execution
  - Application logs for debugging

---

## 🔥 How to Access Logs  
### **List All Logs in S3**
```sh
aws s3 ls s3://emr-branesh-project-1/logs/ --recursive
```

### **Download Logs Locally**
```sh
aws s3 cp s3://emr-branesh-project-1/logs/j-1X718ZYADCHJS/containers/application_1742305176324_0001/container_1742305176324_0001_01_000001/stdout.gz ./logs/
aws s3 cp s3://emr-branesh-project-1/logs/j-1X718ZYADCHJS/containers/application_1742305176324_0001/container_1742305176324_0001_01_000001/stderr.gz ./logs/
```

---

## 🛠️ **Understanding Logs**
- **Spark Driver Logs:** Captures the main application execution.
- **Executor Logs:** Contains task execution details.
- **Error Logs:** If a job fails, check `stderr` for errors.


---
