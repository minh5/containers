FROM minh5/hadoop

MAINTAINER minh mai

ENV SPARK_VERSION     2.2.0
ENV HADOOP_VERSION    2.7.4 
ENV HADOOP_HOME       /opt/hadoop
ENV SPARK_HOME        /opt/spark
ENV SPARK_CONF_DIR    ${SPARK_HOME}/conf 
ENV PATH              ${PATH}:$HADOOP_HOME/bin

USER root

RUN apt-get update && \
    apt-get install -y scala python3 python3-dev python3-pip apt-utils && \
    apt-get clean

# download and configure Spark
RUN wget -q https://d3kbcqa49mib13.cloudfront.net/spark-${SPARK_VERSION}-bin-hadoop2.7.tgz && \
    tar -xzf spark-${SPARK_VERSION}-bin-hadoop2.7.tgz && \
    rm spark-${SPARK_VERSION}-bin-hadoop2.7.tgz && \
    mv spark-${SPARK_VERSION}-bin-hadoop2.7 $SPARK_HOME

# copy drivers from Hadoop common to Spark lib
RUN mkdir -p $SPARK_HOME/lib && \
  cp -r $HADOOP_HOME/share/hadoop/common/* $SPARK_HOME/lib
  
EXPOSE 8080 8081 4040 7077 7078

