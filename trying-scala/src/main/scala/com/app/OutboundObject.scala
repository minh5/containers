//package com.app
//
//class OutboundObject(topic: String){
//
//  val TOPIC = topic
//  def return_values(topic: String): String {
//    val consumer = new KafkaConsumer[String, String](props)
//    consumer.subscribe(util.Collections.singletonList(topic))
//
//    while(true){
//      val records = consumer.poll(100)
//      for (record<-records.asScala){
//        println(record)
//    }
//  }


//}
/* has method to get an string array and return everything from Kafka consumer
 goal is to have a json showing all my data */