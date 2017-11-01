#!/bin/bash -e

: ${SPARK_PREFIX:=/opt/spark}
# Directory to find config artifacts
CONFIG_DIR="/tmp/config"


# Copy spark config files
for f in spark-env.sh log4j.properties spark-defaults.conf; do
  if [[ -e ${CONFIG_DIR}/$f ]]; then
    cp ${CONFIG_DIR}/$f $SPARK_CONF_DIR/$f
  else
    echo "ERROR: Could not find $f in $CONFIG_DIR"
    exit 1
  fi
done

# Common spark setup
. $SPARK_PREFIX/conf/spark-env.sh
cd /opt/spark

case "$1" in
    -master)
        echo "$(hostname -i) $SPARK_MASTER_HOST" >> /etc/hosts
        # Run spark-class directly so that when it exits (or crashes), the pod restarts.
        /opt/spark/bin/spark-class org.apache.spark.deploy.master.Master --ip $SPARK_MASTER_HOST --port 7077 --webui-port 8080
        ;;
    -worker)
        if ! getent hosts $SPARK_MASTER_SERVICE_HOST; then
          echo "=== Cannot resolve the DNS entry for spark-master. Has the service been created yet, and is SkyDNS functional?"
          echo "=== See http://kubernetes.io/v1.1/docs/admin/dns.html for more details on DNS integration."
          echo "=== Sleeping 10s before pod exit."
          sleep 10
          exit 0
        fi
        /opt/spark/bin/spark-class org.apache.spark.deploy.worker.Worker spark://${SPARK_MASTER_HOST}:7077 --webui-port 8081
        ;;
    -notebook)
        for f in user.sh jupyter.sh; do
          chmod +x ${CONFIG_DIR}/$f
          ${CONFIG_DIR}/$f
        done
        export PYSPARK_DRIVER_PYTHON=jupyter
        export PYSPARK_DRIVER_PYTHON_OPTS=notebook
        export PYSPARK_PYTHON=ipython
        gosu user:supergroup bash -c 'tini -s -- /opt/spark/bin/pyspark --master spark://${SPARK_MASTER_HOST}:7077'
        ;;
    -bash)
        bash "${@:2}"
        ;;
    *)
        echo $"Usage: $0 {-master|-worker|-notebook|-bash}"
        exit 1
esac