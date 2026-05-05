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
     Sessionservice -> BaseDeDatos: consultar Session para actualizar
     BaseDeDatos --> Sessionservice: session
     alt Ya CLOSED (FA-02)
       Sessionservice -> BaseDeDatos: registrar AuditEvent SESSION_CLOSE_NOOP
       Sessionservice --> Closesessionview: noop
     else ACTIVE
       Sessionservice -> BaseDeDatos: actualizar Session SET\n  state='CLOSED',\n  close_reason='ADMIN_REVOKED',\n  closed_by_admin_id=admin.id
       Sessionservice -> BaseDeDatos: registrar BlacklistedToken
       Sessionservice -> BaseDeDatos: registrar AuditEvent SESSION_CLOSED
       opt NOTIFY_USER_ON_ADMIN_SESSION_CLOSE
         Sessionservice -> BaseDeDatos: registrar InternalMessage
       end
     end
   end

   Sessionservice --> Closesessionview: result
   Closesessionview --> Frontend: 200 OK
   Frontend --> Admin: Toast confirmacion
 end

 @enduml

