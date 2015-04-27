#!/usr/bin/env bash
MAHOUT="/app/mahout/bin/mahout"


WORK_DIR=/ZTE_Demo

#python3 /root/PycharmProjects/ZMA/src/Data_Preprocess/test_FCM.py /ZTE_Demo/sample_data /ZTE_Demo/fpg_data

hadoop fs -mkdir /ZTE_Demo
hadoop fs -put /ZTE_demo/ratings_for_als.csv ${WORK_DIR}

$MAHOUT parallelALS --input ${WORK_DIR}/ratings_for_als.csv --output ${WORK_DIR}/als/out \
    --tempDir ${WORK_DIR}/als/tmp --numFeatures 3 --numIterations 10 --lambda 0.065 --numThreadsPerSolver 4

$MAHOUT evaluateFactorization --input ${WORK_DIR}/ratings_for_als.csv  --output ${WORK_DIR}/als/rmse/ \
    --userFeatures ${WORK_DIR}/als/out/U/ --itemFeatures ${WORK_DIR}/als/out/M/ --tempDir ${WORK_DIR}/als/tmp

$MAHOUT seqdumper -i /ZTE_Demo/als/out/userRatings/part-r-00000 -o /ZTE_Demo/ratings

hadoop fs -rmr ${WORK_DIR}



#hadoop fs -rmr ${WORK_DIR}
#python3 /root/PycharmProjects/ZMA/src/test_ClusterResult2ProbabilityResult.py /ZTE_Demo /ZTE_Demo/


