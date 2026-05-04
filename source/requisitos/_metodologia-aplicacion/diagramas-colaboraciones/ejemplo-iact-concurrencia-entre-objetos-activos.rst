8.1 Ejemplo IACT — concurrencia entre objetos activos
-----------------------------------------------------

.. uml::

   @startuml
   allowmixing
   object ":Backend" as Backend <<active>>
   object ":Scheduler" as Sch <<active>>
   object ":EvaluadorAlertas" as EvaluadorAlertas <<active>>
   object ":SupervisorETL" as Sup <<active>>
   object ":BDAnalytics"                  as BDAnalytics
   object ":AuditLog"                     as AuditLog
   object ":BuzonInterno"                 as BuzonInterno

   Backend   -> BDAnalytics  : "consultar"
   Sch -> Sup : "disparar_carga()"
   Sup -> BDAnalytics  : "INSERT filas"
   EvaluadorAlertas  -> BDAnalytics  : "evaluar_metrica()"
   EvaluadorAlertas  -> BuzonInterno  : "notificar_alerta()"
   Backend   -> AuditLog  : "registrar()"
   Sup -> AuditLog  : "registrar()"
   EvaluadorAlertas  -> AuditLog  : "registrar()"

   note right of EvaluadorAlertas
     Tres objetos activos en
     paralelo: Backend (atendiendo
     requests), Scheduler+
     SupervisorETL (cargando datos),
     EvaluadorAlertas (monitoreando
     umbrales). Todos escriben en
     BDAnalytics y AuditLog
     (objetos pasivos).
   end note
   @enduml

----
