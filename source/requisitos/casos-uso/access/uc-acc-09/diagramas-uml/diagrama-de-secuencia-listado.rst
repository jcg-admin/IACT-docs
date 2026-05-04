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

