.. _uc-acc-09-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_ACC_09 — actores y casos asociados

 @startuml
 left to right direction

 actor "view_audit_log" as INVOKER
 actor "Sistema" as Sistema

 rectangle "MOD_Access" {
   usecase "UC_ACC_09\nAuditar Cambios" as UC09
   usecase "Listar eventos\npaginado" as LST
   usecase "Ver detalle" as DET
   usecase "Agregar (count\npor categoria)" as AGG
   usecase "Audit P-16\nselectivo" as AUDS
 }

 INVOKER --> UC09
 UC09 ..> LST : <<extend>>
 UC09 ..> DET : <<extend>>
 UC09 ..> AGG : <<extend>>
 LST ..> AUDS : <<extend (filter\ntarget_user_id)>>
 DET ..> AUDS : <<include>>
 Sistema --> AUDS

 note bottom of UC09
   Subset de UC_AUD_*
   filtrado por
   ACCESS_EVENT_TYPES
 end note

 @enduml

8.2 Diagrama de secuencia (listado)
===================================

.. uml::
 :caption: UC_ACC_09 sub-flujo listado

 @startuml

 actor Invoker as Invoker
 participant "Frontend" as Frontend
 participant "AccessAuditView" as Accessauditview
 participant "AuditEventRepo" as Auditeventrepo
 participant "AuditLog" as Auditlog

 I -> Frontend: Aplicar filtros
 Frontend -> Accessauditview: GET /api/access/audit/?...

 Accessauditview -> Accessauditview: Validar JWT (CNST-009)
 Accessauditview -> Accessauditview: Verificar view_audit_log
 alt Sin permiso
   Accessauditview --> Frontend: 403
   Accessauditview -> Auditlog: emit UNAUTHORIZED_ACCESS_ATTEMPT
 else Con permiso
   Accessauditview -> Accessauditview: Validar filtros (whitelist P-20)
   alt Filtros invalidos
     Accessauditview --> Frontend: 400 BAD_FILTER
   else Validos
     Accessauditview -> Auditeventrepo: list_paginated(\n  event_type__in=ACCESS_EVENT_TYPES,\n  filters, ordering, page)
     Auditeventrepo --> Accessauditview: results
     Accessauditview -> Accessauditview: aplicar mascarado PII\n(CNST-026)
     opt filter target_user_id presente
       Accessauditview -> Auditlog: emit\n  ACCESS_AUDIT_VIEWED
     end
     Accessauditview --> Frontend: 200 OK
     Frontend --> I: Tabla
   end
 end

 @enduml

8.3 Diagrama de actividad
=========================

.. uml::
 :caption: UC_ACC_09 — actividad

 @startuml

 start

 :GET /api/access/audit/?...;

 if (JWT valido?) then (no)
   :401; stop
 else (si)
 endif

 if (view_audit_log?) then (no)
   :403; :Audit UNAUTHORIZED;
   stop
 else (si)
 endif

 if (Filtros validos whitelist?) then (no)
   :400 BAD_FILTER; stop
 else (si)
 endif

 :Construir query con
  event_type__in=ACCESS_EVENT_TYPES
  + filters provistos;
 :SELECT paginado;
 :Aplicar mascarado PII;

 if (filter target_user_id?) then (si)
   :Audit ACCESS_AUDIT_VIEWED;
 else (no)
 endif

 :200 OK;

 stop

 @enduml

8.4 Diagrama de relaciones
==========================

.. uml::
 :caption: UC_ACC_09 consume eventos de los
           UCs productores

 @startuml

 [UC_ACC_01 (assign)] --> [AuditEvent]
 [UC_ACC_02 (revoke)] --> [AuditEvent]
 [UC_ACC_04 (AGR)] --> [AuditEvent]
 [UC_ACC_05 (SoD)] --> [AuditEvent]
 [UC_ACC_08 (excepc)] --> [AuditEvent]
 [UC_USR_04 (eliminate)] --> [AuditEvent]
 [AuditEvent] --> [UC_ACC_09 (vista audit)]
 [UC_ACC_09 (vista audit)] --> [Auditor]

 note bottom of [AuditEvent]
   AuditEvent es append-only
   (CNST-025); UC_ACC_09 solo lee.
 end note

 @enduml
