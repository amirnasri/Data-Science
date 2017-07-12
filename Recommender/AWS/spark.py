#!/usr/bin/python 
import csv
import os
from subprocess import Popen, PIPE
import subprocess
import sys
import argparse

class shell_process:
    def __init__(self):
        if not hasattr(self, 'p'):
            self.p = Popen(['/bin/sh'], stdin=PIPE)

    def run(self, command):
        if not command:
            return
        if command[-1] != '\n':
            command = command + '\n'
        self.p.stdin.write(command)


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "python-driver",
        help="Python driver program to run on the master.")
    parser.add_argument(
        "--copy-master", action="store_true",
        help="Whether to copy 'copy-dir' to the master.")
    parser.add_argument(
        "--copy-dir", default="work",
        help="Local directory to be copied to the master (default: '%(default)s').")
    parser.add_argument(
        "-u", "--user", default="root",
        help="SSH user to use for logging onto the master (default: '%(default)s').")
    parser.add_argument(
        "-i", "--identity-file",
        help="SSH private key file to user for logging into instances.")
    parser.add_argument(
        "--ec2-access-key", default="accessKeys.csv",
        help="AWS ec2 access key file (default: '%(default)s').")
    parser.add_argument(
        "-s", "--slaves", type = int, default = 1,
        help = "Number of slaves to launch (default: %(default)s)")
    parser.add_argument(
        "-k", "--key-pair",
        help="Key pair to use on instances")
    parser.add_argument(
        "-t", "--instance-type", default="t2.micro",
        help="Type of instance to launch (default: %(default)s).")
    parser.add_argument(
        "-r", "--region", default="us-east-1",
        help="EC2 region used to launch instances in, or to find them in (default: %(default)s")
    parser.add_argument(
        "-z", "--zone", default="",
        help="Availability zone to launch instances in, or 'all' to spread " +
             "slaves across multiple (an additional $0.01/Gb for bandwidth" +
             "between zones applies) (default: a single zone chosen at random)")
    parser.add_argument(
        "-a", "--ami",
        help="Amazon Machine Image ID to use")
    return parser.parse_args()


def main():
    args = arg_parse()
    with open(args.ec2_access_key) as f:
        try:
            keys = list(csv.reader(f))[1]
            ACCESS_KEY_ID = keys[0]
            AWS_SECRET_ACCESS_KEY = keys[1]
            #print("|%s|%s|" % (ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY))

        except IOError:
            print("Failed to read access keys from file.")
            os.exit(1)

    os.environ['AWS_ACCESS_KEY_ID'] = ACCESS_KEY_ID
    os.environ['AWS_SECRET_ACCESS_KEY'] = AWS_SECRET_ACCESS_KEY
    shell = shell_process()
    #shell.run('env | grep -i aws')

    #script_dir = "~/git/spark-ec2/"
    script_dir = "."
    key_file = os.path.abspath("spark.pem")
    cluster_name = 'spark_cluster'

    opts = dict()
    opts['slaves'] = 1
    opts['region'] = 'us-east-1'
    opts['key-pair'] = 'spark'
    opts['identity-file'] = key_file
    opts['ami'] = 'ami-52d5d044'
    opts['ebs-vol-num'] = 1
    opts['ebs-vol-size'] = 1
    opts['instance-type'] = 't2.micro'
    opts['user'] = 'ubuntu'
    action = sys.argv[1]

    def run_spark_ec2(script_path, action, culster_name, opts):
        command = "{script} %s %s %s".format(
                            script=script_path,
                            , command_optscluster_name)
        print("Running spark-ec2 script %s\n" % command)
        try:
            subprocess.check_call(command.split(), shell=False)
        except subprocess.CalledProcessError as e:
            print("script failed with exit status %d\n", e.returncode)

    shell.run("chmod 600 %s" % key_file)
    #command = "%s -i %s -k %s -t %s -s %s launch %s" % (os.path.join(script_dir, "spark-ec2"), key_file, key_file_name, instance_type, 2, aim)
    command_opts = ' '.join(['--%s=%s'%(k, v) for k, v in opts.items()])

    run_spark_ec2(
        script_path=os.path.expanduser(os.path.join(script_dir, "spark-ec2")),
        culster_name=cluster_name)

    command = "%s %s %s %s" % (os.path.expanduser(os.path.join(script_dir, "spark-ec2")), command_opts, action, cluster_name)
    print("Running spark-ec2 script %s\n" % command)
    #shell.run(command)
    try:
        subprocess.check_call(command.split(), shell=False)
    except subprocess.CalledProcessError as e:
        print("script failed with exit status %d\n", e.returncode)

    with open("master_slave", "r") as f:
        master_address = f.readline().strip()

    if not master_address:
        print("Failed to obtain master address.")
        sys.exit(1)


    """
    1) copy work directory to master
        - work directory contains python script and required data
    2) copy work directory on the master to hdfs so it is accessible from all slaves

    3) run spark submit on the master
    """

    ssh_args = ['-o', 'StrictHostKeyChecking=no']
    ssh_args += ['-o', 'UserKnownHostsFile=/dev/null']
    ssh_args += ['-i', key_file]
    ssh_command = "ssh %s" % " ".join(ssh_args)
    python_script = 'Recommender_spark.py'
    remote_command = "cd work; ~/spark/bin/spark-submit --master spark://%s:7077 %s" %(master_address, python_script)
    ssh_command_args = "%s ubuntu@%s '%s'" % (ssh_command, master_address, remote_command)
    print ssh_command_args
    os.system(ssh_command_args)

    """
    ../../../spark-ec2/spark-ec2 --slaves=2 --region=us-east-1  --key-pair=spark --identity-file=spark.pem -a ami-52d5d044
    launch spark_cluster -t t2.micro --ebs-vol-num=1 --ebs-vol-size=1


    scp -i AWS/spark.pem -r work ubuntu@ec2-34-201-14-166.compute-1.amazonaws.com:

    """


if __name__ == '__main__':
    main()