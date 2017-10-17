#!/usr/bin/env bash -e
unset SPARK_MASTER_PORT
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/opt/hadoop/lib/native

PROJECT_ID=$(curl -s -H "Metadata-Flavor: Google" http://metadata.google.internal/computeMetadata/v1/project/project-id)
if [[ -n "${PROJECT_ID}" ]]; then
  sed -i "s/NOT_RUNNING_INSIDE_GCE/${PROJECT_ID}/" /opt/spark/conf/core-site.xml
fi

if [ -z "$RELEASE_NAME" ]; then
    echo "RELEASE_NAME not set"
    exit 1
fi
if [ -z "$NAMESPACE" ]; then
    echo "NAMESPACE not set"
    exit 1
fi
export SPARK_MASTER_HOST=${RELEASE_NAME}-spark-master