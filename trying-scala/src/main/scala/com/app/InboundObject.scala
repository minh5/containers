package com.app

import java.beans.BeanProperty

class InboundObject extends Serializable {
  @BeanProperty
  var id: Long = _
  @BeanProperty
  var name: String = _
}
