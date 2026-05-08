.. _uc-aud-03-parte-08-diagrama-estados-export-job:

8.3 Diagrama de estados — ExportJob de auditoria
===================================================

.. uml::
 :caption: ExportJob — ciclo de vida del job asincrono.

 @startuml

 [*] --> Queued : encolado por endpoint
 Queued --> Processing : Worker toma el job
 Processing --> Done : archivo generado +\nentregado a mailbox
 Processing --> Failed : error I/O / size limit
 Failed --> Queued : reintento automatico\n(max 3)
 Failed --> [*] : maximo de retries\nalcanzado
 Done --> [*] : notificacion enviada

 note right of Queued
   Job en cola esperando
   ExportWorker disponible.
   ETA visible al user.
 end note

 note right of Processing
   Worker activo. Progress
   actualizado en tiempo real
   visible al user.
 end note

 note right of Failed
   Reintento automatico hasta 3 veces.
   Despues, alerta al admin y
   estado terminal.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/export-job`.
 - :doc:`/arquitectura-tecnica/domain-model/export-worker`.
