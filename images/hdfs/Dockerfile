FROM openjdk:8-jre

MAINTAINER minh mai

USER root

ENV HADOOP_VERSION        2.7.4 
ENV HADOOP_HOME           /usr/local/hadoop
ENV HADOOP_HDFS_HOME      /usr/local/hadoop
ENV HADOOP_PREFIX         /usr/local/hadoop
ENV HADOOP_COMMON_HOME    /usr/local/hadoop
ENV HADOOP_MAPRED_HOME    /usr/local/hadoop
ENV HADOOP_YARN_HOME      /usr/local/hadoop
ENV HADOOP_CONF_DIR       /usr/local/hadoop/etc/hadoop
ENV YARN_CONF_DIR         /usr/local/hadoop/etc/hadoop
ENV PATH                  ${PATH}:$HADOOP_HOME

RUN apt-get update && \
    apt-get install -y build-essential ssh openssh-client
 
# download and condfigure Hadoop
RUN wget -q http://apache.cs.utah.edu/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz && \
    tar -zxf hadoop-${HADOOP_VERSION}.tar.gz && \
    rm hadoop-${HADOOP_VERSION}.tar.gz && \
    mv hadoop-${HADOOP_VERSION} $HADOOP_HOME

# download extra drivers
RUN cd $HADOOP_HOME/share/hadoop/common && \
  curl -O https://storage.googleapis.com/hadoop-lib/gcs/gcs-connector-latest-hadoop2.jar && \
  curl -O https://jdbc.postgresql.org/download/postgresql-42.1.3.jar && \
  curl -O http://central.maven.org/maven2/org/apache/hadoop/hadoop-aws/2.7.3/hadoop-aws-2.7.3.jar && \
  curl -O http://central.maven.org/maven2/com/amazonaws/aws-java-sdk/1.7.4.2/aws-java-sdk-1.7.4.2.jar
 
# Hdfs ports
EXPOSE 50010 50020 50070 50075 50090 8020 9000
# Mapred ports
EXPOSE 10020 19888
#Yarn ports
EXPOSE 8030 8031 8032 8033 8040 8042 8088
#Other ports
EXPOSE 49707 2122