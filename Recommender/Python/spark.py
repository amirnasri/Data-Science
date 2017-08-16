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


def arg_parse(*args, **kwargs):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'action',
        choices=('launch', 'destroy', 'start', 'start-spark', 'stop-spark'),
        help='Action to perform on the cluster.')
    parser.add_argument(
        'cluster_name',
        help='Name of the ec2 culster.')
    parser.add_argument(
        'python_driver',
        help='Python driver program to run on the master.')
    parser.add_argument(
        '--remote-spark-home', default='~/spark/',
        help='Directory on the instances where spark is installed (default: \'%(default)s\').')
    parser.add_argument(
        '--copy-master', action='store_true',
        help='Whether to copy \'copy-dir\' to the master.')
    parser.add_argument(
        '--copy-dir', default='work',
        help='Local directory to be copied to the master (default: \'%(default)s\').')
    parser.add_argument(
        '-u', '--user', default='root',
        help='SSH user to use for logging onto the master (default: \'%(default)s\').')
    parser.add_argument(
        '-i', '--identity-file',
        help='SSH private key file to user for logging into instances (default: \'%(default)s\').')
    parser.add_argument(
        '--ec2-access-key', default='accessKeys.csv',
        help='AWS ec2 access key file (default: \'%(default)s\').')
    parser.add_argument(
        '-s', '--slaves', type = int, default = 1,
        help = 'Number of slaves to launch (default: %(default)s)')
    parser.add_argument(
        '-k', '--key-pair',
        default='',
        help='Key pair to use on instances (default: \'%(default)s\').')
    parser.add_argument(
        '-t', '--instance-type', default='t2.micro',
        help='Type of instance to launch (default: %(default)s).')
    parser.add_argument(
        '-r', '--region', default='us-east-1',
        help='EC2 region used to launch instances in, or to find them in (default: %(default)s')
    parser.add_argument(
        '--private-ips', action='store_true', default=False,
        help='Use private IPs for instances rather than public if VPC/subnet ' +
             'requires that.')
    parser.add_argument(
        '-a', '--ami',
        default='ami-52d5d044',
        help='Amazon Machine Image ID to use (default: %(default)s).')
    parser.add_argument(
        '--remote-server', default='amirnasri.ca',
        help='Remote server address where the results are uploaded (default: %(default)s).')
    parser.add_argument(
        '--run-local', action='store_true', default=False,
        help='run driver program in local machine instead of the remote server')
    return parser, parser.parse_args(*args, **kwargs)


def run_ec2_cluster(script_path, args, args_extra):
    command_str = '{script_path} --user={user} ' \
                  '--slaves={slaves} --key-pair={key_pair} --instance-type={instance_type} ' \
                  '{private_ips} ' \
                  '--region={region} --ami={ami} {action} {cluster_name} '

    command = command_str.format(
        script_path=script_path,
        user=args.user,
        identity_file=args.identity_file,
        slaves=args.slaves,
        key_pair=args.key_pair,
        instance_type=args.instance_type,
        private_ips='--private-ips' if args.private_ips else '',
        region=args.region,
        ami=args.ami,
        action=args.action,
        cluster_name=args.cluster_name,
    )
    command += args_extra
    print('Running spark-ec2 script %s\n' % command)

    try:
        subprocess.check_call(command.split(), shell=False)
    except subprocess.CalledProcessError as e:
        print('script failed with exit status %d\n' % e.returncode)
        raise e

def ssh(master, args, remote_command, extra_args=''):
    ssh_args = ['-o', 'StrictHostKeyChecking=no']
    ssh_args.extend(['-o', 'UserKnownHostsFile=/dev/null'])
    ssh_args.extend(['-i', args.identity_file])
    ssh_args.append(extra_args)
    ssh_command = 'ssh -q {args} {user}@{master} \'{remote_command}\''.format(
        args=' '.join(ssh_args),
        user=args.user,
        master=master,
        identity_file=args.identity_file,
        remote_command=remote_command,
    )
    print(ssh_command)
    os.system(ssh_command)


def copy_user_files(instances, args):
    '''Copy local work directory specified in 'copy-dir' option to the master.

    Local work directory should contain python driver program as well as any program
    or data needed by the driver program. After directory is uploaded to master, it is
    copied to hdfs so that it is also available in slaves.

    Note: The directory will be copied to ~/work on the master. If directory already exists
    it will be deleted first.
    '''
    subprocess.check_call(('tar czvf work.tar.gz %s' % args.copy_dir).split())
    for i in instances:
        scp_command = 'scp -o StrictHostKeyChecking=no -i {identity_file} work.tar.gz {user}@{host}:'.format(
            identity_file=args.identity_file,
            user=args.user,
            host=i,
        )
        print(scp_command)
        os.system(scp_command)

        ssh(i, args, 'rm -fr work '
                     '&& tar xzvf work.tar.gz'
                     '&& rm work.tar.gz')

        #ssh(master, args, 'ephemeral-hdfs/bin/hadoop fs -put work /work')


