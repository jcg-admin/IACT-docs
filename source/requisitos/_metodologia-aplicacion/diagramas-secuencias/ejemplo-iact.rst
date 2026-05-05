Ejemplo IACT
~~~~~~~~~~~~

.. uml::

   @startuml
   title UC_RPT_04 — paso opcional de notificacion

   participant "rpt_app" as Rpt
   participant "log_app" as Log
   actor Supervisor

   Rpt -> Rpt : encolar export

   opt [supervisor.notif_buzon == true]
     Rpt ->> Log : notificar buzon (CNST_001)
     Log --> Supervisor : entrega mensaje
   end

   Rpt --> Rpt : retornar tarea_id
   @enduml

Lectura: la notificación al buzón solo se dispara
cuando el supervisor tiene la preferencia
activada; si no, el flujo continúa sin tocar
``log_app``.
