package scala.com.app.util

import java.util.Properties
import scala.collection.JavaConversions._
import org.apache.kafka.clients.consumer.{ConsumerRecords, KafkaConsumer}


class SimpleConsumer {

  val props = new Properties()
  props.put("bootstrap.servers", "localhost:9092")
  props.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer")
  props.put("value.deserializer", "org.apache.kafka.common.serialization.StringDeserializer")
  props.put("group.id", "exampleConsumer")

  val consumer = new KafkaConsumer[String, String](props)
  val topic = java.util.Collections.singletonList("testTopic")
  consumer.subscribe(topic)

  while(true) {
    val records : ConsumerRecords[String, String] = consumer.poll(100)

    for (record <- records.iterator()) {
      println("record now")
      println(record.value())
    }
  }
}