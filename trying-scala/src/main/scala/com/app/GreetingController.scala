package com.app

import org.springframework.http.{HttpStatus, ResponseEntity}
import org.springframework.web.bind.annotation._

@RestController
@RequestMapping(path = Array("/test/"))
class GreetingController {
  @PostMapping(path = Array("/users"))
  def greeting(@RequestBody inboundObject: InboundObject): ResponseEntity[String] = {
    /* put producer in here with the post mapping
       take inboundObject and pass to the producer
       bonus: try Spark streaming consumer to persist to parquet */
    val array = Array(inboundObject.id.toString(), inboundObject.name)
    val producer = new SimpleProducer(array, "testTopic")
    new ResponseEntity(inboundObject.name, HttpStatus.OK)
  }
}

///* To lookup
// Request body spring for scala
// change names to be more "professional"
//