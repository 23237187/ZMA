#!/usr/bin/env bash

WORK_DIR=/ZTE_Demo

python3 /root/ZMA_Stage_1/src/Data_Preprocess/test_FCM.py /ZTE_Demo/sample_data /ZTE_Demo/fpg_data

hadoop fs -mkdir /ZTE_Demo
hadoop fs -put /ZTE_Demo/sample_data/ratings_for_als.csv ${WORK_DIR}

mahout parallelALS --input ${WORK_DIR}/ratings_for_als.csv --output ${WORK_DIR}/als/out \
    --tempDir ${WORK_DIR}/als/tmp --numFeatures 3 --numIterations 10 --lambda 0.065 --numThreadsPerSolver 4

#mahout seqdumper -i /ZTE_Demo/als/out/U/part-m-00000 -o /ZTE_Demo/U

mkdir /ZTE_Demo/SKM_Iterations

for k in $(seq 1 10)
do
    mahout streamingkmeans \
        -i ${WORK_DIR}/als/out/U/part-m-00000 \
        -o ${WORK_DIR}/SKM \
        -k 3 \
        -ow \
        -km 6
    mahout seqdumper -i /ZTE_Demo/SKM/part-r-00000 -o /ZTE_Demo/SKM_Iterations/SKM-${k}
done


python3 /root/ZMA_Stage_1/src/Data_Preprocess/test_Results_Merge_Util.py

java -jar /app/hadoop-2.6.0/CSV2Mahout.jar

hadoop fs -put /ZTE_Demo/SKM_Iterations/centroids ${WORK_DIR}

mahout kmeans \
    -i ${WORK_DIR}/centroids \
    -c ${WORK_DIR}/init_clusters \
    -o ${WORK_DIR}/KMS \
    -k 3 \
    -dm org.apache.mahout.common.distance.EuclideanDistanceMeasure \
    -x 1 \
    -ow \
    -cl

mahout fkmeans \
    -i ${WORK_DIR}/als/out/U/part-m-00000 \
    -c ${WORK_DIR}/KMS/clusters-1-final \
    -o ${WORK_DIR}/FCM \
    -dm org.apache.mahout.common.distance.EuclideanDistanceMeasure \
    -m 1.0001 \
    -ow \
    -cd 0.005 \
    -x 50 \
    -cl
hadoop fs -ls ${WORK_DIR}/FCM/

echo -e "please enter iteration nums:"
read NUM


mahout clusterdump \
    -i ${WORK_DIR}/FCM/clusters-$NUM-final \
    -o ${WORK_DIR}/cluster555 \
    -p ${WORK_DIR}/FCM/clusteredPoints/




hadoop fs -rmr ${WORK_DIR}/FCM


python3 /root/ZMA_Stage_1/src/test_ClusterResult2ProbabilityResult.py /ZTE_Demo /ZTE_Demo/