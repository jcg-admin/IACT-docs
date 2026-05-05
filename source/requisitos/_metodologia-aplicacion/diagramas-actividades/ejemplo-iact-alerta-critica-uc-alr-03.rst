Ejemplo IACT — Alerta crítica (UC_ALR_03)
-----------------------------------------

.. uml::

   @startuml
   start
   :EvaluadorAlertas detecta umbral excedido;
   :Emitir senal "AlertaCritica";
   note right
     senal asincronica
     hacia el supervisor
   end note
   :Registrar emision en AuditLog;
   stop
   @enduml

.. uml::

   @startuml
   start
   :Esperar senal "AlertaCritica";
   :Recibir senal;
   :Mostrar alerta en panel del supervisor;
   :Habilitar accion "reconocer";
   stop
   @enduml
