#!/usr/bin/env bash
WORK_DIR=/ZTE_Demo

python3 /root/ZMA_Stage_1/src/Data_Preprocess/test_FPG.py /ZTE_Demo/sample_data /ZTE_Demo/fpg_data tran_gen

hadoop fs -mkdir /ZTE_Demo
hadoop fs -mkdir /ZTE_Demo/fpg_data
hadoop fs -put /ZTE_Demo/fpg_data /ZTE_Demo/fpg_data/transactions.txt

/app/spark/bin/spark-submit \
    --class org.apache.spark.ZTE_Project.ZTE_fpg_demo \
    --master yarn-cluster /app/spark/lib/FPG.jar \
    --minSupport 0.0001 \
    --numPartition 2 \
    /ZTE_Demo/fpg_data/transactions.txt

hadoop fs -get ${WORK_DIR}/FPG_result ${WORK_DIR}/FPG_result

hadoop fs -rmr ${WORK_DIR}

python3 /root/ZMA_Stage_1/src/Data_Preprocess/test_FPG.py /ZTE_Demo/sample_data /ZTE_Demo/fpg_data rule_gen

echo "FPG Complete"


