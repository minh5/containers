{{- define "spark-defaults-conf" -}}
spark.master spark://spark-master:7077
spark.driver.extraClassPath /opt/spark/lib/*
spark.executor.extraClassPath /opt/spark/lib/*
spark.driver.extraLibraryPath /opt/hadoop/lib/native
spark.executor.extraLibraryPath /opt/hadoop/lib/native
spark.sql.warehouse.dir /data
spark.app.id KubernetesSpark
spark.executor.memory {{ .Values.executor.memory }}
spark.driver.memory {{ .Values.driver.memory }}
spark.network.timeout 200
spark.driver.extraJavaOptions -XX:+UseCompressedOops
spark.executor.extraJavaOptions -XX:+UseCompressedOops -XX:+PrintGCDetails -XX:+PrintGCTimeStamps
spark.ui.reverseProxy	true
spark.ui.reverseProxyUrl /
spark.eventLog.enabled true
spark.history.fs.logDirectory hdfs://hdfs-nn:9000/shared/spark-logs
spark.eventLog.dir hdfs://hdfs-nn:9000/shared/spark-logs
{{- end -}}
