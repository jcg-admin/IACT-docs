Ejemplo IACT — ``EventoAuditoria`` con FK opcionales
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Un evento puede originarse en un reporte, en una
alerta o en una ejecución ETL — pero no
necesariamente en ninguno (eventos de
autenticación pura, por ejemplo).

.. uml::

   @startuml
   title IACT — ERD snapshot: AuditEvent con origenes opcionales

   entity AuditEvent {
     * event_id : bigint <<PK>>
     --
     * user_id : int <<FK>>
     * type_id : int <<FK>>
     * timestamp : datetime <<IDX>>
     report_id : int <<FK>>
     alert_id : int <<FK>>
     etl_execution_id : int <<FK>>
     payload : text
   }

   entity Report {
     * report_id : int <<PK>>
     --
     name : varchar(150)
   }

   entity Alert {
     * alert_id : int <<PK>>
     --
     state : varchar(20)
   }

   entity ETLExecution {
     * etl_execution_id : int <<PK>>
     --
     * start : datetime
     end : datetime
   }

   Report ||--o{ AuditEvent : "originates (optional)"
   Alert ||--o{ AuditEvent : "originates (optional)"
   ETLExecution ||--o{ AuditEvent : "originates (optional)"
   @enduml

Lectura: un mismo evento de auditoría puede tener
**ningún origen específico** (todas las FK NULL),
o tener **uno** de los tres origenes posibles. El
schema lo permite con FKs nullable.
