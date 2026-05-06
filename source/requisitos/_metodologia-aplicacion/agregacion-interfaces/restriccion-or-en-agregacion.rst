2.3 Restricción OR en agregación
--------------------------------

A veces la agregación tiene un patrón *"uno u otro"*. En IACT,
una **alerta crítica** notifica por canal de máxima visibilidad,
elegido entre dos opciones del buzón interno (sin email per
CNST_001):

.. uml::

   @startuml
   allowmixing

   class CriticalAlert
   class UrgentChannel
   class PriorityChannel
   class ImmediateDeliveryType

   CriticalAlert o-- UrgentChannel
   CriticalAlert o-- PriorityChannel
   CriticalAlert o-- ImmediateDeliveryType

   note "{xor}\nUrgentChannel OR PriorityChannel\n(no ambos)" as NotaXor
   UrgentChannel .. NotaXor
   PriorityChannel .. NotaXor
   @enduml
