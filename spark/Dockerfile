FROM openjdk:8-jre

# Install System Build Dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential git nfs-common && rm -rf /var/lib/apt/lists/* && apt-get clean

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

# HADOOP
ENV HADOOP_VERSION=2.7.3 \
    HADOOP_HOME=/opt/hadoop \
    PATH=${PATH}:/opt/hadoop/bin

RUN mkdir -p /opt && curl -sL --retry 3 \
  "http://archive.apache.org/dist/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz" \
  | tar -zx hadoop-${HADOOP_VERSION}/lib/native \
  && mv hadoop-${HADOOP_VERSION} $HADOOP_HOME \
  && chown -R root:root $HADOOP_HOME

# SPARK
ENV SPARK_VERSION=2.2.0 \
    SPARK_HOME=/opt/spark
ENV SPARK_PACKAGE=spark-${SPARK_VERSION}-bin-hadoop2.7 \
    SPARK_CONF_DIR=${SPARK_HOME}/conf \
    PATH=${PATH}:${SPARK_HOME}/bin

RUN curl -sL --retry 3 \
  "http://www.us.apache.org/dist/spark/spark-${SPARK_VERSION}/${SPARK_PACKAGE}.tgz" \
  | gunzip \
  | tar x -C /opt/ \
  && mv /opt/$SPARK_PACKAGE $SPARK_HOME \
  && chown -R root:root $SPARK_HOME \
  && mkdir -p /data

# Add additional dependencies
RUN mkdir -p $SPARK_HOME/lib && cd $SPARK_HOME/lib && \
  curl -O https://storage.googleapis.com/hadoop-lib/gcs/gcs-connector-latest-hadoop2.jar && \
  curl -O https://jdbc.postgresql.org/download/postgresql-42.1.3.jar && \
  curl -O http://central.maven.org/maven2/org/apache/hadoop/hadoop-aws/2.7.3/hadoop-aws-2.7.3.jar && \
  curl -O http://central.maven.org/maven2/com/amazonaws/aws-java-sdk/1.7.4.2/aws-java-sdk-1.7.4.2.jar

ENV GOSU_VERSION 1.10
RUN set -x \
    && dpkgArch="$(dpkg --print-architecture | awk -F- '{ print $NF }')" \
    && wget -O /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch" \
    && wget -O /usr/local/bin/gosu.asc "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch.asc" \
    && gpg --keyserver ha.pool.sks-keyservers.net --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4 \
    && gpg --batch --verify /usr/local/bin/gosu.asc /usr/local/bin/gosu \
    && rm -r /usr/local/bin/gosu.asc \
    && chmod +x /usr/local/bin/gosu \
    && gosu nobody true

#Spark ports
EXPOSE 8080 8081 4040 7077 7078

