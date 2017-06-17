import os

with open('access') as f:
    try:
        ACCESS_KEY_ID = f.readline()
        AWS_SECRET_ACCESS_KEY = f.readline()
        if ACCESS_KEY_ID[-1] == '\n':
            ACCESS_KEY_ID = ACCESS_KEY_ID[:-1]
        if AWS_SECRET_ACCESS_KEY[-1] == '\n':
            AWS_SECRET_ACCESS_KEY = AWS_SECRET_ACCESS_KEY[:-1]
            
    except IOError:
        print("Failed to read access keys from file.")
        os.exit(1)

os.environ['AWS_ACCESS_KEY_ID'] = ACCESS_KEY_ID
os.environ['AWS_SECRET_ACCESS_KEY'] = AWS_SECRET_ACCESS_KEY
#os.system("export AWS_ACCESS_KEY_ID=%s" % ACCESS_KEY_ID)
#os.system("export AWS_SECRET_ACCESS_KEY=%s" % AWS_SECRET_ACCESS_KEY);

script_dir = "../../training-scripts/"
key_file = os.path.abspath("spark.pem")
key_file_name = "spark"
instance_type = "t1.micro"
n_slaves = 2
aim = "amplab-training"

os.system("chmod 600 %s" % key_file)
command = "%s -i %s -k %s -t %s -s %s launch %s" % (os.path.join(script_dir, "spark-ec2"), key_file, key_file_name, instance_type, 2, aim)
print("Running command %s" % command)
os.system(command)
