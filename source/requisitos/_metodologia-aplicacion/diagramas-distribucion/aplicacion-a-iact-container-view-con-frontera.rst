Aplicación a IACT — Container view con frontera
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. uml::

   @startuml
   title IACT C4 — Container view con frontera

   actor "Supervisor\n[Person]" as Supervisor

   package "IACT" {
     rectangle "Browser\n[Navegador del supervisor]" as Browser <<c4_container>>
     rectangle "iact.wsgi\n[Django + mod_wsgi sobre Apache]" as SERVIDOR_WSGI <<c4_container>>
     database "Redis\n[Sesiones + throttling]" as Redis <<c4_container>>
     database "bd_analytics\n[MySQL]" as BD_ANALYTICS <<c4_container>>
     database "audit_log\n[MySQL immutable]" as Audit <<c4_container>>
   }

   rectangle "ldap-corporativo\n[External]" as LDAP_CORPORATIVO <<c4_externo>>
   database "bd-operativa\n[External, read-only]" as BD_OPERATIVA <<c4_externo>>
   rectangle "ivr-host\n[External]" as SISTEMA_IVR <<c4_externo>>

   Supervisor --> Browser : opera el panel
   Browser --> SERVIDOR_WSGI : consulta dashboards\n[HTTPS intranet]
   SERVIDOR_WSGI --> Redis : sesiones y throttling\n[Redis Protocol]
   SERVIDOR_WSGI --> BD_ANALYTICS : lee/escribe analytics\n[MySQL TCP]
   SERVIDOR_WSGI --> Audit : registra eventos\n[MySQL TCP append-only]
   SERVIDOR_WSGI --> LDAP_CORPORATIVO : autentica\n[LDAPS]
   SERVIDOR_WSGI --> BD_OPERATIVA : lee llamadas\n[SQL read-only]
   SERVIDOR_WSGI --> SISTEMA_IVR : recibe eventos\n[protocolo SISTEMA_IVR]
   @enduml
