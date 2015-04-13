#!/usr/bin/env bash
MAHOUT="/app/mahout/bin/mahout"


WORK_DIR=/ZTE_Demo



hadoop fs -mkdir /ZTE_Demo
hadoop fs -put /ZTE_demo/ratings_for_als.csv ${WORK_DIR}

$MAHOUT parallelALS --input ${WORK_DIR}/ratings_for_als.csv --output ${WORK_DIR}/als/out \
    --tempDir ${WORK_DIR}/als/tmp --numFeatures 3 --numIterations 10 --lambda 0.065 --numThreadsPerSolver 4

mahout seqdumper -i /ZTE_Demo/als/out/U/part-m-00000 -o /ZTE_Demo/U

mahout fkmeans \
    -i ${WORK_DIR}/als/out/U/part-m-00000 \
    -c ${WORK_DIR}/init_clusters \
    -o ${WORK_DIR}/FCM \
    -k 4 \
    -dm org.apache.mahout.common.distance.EuclideanDistanceMeasure \
    -m 2 \
    -ow \
    -x 10 \
    -cl

mahout clusterdump \
    -i ${WORK_DIR}/FCM/clusters-2-final \
    -o ${WORK_DIR}/cluster555 \
    -p ${WORK_DIR}/FCM/clusteredPoints/part-m-00000

hadoop fs -rmr ${WORK_DIR}
python3 /root/PycharmProjects/ZMA/src/test_ClusterResult2ProbabilityResult.py /ZTE_Demo /ZTE_Demo/


