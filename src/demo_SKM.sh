#!/usr/bin/env bash

WORK_DIR=/ZTE_Demo

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

