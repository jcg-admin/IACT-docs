14.11 Sincronización — UC_ALR_03
--------------------------------

.. uml::

   @startuml
   allowmixing

   object ":Supervisor" as Supervisor
   object ":alr_app" as Alr
   object ":audit_log" as Audit
   object ":log_app" as Log
   object ":Alerta" as Alerta

   Supervisor -> Alr : "1: reconocer(alerta_id)"
   Alr -> Audit : "1.1: registrar(CNST_025)"
   Alr -> Log : "1.2: notificar(CNST_001)"
   Alr -> Alerta : "1.3: cambiar_estado(reconocida)"
   note right of Alerta
     estado: publicada → reconocida
   end note
   @enduml
