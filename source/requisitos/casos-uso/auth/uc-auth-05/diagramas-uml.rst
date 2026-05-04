.. _uc-auth-05-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_AUTH_05 — actores y casos asociados

 @startuml

 left to right direction

 actor "view_all_active_sessions" as ADMIN
 actor "User afectado" as USER <<beneficiario>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "Sistema" as Sistema <<sistema>>

 rectangle "MOD_Auth" {
   usecase "UC_AUTH_05\nGestionar Sesiones" as UC05
   usecase "Listar Sessions" as LST
   usecase "Cerrar Session\nindividual" as CerrarSession
   usecase "Cerrar todas\nlas del User" as CALL
   usecase "Notificar\n(opcional)" as NOT
   usecase "AuditEvent\nSESSION_CLOSED" as EMI
 }

 ADMIN --> UC05
 UC05 ..> LST : <<extend>>
 UC05 ..> CerrarSession : <<extend>>
 UC05 ..> CALL : <<extend>>
 CerrarSession ..> EMI : <<include>>
 CALL ..> EMI : <<include>>
 CerrarSession ..> NOT : <<extend>>
 CALL ..> NOT : <<extend>>
 NOT --> USER
 Sistema --> EMI
 EMI --> view_audit_log

 @enduml

8.2 Diagrama de secuencia (cierre individual)
=============================================

.. uml::
 :caption: UC_AUTH_05 sub-flujo 3.B

 @startuml

 actor Admin as Admin
 participant "Frontend" as Frontend
 participant "CloseSessionView" as Closesessionview
 participant "SessionService" as Sessionservice
 database "Base de Datos" as BaseDeDatos

 Admin -> Frontend: Click "Cerrar" en Session X
 Frontend -> Frontend: Modal confirm
 Admin -> Frontend: Confirmar
 Frontend -> Closesessionview: POST /api/auth/sessions/{id}/close/
 Closesessionview -> Closesessionview: Validar JWT (CNST-009)
 Closesessionview -> Closesessionview: Verificar close_user_session
 alt Sin permiso
   Closesessionview --> Frontend: 403 FORBIDDEN
 else
   Closesessionview -> Sessionservice: close(session_id, admin)

   group Transaccion atomica
     Sessionservice -> BaseDeDatos: SELECT Session FOR UPDATE
     BaseDeDatos --> Sessionservice: session
     alt Ya CLOSED (FA-02)
       Sessionservice -> BaseDeDatos: INSERT AuditEvent SESSION_CLOSE_NOOP
       Sessionservice --> Closesessionview: noop
     else ACTIVE
       Sessionservice -> BaseDeDatos: UPDATE Session SET\n  state='CLOSED',\n  close_reason='ADMIN_REVOKED',\n  closed_by_admin_id=admin.id
       Sessionservice -> BaseDeDatos: INSERT BlacklistedToken
       Sessionservice -> BaseDeDatos: INSERT AuditEvent SESSION_CLOSED
       opt NOTIFY_USER_ON_ADMIN_SESSION_CLOSE
         Sessionservice -> BaseDeDatos: INSERT InternalMessage
       end
     end
   end

   Sessionservice --> Closesessionview: result
   Closesessionview --> Frontend: 200 OK
   Frontend --> Admin: Toast confirmacion
 end

 @enduml

8.3 Diagrama de actividad (cierre masivo 3.C)
=============================================

.. uml::
 :caption: UC_AUTH_05 sub-flujo 3.C — actividad

 @startuml

 start

 :Admin abre detalle del User;
 :Click "Cerrar todas las sesiones";
 :Modal robusto con count;

 if (Admin confirma?) then (no)
   :Cancelar; stop
 else (si)
 endif

 :POST /api/users/{id}/close-all-sessions/;

 if (JWT valido?) then (no)
   :401; stop
 else (si)
 endif

 if (Tiene close_user_session?) then (no)
   :403; :Audit UNAUTHORIZED_ACCESS_ATTEMPT;
   stop
 else (si)
 endif

 if (User existe?) then (no)
   :404; stop
 else (si)
 endif

 if (target_user == admin?) then (si)
   if (Setting permite?) then (no)
     :400 SELF_BULK_CLOSE_FORBIDDEN; stop
   else (si)
   endif
 else (no)
 endif

 :SELECT Sessions ACTIVE WHERE user=target;

 if (count == 0?) then (si)
   :Audit BULK_SESSION_CLOSE_NOOP;
   :200 OK count=0;
   stop
 else (no)
 endif

 partition "Transaccion atomica" {
   :UPDATE Sessions → CLOSED;
   :INSERT BlacklistedToken (N);
   :INSERT N AuditEvent SESSION_CLOSED;
   :INSERT 1 AuditEvent BULK_SESSION_CLOSE;
   if (Setting notify) then (si)
     :INSERT InternalMessage al User;
   else (no)
   endif
 }

 if (Transaccion OK?) then (no)
   :ROLLBACK;
   :500/503;
   stop
 else (si)
 endif

 :200 OK con count;
 :Frontend toast con count;

 stop

 @enduml

8.4 Diagrama de estados — Session (foco UC_AUTH_05)
===================================================

.. uml::
 :caption: Estados Session relevantes a UC_AUTH_05

 @startuml

 [*] --> ACTIVE : UC_AUTH_01

 ACTIVE --> CLOSED : UC_AUTH_05 (ADMIN_REVOKED)
 ACTIVE --> CLOSED : UC_AUTH_02 (USER_LOGOUT)
 ACTIVE --> CLOSED : CNST-004 (SUPERSEDED)
 ACTIVE --> CLOSED : CNST-005 (TIMEOUT)
 ACTIVE --> CLOSED : UC_AUTH_03 (PASSWORD_RESET)

 note right of CLOSED
   close_reason indica origen
   UC_AUTH_05 solo origina ADMIN_REVOKED
 end note

 CLOSED --> [*]

 @enduml
