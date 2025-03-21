echo "Installing CloudWatch Agent..."
sudo yum install -y amazon-cloudwatch-agent

echo "Creating directory for CloudWatch config..."
sudo mkdir -p /opt/aws/amazon-cloudwatch-agent/etc
sudo chown root:root /opt/aws/amazon-cloudwatch-agent/etc  # Ensure proper ownership
sudo chmod 755 /opt/aws/amazon-cloudwatch-agent/etc  # Set proper permissions

echo "Downloading CloudWatch config from S3..."
sudo aws s3 cp s3://emr-branesh-project-1/cloudwatch/cloudwatch-config.json /opt/aws/amazon-cloudwatch-agent/etc/cloudwatch-config.json

echo "Starting CloudWatch Agent..."
sudo amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -c file:/opt/aws/amazon-cloudwatch-agent/etc/cloudwatch-config.json -s
