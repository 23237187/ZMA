#!/usr/bin/env bash

WorkDir=/ZTE_Demo/fpg
script_path=/root/ZMA_Stage_1/src

hadoop fs -rmr ${WorkDir}
rm -r ${WorkDir}/mba/*
cd /app/model0/data_3/
/app/MobileBehaviorAnalysis-1.0.0/bin/mba train

mkdir -p ${WorkDir}/mba/sample_3/
hadoop fs -get ${WorkDir}/rules/ ${WorkDir}/mba/sample_3/rules
hadoop fs -rmr ${WorkDir}

cd /app/model0/data_next/
/app/MobileBehaviorAnalysis-1.0.0/bin/mba train

mkdir -p ${WorkDir}/mba/sample_next
hadoop fs -get ${WorkDir}/rules/ ${WorkDir}/mba/sample_next/rules



python3 ${script_path}/Data_Preprocess/test_FPG.py