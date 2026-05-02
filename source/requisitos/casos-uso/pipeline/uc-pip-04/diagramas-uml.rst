.. _uc-pip-04-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "retry_etl" as USR
 actor "ETLScheduler" as DE
 rectangle "MOD_Pipeline" {
   usecase "UC_PIP_04\nReintentar ETL" as UC04
 }
 USR --> UC04
 UC04 --> DE
 @enduml

8.2 Actividad
=============

.. uml::

 @startuml
 start
 :POST /api/v1/etl/reintento/;
 :JWT + RBAC (retry_etl);
 :Validar trimestre y motivo (min 20 chars);
 if (ETL en ejecucion?) then (si)
   :409 Conflict; stop
 endif
 :Registrar nueva ejecucion (manual);
 :Invocar Disparador ETL (reproceso completo);
 :Emitir auditoria ETL_REINTENTO_SOLICITADO;
 :202 Accepted con etl_run_id;
 stop
 @enduml

8.3 Estado del reintento
=========================

.. uml::

 @startuml
 [*] --> en_ejecucion : POST reintento aceptado
 en_ejecucion --> exitoso : SP completa sin errores
 en_ejecucion --> fallido : SP lanza error
 exitoso --> [*]
 fallido --> [*] : requiere nuevo reintento
 @enduml

8.4 Secuencia
=============

.. uml::

 @startuml
 actor "retry_etl" as O
 participant "Endpoint" as E
 database "Registro de\nEjecuciones" as R
 participant "Disparador ETL" as DE
 participant "AuditService" as A
 O -> E: POST /api/v1/etl/reintento/
 E -> E: JWT + RBAC + validar
 E -> R: get_activa()
 R --> E: null (sin ejecucion activa)
 E -> R: crear_manual(trimestre, manual)
 R --> E: etl_run_id
 E -> DE: ejecutar_historico(trimestre)
 E -> A: emit ETL_REINTENTO_SOLICITADO
 E --> O: 202 Accepted {etl_run_id}
 @enduml
