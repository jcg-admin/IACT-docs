2.3 Restricción OR en agregación
--------------------------------

A veces la agregación tiene un patrón *"uno u otro"*. En IACT,
una **alerta crítica** notifica por canal de máxima visibilidad,
elegido entre dos opciones del buzón interno (sin email per
CNST_001):

.. uml::

   @startuml
   allowmixing

   class AlertaCritica
   class CanalUrgente
   class CanalPrioritario
   class TipoEntregaImmediata

   AlertaCritica o-- CanalUrgente
   AlertaCritica o-- CanalPrioritario
   AlertaCritica o-- TipoEntregaImmediata

   note "{xor}\nCanalUrgente OR CanalPrioritario\n(no ambos)" as NotaXor
   CanalUrgente .. NotaXor
   CanalPrioritario .. NotaXor
   @enduml
