#!/usr/bin/env bash
WORK_DIR=/ZTE_Demo

python3 /root/PycharmProjects/ZMA/src/Data_Preprocess/test_FPG.py /ZTE_Demo/sample_data /ZTE_Demo/fpg_data

hadoop fs -mkdir /ZTE_Demo
hadoop fs -mkdir /ZTE_Demo/fpg_data
hadoop fs -put /ZTE_Demo/fpg_data /ZTE_Demo/fpg_data/transactions.txt

/app/spark/bin/spark-submit \
    --class org.apache.spark.examples.mllib.FPGrowthExample \
    --master yarn-cluster /app/spark/lib/spark-examples-1.3.1-hadoop2.6.0.jar \
    --minSupport 0.0001 \
    --numPartition 2 \
    /ZTE_Demo/fpg_data/transactions.txt

