#!/usr/bin/env bash

#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# These variables are automatically filled in by the spark-ec2 script.
export MASTERS="ec2-34-203-29-101.compute-1.amazonaws.com"
export SLAVES="ec2-34-229-186-206.compute-1.amazonaws.com"
export HDFS_DATA_DIRS="/mnt/ephemeral-hdfs/data"
export MAPRED_LOCAL_DIRS="/mnt/hadoop/mrlocal"
export SPARK_LOCAL_DIRS="/mnt/spark"
export MODULES="spark
ephemeral-hdfs
persistent-hdfs
spark-standalone
tachyon
rstudio
ganglia"
export SPARK_VERSION="1.6.2"
export TACHYON_VERSION="0.8.2"
export HADOOP_MAJOR_VERSION="1"
export SWAP_MB="1024"
export SPARK_WORKER_INSTANCES="1"
export SPARK_MASTER_OPTS=""
export AWS_ACCESS_KEY_ID=""
export AWS_SECRET_ACCESS_KEY=""
