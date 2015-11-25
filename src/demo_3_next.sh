#!/usr/bin/env bash

WorkDir=/ZTE_Demo
script_path=/root/ZMA_Stage_1/src



hadoop fs -rmr ${WorkDir}
rm -r ${WorkDir}/mba/*
cd /app/model0/data_3/
/app/MobileBehaviorAnalysis-1.0.0/bin/mba train

mkdir -p ${WorkDir}/mba/sample_3/rec
hadoop fs -get ${WorkDir}/sample_3/rec/miracle_rec_list/ ${WorkDir}/mba/sample_3/rec
hadoop fs -get ${WorkDir}/sample_3/rec/miracle_ratings/ ${WorkDir}/mba/sample_3/rec
hadoop fs -get ${WorkDir}/sample_3/rec/miracle_rec/ ${WorkDir}/mba/sample_3/rec
hadoop fs -rmr ${WorkDir}

cd /app/model0/data_next/
/app/MobileBehaviorAnalysis-1.0.0/bin/mba train

mkdir -p ${WorkDir}/mba/sample_next/rec
hadoop fs -get ${WorkDir}/sample_next/rec/miracle_rec/ ${WorkDir}/mba/sample_next/rec

python3 ${script_path}/Data_Preprocess/test_others.py
python3 ${script_path}/Data_Preprocess/test_RA.py

mkdir -p ${WorkDir}/mba/sample_next/fcm
hadoop fs -get ${WorkDir}/sample_next/fcm/ ${WorkDir}/mba/sample_next/fcm

python3 ${script_path}/Data_Preprocess/test_V.py






