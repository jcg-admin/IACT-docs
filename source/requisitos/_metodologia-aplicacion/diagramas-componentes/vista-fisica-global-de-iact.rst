3. Vista física global de IACT
==============================

.. uml::

   @startuml
   skinparam componentStyle rectangle

   package "Cliente (navegador del supervisor)" {
     [iact-admin.bundle.js] as IactAdminBundleJs
   }

   package "Apache + mod_wsgi" {
     [iact.wsgi] as WSGI
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
     database "bd_operativa\n(read-only, CNST_007)" as BDO
     database "bd_analytics" as BDA
     database "audit_log\n(immutable, CNST_025)" as AUDIT
     database "Redis\n(sesiones, throttling)" as REDIS
   }

   package "Integraciones" {
     [LDAP corporativo] as LDAP
     [IVR (read-only)] as IVR
     [etl_runner.py] as ETL
   }

   IactAdminBundleJs --> WSGI : HTTPS
   WSGI --> auth_app
   WSGI --> perm_app
   WSGI --> rpt_app
   WSGI --> alr_app
   WSGI --> aud_app
   WSGI --> log_app
   auth_app --> LDAP
   auth_app --> REDIS : sesion (CNST_002)
   perm_app --> aud_app : ISecurity → IAuditLog
   rpt_app --> BDA : IDatosAnalytics
   rpt_app --> aud_app
   alr_app --> BDA
   alr_app --> log_app : INotificacion
   pip_app --> ETL
   ETL --> BDO : IDatosOperativos
   ETL --> IVR
   ETL --> BDA : IDatosAnalytics
   aud_app --> AUDIT : IAuditLog
   @enduml
