2. Vista de despliegue global IACT
==================================

.. uml::

   @startuml

   node "puesto-supervisor\n<<computadora>>" as PuestoSupervisor {
     artifact "Navegador (intranet)" as NavegadorIntranet
   }

   node "vm-iact\n<<servidor>>" as VmIact {
     node "Apache + mod_wsgi" as APACHE {
       artifact "iact.wsgi" as SERVIDOR_WSGI
       artifact "auth_app, perm_app,\nrpt_app, alr_app,\npip_app, aud_app, log_app" as MODULOS_DJANGO
     }
     node "Redis" as CACHE_REDIS
     database "bd_analytics\n(MySQL)" as BD_ANALYTICS
     database "audit_log\n(MySQL,\nimmutable CNST_025)" as TABLA_AUDIT_LOG
     artifact "etl_runner.py\n(cron, ventana\nCNST_006/008)" as SERVICIO_ETL
     artifact "iact-admin.bundle.js" as UIBUNDLE
   }

   node "ldap-corporativo\n<<servidor>>" as LDAP_CORPORATIVO

   database "bd-operativa\n(read-only,\nCNST_007)" as BD_OPERATIVA

   node "ivr-host\n<<servidor>>" as SISTEMA_IVR

   NavegadorIntranet -down-> APACHE : HTTPS (intranet)
   APACHE -down-> UIBUNDLE : sirve estaticos
   MODULOS_DJANGO -right-> CACHE_REDIS : sesiones (CNST_002)\nthrottling (CNST_011)
   MODULOS_DJANGO -down-> BD_ANALYTICS : lectura/escritura
   MODULOS_DJANGO -down-> TABLA_AUDIT_LOG : append-only
   MODULOS_DJANGO -right-> LDAP_CORPORATIVO : LDAPS (auth)
   SERVICIO_ETL -left-> BD_OPERATIVA : SQL read-only
   SERVICIO_ETL -left-> SISTEMA_IVR : protocolo SISTEMA_IVR
   SERVICIO_ETL -down-> BD_ANALYTICS : insert agregados
   @enduml
