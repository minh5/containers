FROM minh5/hadoop

MAINTAINER minh mai

ENV SPARK_VERSION     2.2.0
ENV HADOOP_VERSION    2.7.4 
ENV HADOOP_HOME       /opt/hadoop
ENV SPARK_HOME        /opt/spark
ENV SPARK_CONF_DIR    ${SPARK_HOME}/conf 
ENV PATH              ${PATH}:$HADOOP_HOME/bin
ENV GOSU_VERSION      1.10

USER root

RUN apt-get update && \
    apt-get install -y scala python python-dev python-pip python3 python3-dev python3-pip apt-utils && \
    apt-get clean

# download and configure Spark
RUN wget -q https://d3kbcqa49mib13.cloudfront.net/spark-${SPARK_VERSION}-bin-hadoop2.7.tgz && \
    tar -xzf spark-${SPARK_VERSION}-bin-hadoop2.7.tgz && \
    rm spark-${SPARK_VERSION}-bin-hadoop2.7.tgz && \
    mv spark-${SPARK_VERSION}-bin-hadoop2.7 $SPARK_HOME

# copy drivers and files from Hadoop to Spark
RUN mkdir -p $SPARK_HOME/lib && \
  cp -r $HADOOP_HOME/share/hadoop/common/* $SPARK_HOME/lib && \
  cp $HADOOP_PREFIX/etc/hadoop/core-site.xml $SPARK_CONF_DIR && \
  cp $HADOOP_PREFIX/etc/hadoop/hdfs-site.xml $SPARK_CONF_DIR && \
  cp $HADOOP_PREFIX/etc/hadoop/slaves $SPARK_CONF_DIR

# install gosu
RUN arch="$(dpkg --print-architecture | awk -F- '{ print $NF }')" && \
    wget -O /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/1.10/gosu-$arch" && \
    chmod +x /usr/local/bin/gosu && \
    gosu nobody true

#install tini
RUN wget https://github.com/krallin/tini/releases/download/v0.16.1/tini && \
    chmod +x tini && \
    mv tini /bin

EXPOSE 8080 8081 4040 7077 7078

