8.3 Diagrama de actividad
=========================

Vista del control de flujo con bifurcaciones por
las distintas excepciones y flujos alternos.

.. uml::
 :caption: UC_AUTH_01 — flujo de control con decisiones

 @startuml

 start

 :Recibir POST /api/auth/login/;
 :Validar Serializer;
 if (formato OK?) then (no)
   :Responder 400\nVALIDATION_ERROR;
   stop
 endif

 :Aplicar throttling CNST-011;
 if (dentro de limite?) then (no)
   :Responder 429\nRATE_LIMITED;
   :Emitir AuditEvent\nLOGIN_THROTTLED;
   stop
 endif

 :Buscar User por username;
 if (User existe?) then (no)
   :Responder 401\nINVALID_CREDENTIALS;
   :Emitir AuditEvent\nLOGIN_FAILED;
   stop
 endif

 if (User.state == BLOCKED?) then (si)
   :Responder 403\nACCOUNT_BLOCKED;
   :Emitir AuditEvent\nLOGIN_BLOCKED;
   stop
 endif

 if (User.state == INACTIVE?) then (si)
   :Responder 403\nACCOUNT_INACTIVE;
   :Emitir AuditEvent\nLOGIN_INACTIVE;
   stop
 endif

 :Verificar password (hash criptografico);
 if (password correcto?) then (no)
   :Responder 401\nINVALID_CREDENTIALS;
   :Emitir AuditEvent\nLOGIN_FAILED;
   stop
 endif

 :BEGIN TRANSACTION;
 :Cerrar Sessions ACTIVE\ndel User (CNST-004);
 :Crear Session nueva\n(CNST-003, CNST-005);
 :Emitir AuditEvent LOGIN\n(CNST-025);
 :Actualizar User.last_login_at;

 if (BD ok?) then (no)
   :ROLLBACK;
   :Responder 503\nDB_TRANSIENT_ERROR;
   stop
 endif

 :COMMIT;

 :Generar tokens JWT;

 if (User.first_login?) then (si)
   :Responder 200 con\nnext_step="change_password";
   :Frontend redirige\na UC_AUTH_04;
 elseif (password proximo\na expirar?) then (si)
   :Responder 200 con\nwarning password_expiring;
   :Frontend muestra modal\nopcional UC_AUTH_04;
 else (no)
   :Responder 200 con\ntokens y user;
   :Frontend redirige\nal landing;
 endif

 stop

 @enduml

