FROM openjdk:8-jre

MAINTAINER minh

ENV SPARK_VERSION     2.2.0
ENV HADOOP_VERSION    2.7.4 
ENV HADOOP_HOME       /opt/hadoop
ENV SPARK_HOME        /opt/spark
ENV SPARK_CONF_DIR    ${SPARK_HOME}/conf 
ENV PATH              ${PATH}:$HADOOP_HOME/bin

USER root
RUN apt-get update && \
    apt-get install -y scala python3 python3-dev apt-utils && \
    apt-get clean

# download and condfigure Hadoop
RUN mkdir -p $HADOOP_HOME && \
    wget -q http://apache.cs.utah.edu/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz && \
    tar -zxf hadoop-${HADOOP_VERSION}.tar.gz && \
    mv hadoop-${HADOOP_VERSION} $HADOOP_HOME && \
    chown -R root:root $HADOOP_HOME

# download and configure Spark
RUN wget -q https://d3kbcqa49mib13.cloudfront.net/spark-${SPARK_VERSION}-bin-hadoop2.7.tgz && \
    tar -xzf spark-${SPARK_VERSION}-bin-hadoop2.7.tgz && \
    rm spark-${SPARK_VERSION}-bin-hadoop2.7.tgz && \
    mv spark-${SPARK_VERSION}-bin-hadoop2.7 $SPARK_HOME

# download extra drivers
RUN mkdir -p $SPARK_HOME/lib && cd $SPARK_HOME/lib && \
  curl -O https://storage.googleapis.com/hadoop-lib/gcs/gcs-connector-latest-hadoop2.jar && \
  curl -O https://jdbc.postgresql.org/download/postgresql-42.1.3.jar && \
  curl -O http://central.maven.org/maven2/org/apache/hadoop/hadoop-aws/2.7.3/hadoop-aws-2.7.3.jar && \
  curl -O http://central.maven.org/maven2/com/amazonaws/aws-java-sdk/1.7.4.2/aws-java-sdk-1.7.4.2.jar

EXPOSE 8080 8081 4040 7077 7078

COPY ./docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh
# ENTRYPOINT [ "/docker-entrypoint.sh" ]

