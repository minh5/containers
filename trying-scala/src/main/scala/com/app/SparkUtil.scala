package com.app

import org.apache.spark.sql.SparkSession

class SparkUtil {
  val spark = SparkSession
    .builder
    .appName("KafkaSpark")
    .master("local")
    .getOrCreate()
  val df = spark
    .readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "testTopic")
    .load()
    .show()
}
