2. Vista de despliegue global IACT
==================================

.. uml::

   @startuml

   node "puesto-supervisor\n<<computadora>>" as PuestoSupervisor {
     artifact "Navegador (intranet)" as NavegadorIntranet
   }

   node "vm-iact\n<<servidor>>" as VmIact {
     node "Apache + mod_wsgi" as APACHE {
       artifact "iact.wsgi" as WSGI
       artifact "auth_app, perm_app,\nrpt_app, alr_app,\npip_app, aud_app, log_app" as APPS
     }
     node "Redis" as REDIS
     database "bd_analytics\n(MySQL)" as BDA
     database "audit_log\n(MySQL,\nimmutable CNST_025)" as AUDIT
     artifact "etl_runner.py\n(cron, ventana\nCNST_006/008)" as ETL
     artifact "iact-admin.bundle.js" as UIBUNDLE
   }

   node "ldap-corporativo\n<<servidor>>" as LDAP

   database "bd-operativa\n(read-only,\nCNST_007)" as BDO

   node "ivr-host\n<<servidor>>" as IVR

   NavegadorIntranet -down-> APACHE : HTTPS (intranet)
   APACHE -down-> UIBUNDLE : sirve estaticos
   APPS -right-> REDIS : sesiones (CNST_002)\nthrottling (CNST_011)
   APPS -down-> BDA : lectura/escritura
   APPS -down-> AUDIT : append-only
   APPS -right-> LDAP : LDAPS (auth)
   ETL -left-> BDO : SQL read-only
   ETL -left-> IVR : protocolo IVR
   ETL -down-> BDA : insert agregados
   @enduml
