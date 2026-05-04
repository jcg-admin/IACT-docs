Ejemplo IACT — ``EventoAuditoria`` con FK opcionales
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Un evento puede originarse en un reporte, en una
alerta o en una ejecución ETL — pero no
necesariamente en ninguno (eventos de
autenticación pura, por ejemplo).

.. uml::

   @startuml
   title IACT — ERD snapshot: EventoAuditoria con origenes opcionales

   entity EventoAuditoria {
     * evento_id : bigint <<PK>>
     --
     * usuario_id : int <<FK>>
     * tipo_id : int <<FK>>
     * timestamp : datetime <<IDX>>
     reporte_id : int <<FK>>
     alerta_id : int <<FK>>
     ejecucion_etl_id : int <<FK>>
     payload : text
   }

   entity Reporte {
     * reporte_id : int <<PK>>
     --
     nombre : varchar(150)
   }

   entity Alerta {
     * alerta_id : int <<PK>>
     --
     estado : varchar(20)
   }

   entity EjecucionETL {
     * ejecucion_etl_id : int <<PK>>
     --
     * inicio : datetime
     fin : datetime
   }

   Reporte ||--o{ EventoAuditoria : "origina (opcional)"
   Alerta ||--o{ EventoAuditoria : "origina (opcional)"
   EjecucionETL ||--o{ EventoAuditoria : "origina (opcional)"
   @enduml

Lectura: un mismo evento de auditoría puede tener
**ningún origen específico** (todas las FK NULL),
o tener **uno** de los tres origenes posibles. El
schema lo permite con FKs nullable.
