import os
import subprocess

key_file = "spark_emr.pem"
key_name = "spark_emr"

#os.environ['AWS_ACCESS_KEY_ID'] = ACCESS_KEY_ID
#os.environ['AWS_SECRET_ACCESS_KEY'] = AWS_SECRET_ACCESS_KEY
os.system("aws ec2 create-key-pair --key-name %s --query 'KeyMaterial' --output text > %s" % (key_name, key_file))
os.system("chmod 600 %s" % key_file)


CLUSTER_ID = subprocess.check_output("aws emr create-cluster --name 'Spark cluster' \
--release-label emr-4.1.0 --applications Name=Spark --ec2-attributes KeyName=%s \
--instance-type m1.small --instance-count 2 --use-default-roles \
--query 'ClusterId' --output text" % (key_name, ), shell=True)

print("created cluster: CLUSTER_ID=%s" % CLUSTER_ID)
os.environ['CLUSTER_ID'] = CLUSTER_ID

cluster_status = subprocess.check_output("aws emr describe-cluster --cluster-id $CLUSTER_ID --query 'Cluster.Status.State' --output text", shell=True)
domain_name = subprocess.check_output("aws emr describe-cluster --cluster-id $CLUSTER_ID \
--query 'Cluster.MainPublicDnsName' --output text", shell=True)

print("cluster domain-name=%s status=%s" % (domain_name, cluster_status))


"""

script_dir = "../../training-scripts/"
key_file = os.path.abspath("spark.pem")
key_file_name = "spark"
instance_type = "t1.micro"
n_subordinates = 2
aim = "amplab-training"

os.system("chmod 600 %s" % key_file)
command = "%s -i %s -k %s -t %s -s %s launch %s" % (os.path.join(script_dir, "spark-ec2"), key_file, key_file_name, instance_type, 2, aim)
print("Running command %s" % command)
os.system(command)
"""
