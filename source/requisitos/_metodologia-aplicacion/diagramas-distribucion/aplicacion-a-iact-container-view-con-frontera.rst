Aplicación a IACT — Container view con frontera
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. uml::

   @startuml
   title IACT C4 — Container view con frontera

   actor "Supervisor\n[Person]" as Supervisor

   package "IACT" {
     rectangle "Browser\n[Navegador del supervisor]" as Browser <<c4_container>>
     rectangle "iact.wsgi\n[Django + mod_wsgi sobre Apache]" as WSGI <<c4_container>>
     database "Redis\n[Sesiones + throttling]" as Redis <<c4_container>>
     database "bd_analytics\n[MySQL]" as BDA <<c4_container>>
     database "audit_log\n[MySQL immutable]" as Audit <<c4_container>>
   }

   rectangle "ldap-corporativo\n[External]" as LDAP <<c4_externo>>
   database "bd-operativa\n[External, read-only]" as BDO <<c4_externo>>
   rectangle "ivr-host\n[External]" as IVR <<c4_externo>>

   Supervisor --> Browser : opera el panel
   Browser --> WSGI : consulta dashboards\n[HTTPS intranet]
   WSGI --> Redis : sesiones y throttling\n[Redis Protocol]
   WSGI --> BDA : lee/escribe analytics\n[MySQL TCP]
   WSGI --> Audit : registra eventos\n[MySQL TCP append-only]
   WSGI --> LDAP : autentica\n[LDAPS]
   WSGI --> BDO : lee llamadas\n[SQL read-only]
   WSGI --> IVR : recibe eventos\n[protocolo IVR]
   @enduml
