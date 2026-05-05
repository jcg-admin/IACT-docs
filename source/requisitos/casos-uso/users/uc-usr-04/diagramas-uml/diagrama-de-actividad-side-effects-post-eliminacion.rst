8.5 Diagrama de actividad — side-effects post-eliminacion
=========================================================

.. uml::
 :caption: Que pasa cuando el User intenta usar tokens o iniciar
           sesion despues de UC_USR_04

 @startuml

 start

 :User eliminado intenta operacion;

 if (Tiene token activo (cached)?) then (si)
   :GET /api/{cualquier}/;
   :Middleware verifica blacklist;
   :Token blacklisteado;
   :401 INVALID_TOKEN; stop
 else (no — intenta nuevo login)
 endif

 :POST /api/auth/login/;
 :Servicio de Autenticacion busca usuario por username;

 if (User.state == ELIMINATED?) then (si)
   :401 ACCOUNT_ELIMINATED;
   :Audit LOGIN_FAILED
    {reason:'account_eliminated',
     user_state:'ELIMINATED'};
   stop
 endif

 stop

 @enduml
