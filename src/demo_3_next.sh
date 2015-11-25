#!/usr/bin/env bash

script_path=/root/ZMA_Stage_1/src
hdfs_output_path=/home/yang/Data_Test/sample_next
lfs_output_path=/home/yang/Data_Test/mba/sample_3/

hadoop fs -rmr /home
rm -r /home/yang/Data_Test/mba/*
cd /app/model0/data_3/
/app/MobileBehaviorAnalysis-1.0.0/bin/mba train

mkdir -p /home/yang/Data_Test/mba/sample_3/
hadoop fs -get /home/yang/Data_Test/sample_next/miracle_rec_list/ /home/yang/Data_Test/mba/sample_3/
hadoop fs -get /home/yang/Data_Test/sample_next/miracle_ratings/ /home/yang/Data_Test/mba/sample_3/
hadoop fs -get /home/yang/Data_Test/sample_next/miracle_rec/ /home/yang/Data_Test/mba/sample_3/
hadoop fs -rmr /home

cd /app/model0/data_next/
/app/MobileBehaviorAnalysis-1.0.0/bin/mba train

mkdir -p /home/yang/Data_Test/mba/sample_next/
hadoop fs -get /home/yang/Data_Test/sample_next/miracle_rec/ /home/yang/Data_Test/mba/sample_next/

python3 ${script_path}/Data_Preprocess/test_others.py
python3 ${script_path}/Data_Preprocess/test_RA.py






