.. _uc-acc-08-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_ACC_08 — actores y casos asociados

 @startuml
 left to right direction

 actor "grant_exceptional_permission" as INVOKER
 actor "User destino" as TARGET
 actor "view_audit_log" as view_audit_log

 rectangle "MOD_Access" {
   usecase "UC_ACC_08\nPermiso Temporal" as UC08
   usecase "Validar payload\n(justification +\nexpires_at bounds)" as VPL
   usecase "Validar SoD\nwrite-time" as VSOD
   usecase "INSERT\nExceptionalPermissions" as INS
   usecase "Notificar via\nInternalMailbox\n(OBLIGATORIO)" as NOT
   usecase "AuditEvent\nGRANTED reforzado" as EMI
 }

 INVOKER --> UC08
 UC08 ..> VPL : <<include>>
 UC08 ..> VSOD : <<include>>
 UC08 ..> INS : <<include>>
 UC08 ..> NOT : <<include>>
 UC08 ..> EMI : <<include>>
 NOT --> TARGET
 EMI --> view_audit_log

 note bottom of NOT
   Mailbox-or-abort HARD
   (P-10) — sin notificacion
   no se completa
 end note
 note bottom of UC08
   Trazabilidad reforzada:
   justification + expires_at
   + ticket_reference
 end note

 @enduml

8.2 Diagrama de secuencia
=========================

.. uml::
 :caption: UC_ACC_08 — flujo principal

 @startuml

 actor Invoker as Invoker
 participant "Frontend" as Frontend
 participant "GrantExcView" as Grantexcview
 participant "AccessService" as Accessservice
 participant "SoDValidator" as Sodvalidator
 participant "PermissionCache" as Permissioncache
 participant "InternalMailbox" as Internalmailbox
 participant "AuditLog" as Auditlog
 database "Repo" as Repo

 I -> Frontend: Form con functions, expires_at,\n  justification, ticket_ref
 Frontend -> Grantexcview: POST /api/users/{id}/\n  exceptional-permissions/

 Grantexcview -> Grantexcview: Validar JWT
 Grantexcview -> Grantexcview: Verificar grant_exceptional_permission
 alt Sin la funcion
   Grantexcview --> Frontend: 403
   Grantexcview -> Auditlog: emit UNAUTHORIZED ALERTA ALTA
 else
   Grantexcview -> Accessservice: grant_exceptional(target_id,\n  function_ids, expires_at,\n  justification, ticket_ref,\n  invoker)

   Accessservice -> Repo: SELECT User FOR UPDATE
   alt User invalido
     Accessservice --> Grantexcview: error
     Grantexcview --> Frontend: 404 / 400
   else OK
     Accessservice -> Accessservice: validar P-11 anti-self
     Accessservice -> Accessservice: validar payload\n  (justification, expires_at)
     Accessservice -> Repo: SELECT Function WHERE id IN ...
     alt Funcion invalida
       Accessservice --> Grantexcview: error
       Grantexcview --> Frontend: 400
     else OK
       Accessservice -> Repo: SELECT ExceptionalPermission\n  ACTIVE existentes
       Accessservice -> Accessservice: filtrar idempotencia
       Accessservice -> Sodvalidator: validate(effective_post_grant,\n  rules)
       alt SoD viola
         Sodvalidator --> Accessservice: SoDViolation
         Accessservice -> Auditlog: emit GRANT_FAILED ALERTA
         Grantexcview --> Frontend: 409
       else SoD OK
         group Transaccion atomica
           Accessservice -> Repo: INSERT ExceptionalPermission\n  (N filas)
           Accessservice -> Internalmailbox: send obligatorio
           alt Mailbox falla
             Internalmailbox --> Accessservice: MailboxFailure
             Accessservice -> Auditlog: emit GRANT_FAILED
             Grantexcview --> Frontend: 500 (rollback)
           else Mailbox OK
             Accessservice -> Auditlog: emit\n  EXCEPTIONAL_PERMISSION_GRANTED
           end
         end
         Accessservice -> Permissioncache: invalidate(target.id) post-COMMIT
         Accessservice --> Grantexcview: result
         Grantexcview --> Frontend: 201 Created
       end
     end
   end
 end

 @enduml

8.3 Diagrama de actividad
=========================

.. uml::
 :caption: UC_ACC_08 — actividad

 @startuml

 start

 :POST exceptional-permissions/;

 if (JWT valido?) then (no)
   :401; stop
 else (si)
 endif

 if (Tiene grant_exceptional_permission?) then (no)
   :403; :Audit UNAUTHORIZED ALERTA ALTA;
   stop
 else (si)
 endif

 if (User existe + state OK?) then (no)
   :404 / 400; stop
 else (si)
 endif

 if (P-11 viola?) then (si)
   :400 SELF_GRANT_FORBIDDEN;
   :Audit ALERTA CRITICA;
   stop
 else (no)
 endif

 if (justification + expires_at validos?) then (no)
   :400 VALIDATION_ERROR; stop
 else (si)
 endif

 if (Funciones validas?) then (no)
   :400; stop
 else (si)
 endif

 :Filtrar idempotencia;
 if (Quedan funciones a grant?) then (no)
   :Audit GRANT_NOOP;
   :200 OK informativo;
   stop
 else (si)
 endif

 :Construir effective_post_grant;
 :Evaluar SoDRules;

 if (SoD viola?) then (si)
   :409 SOD_VIOLATION;
   :Audit GRANT_FAILED ALERTA;
   stop
 else (no)
 endif

 :Iniciar transaccion atomica;
 :INSERT ExceptionalPermission (N);
 :INSERT InternalMessage (obligatorio P-10);
 if (Mailbox OK?) then (no)
   :ROLLBACK;
   :500 MAILBOX_FAILED;
   stop
 else (si)
 endif
 :INSERT AuditEvent
  EXCEPTIONAL_PERMISSION_GRANTED;
 :Commit;

 :PermissionCache.invalidate post-COMMIT;
 :201 Created;

 stop

 @enduml

8.4 Diagrama de estados — ExceptionalPermission
===============================================

.. uml::
 :caption: Estados de ExceptionalPermission

 @startuml

 [*] --> ACTIVE : UC_ACC_08\n(grant)

 ACTIVE --> EXPIRED : cron job\n(NOW() > expires_at)
 ACTIVE --> REVOKED : revocacion\nexplicita
 EXPIRED --> [*]
 REVOKED --> [*]

 note right of EXPIRED
   AuditEvent
   EXCEPTIONAL_PERMISSION_EXPIRED
   automatico
 end note

 @enduml
