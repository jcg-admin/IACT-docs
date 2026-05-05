3. Vista física global de IACT
==============================

.. uml::

   @startuml
   skinparam componentStyle rectangle

   package "Cliente (navegador del supervisor)" {
     [iact-admin.bundle.js] as IactAdminBundleJs
   }

   package "Apache + mod_wsgi" {
     [iact.wsgi] as SERVIDOR_WSGI
     package "Apps Django" {
       [auth_app]
       [perm_app]
       [rpt_app]
       [alr_app]
       [pip_app]
       [aud_app]
       [log_app]
     }
   }

   package "Datos" {
     database "bd_operativa\n(read-only, CNST_007)" as BD_OPERATIVA
     database "bd_analytics" as BD_ANALYTICS
     database "audit_log\n(immutable, CNST_025)" as TABLA_AUDIT_LOG
     database "Redis\n(sesiones, throttling)" as CACHE_REDIS
   }

   package "Integraciones" {
     [LDAP_CORPORATIVO corporativo] as LDAP_CORPORATIVO
     [SISTEMA_IVR (read-only)] as SISTEMA_IVR
     [etl_runner.py] as SERVICIO_ETL
   }

   IactAdminBundleJs --> SERVIDOR_WSGI : HTTPS
   SERVIDOR_WSGI --> auth_app
   SERVIDOR_WSGI --> perm_app
   SERVIDOR_WSGI --> rpt_app
   SERVIDOR_WSGI --> alr_app
   SERVIDOR_WSGI --> aud_app
   SERVIDOR_WSGI --> log_app
   auth_app --> LDAP_CORPORATIVO
   auth_app --> CACHE_REDIS : sesion (CNST_002)
   perm_app --> aud_app : ISecurity → IAuditLog
   rpt_app --> BD_ANALYTICS : IDatosAnalytics
   rpt_app --> aud_app
   alr_app --> BD_ANALYTICS
   alr_app --> log_app : INotificacion
   pip_app --> SERVICIO_ETL
   SERVICIO_ETL --> BD_OPERATIVA : IDatosOperativos
   SERVICIO_ETL --> SISTEMA_IVR
   SERVICIO_ETL --> BD_ANALYTICS : IDatosAnalytics
   aud_app --> TABLA_AUDIT_LOG : IAuditLog
   @enduml
