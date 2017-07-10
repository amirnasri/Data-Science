import csv
import os
from subprocess import Popen, PIPE

class shell_process:
    def __init__(self):
        if not hasattr(self, 'p'):
            print("Running shell process")
            self.p = Popen(['/bin/sh'], stdin=PIPE)

    def run(self, command):
        if not command:
            return
        if command[-1] != '\n':
            command = command + '\n'
        self.p.stdin.write(command)


with open('accessKeys.csv') as f:
    try:
        keys = list(csv.reader(f))[1]
        ACCESS_KEY_ID = keys[0]
        AWS_SECRET_ACCESS_KEY = keys[1]
        print("|%s|%s|" % (ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY))
            
    except IOError:
        print("Failed to read access keys from file.")
        os.exit(1)


os.environ['AWS_ACCESS_KEY_ID'] = ACCESS_KEY_ID
os.environ['AWS_SECRET_ACCESS_KEY'] = AWS_SECRET_ACCESS_KEY
#os.system("export AWS_ACCESS_KEY_ID=%s" % ACCESS_KEY_ID)
#os.system("export AWS_SECRET_ACCESS_KEY=%s" % AWS_SECRET_ACCESS_KEY);
shell = shell_process()
shell.run('env | grep -i aws')

script_dir = "../../../training-scripts/"
key_file = os.path.abspath("spark.pem")
key_file_name = "spark"
instance_type = "t1.micro"
n_slaves = 2
aim = "amplab-training"

shell.run("chmod 600 %s" % key_file)
command = "%s -i %s -k %s -t %s -s %s launch %s" % (os.path.join(script_dir, "spark-ec2"), key_file, key_file_name, instance_type, 2, aim)
print("Running command %s" % command)
shell.run(command)



"""
../../../spark-ec2/spark-ec2 --slaves=2 --region=us-east-1  --key-pair=spark --identity-file=spark.pem -a ami-52d5d044 
launch spark_cluster -t t2.micro --ebs-vol-num=1 --ebs-vol-size=1


scp -i AWS/spark.pem -r work ubuntu@ec2-34-201-14-166.compute-1.amazonaws.com:

"""
