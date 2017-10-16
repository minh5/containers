#! /bin/bash
CONFIG_DIR="/tmp/hadoop-config"

for f in core-site.xml hdfs-site.xml slaves; do
  if [[ -e ${CONFIG_DIR}/$f ]]; then
    cp ${CONFIG_DIR}/$f $HADOOP_PREFIX/etc/hadoop/$f
  else
    echo "ERROR: Could not find $f in $CONFIG_DIR"
    exit 1
  fi
done

: ${HADOOP_PREFIX:=/opt/hadoop}
. $HADOOP_PREFIX/etc/hadoop/hadoop-env.sh

case "$1" in
    -datanode)
        mkdir -p /root/hdfs/datanode
        $HADOOP_PREFIX/bin/hdfs datanode
        ;;
    -namenode)
        echo "$(hostname -i) hdfs-nn" >> /etc/hosts
        mkdir -p /root/hdfs/namenode
        $HADOOP_PREFIX/bin/hdfs namenode -format -force -nonInteractive
        $HADOOP_PREFIX/bin/hdfs namenode
        ;;
    *)
        echo $"Usage: $0 {-datanode|-namenode}"
        exit 1
esac

until find ${HADOOP_PREFIX}/logs -mmin -1 | egrep -q '.*'; echo "`date`: Waiting for logs..." ; do sleep 2 ; done
tail -F ${HADOOP_PREFIX}/logs/* &
while true; do sleep 1000; done