def run_spark(master, args):
    remote_command = 'cd work; {0}/bin/spark-submit --master spark://{1}:7077 {2}'.format(
        args.remote_spark_home, master, args.python_driver
    )
    ssh(master, args, remote_command)


def main():
    parser, args = arg_parse()
    if not args.run_local:
        with open(args.ec2_access_key) as f:
            try:
                keys = list(csv.reader(f))[1]
                ACCESS_KEY_ID = keys[0]
                AWS_SECRET_ACCESS_KEY = keys[1]
    
            except IOError:
                print('Failed to read access keys from file.')
                os.exit(1)
    
        os.environ['AWS_ACCESS_KEY_ID'] = ACCESS_KEY_ID
        os.environ['AWS_SECRET_ACCESS_KEY'] = AWS_SECRET_ACCESS_KEY
        shell = shell_process()
        #shell.run('env | grep -i aws')
    
        script_dir = './AWS'
        key_file = ''
        if args.identity_file:
            shell.run('chmod 600 %s' % args.identity_file)
    
        opts = dict()
        opts['ebs-vol-num'] = 1
        opts['ebs-vol-size'] = 1
        if args.identity_file:
            opts['identity-file'] = args.identity_file
    
        command_opts_extra = ' '.join(['--{0}={1}'.format(k, v) for k, v in opts.items()])
    
        # command = '%s -i %s -k %s -t %s -s %s launch %s' % (os.path.join(script_dir, 'spark-ec2'), key_file, key_file_name, instance_type, 2, aim)
        # command = '%s %s %s %s' % (os.path.expanduser(os.path.join(script_dir, 'spark-ec2')), command_opts, action, cluster_name)
        run_ec2_cluster(
            script_path=os.path.expanduser(os.path.join(script_dir, 'spark-ec2')),
            args=args,
            args_extra=command_opts_extra,
        )
    
    
        '''
        1) copy work directory to master
            - work directory contains python script and required data
        2) copy work directory on the master to hdfs so it is accessible from all slaves
    
        3) run spark submit on the master
        '''
    
        with open('master_slave', 'r') as f:
            master_address = f.readline().strip()
            slave_addresses = [s.strip() for s in f.readlines()]
    
    
        if not master_address:
            print('Failed to obtain master address.')
            sys.exit(1)
    
        if args.copy_master:
            copy_user_files([master_address] + slave_addresses, args)
    
        run_spark(master_address, args)
    
        # Compress the results on the master and upload them to http server.
        ssh(master_address, args, 'cd work/result/'
                                  '&& tar -zcvf result.tar.gz * '
                                  '&&  curl -T result.tar.gz {remote_server}/recommender/upload_data'
                                  '&&  rm result.tar.gz'.format(remote_server=args.remote_server))
        
    else:
        os.chdir('work')
        try:
            subprocess.check_call('spark-submit {script}'.format(script=args.python_driver).split())
        except subprocess.CalledProcessError as e:
            print('script failed with return value=%d' % e.returncode)
            return
        os.system('cd result/'
                        '&& tar -zcvf result.tar.gz * '
                        '&&  curl -T result.tar.gz {remote_server}/recommender/upload_data'
                        .format(remote_server=args.remote_server))

    '''
     ./spark.py start spark_clust Recommender_spark.py --user=ubuntu --key-pair=spark \
     --identity-file=AWS/spark.pem --copy-master --ec2-access-key=AWS/accessKeys.csv \
     --run-local --remote-server localhost:8000

     ./spark.py start spark_clust Recommender_spark.py --user=ubuntu --key-pair=spark \
     --identity-file=AWS/spark.pem --copy-master --ec2-access-key=AWS/accessKeys.csv \
     --remote-server amirnasri.ca

    ../../../spark-ec2/spark-ec2 --slaves=2 --region=us-east-1  --key-pair=spark --identity-file=spark.pem -a ami-52d5d044
    launch spark_cluster -t t2.micro --ebs-vol-num=1 --ebs-vol-size=1


    scp -i AWS/spark.pem -r work ubuntu@ec2-34-201-14-166.compute-1.amazonaws.com:
    ../../../spark-ec2/spark-ec2 --slaves=1 --region=us-east-1  --key-pair=spark --identity-file=AWS/spark.pem -a ami-19474270 launch spark_cluster -t m1.medium --ebs-vol-num=1 --ebs-vol-size=1

    '''


if __name__ == '__main__':
    main()