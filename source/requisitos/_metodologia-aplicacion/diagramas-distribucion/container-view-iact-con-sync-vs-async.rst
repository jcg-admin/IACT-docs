Container view IACT con sync vs async
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. uml::

   @startuml
   title IACT C4 — Container view (sync vs async)

   actor "Supervisor\n[Person]" as Supervisor

   package "IACT" {
     rectangle "Browser" as Browser <<c4_container>>
     rectangle "iact.wsgi\n[Django + mod_wsgi]" as SERVIDOR_WSGI <<c4_container>>
     database "Redis" as Redis <<c4_container>>
     database "bd_analytics\n[MySQL]" as BD_ANALYTICS <<c4_container>>
     database "audit_log\n[MySQL immutable]" as Audit <<c4_container>>
     rectangle "Worker Export\n[Django mgmt cmd]" as Worker <<c4_container>>
   }

   rectangle "ldap-corporativo" as LDAP_CORPORATIVO <<c4_externo>>
   database "bd-operativa" as BD_OPERATIVA <<c4_externo>>

   ' Sync (linea continua)
   Supervisor --> Browser
   Browser --> SERVIDOR_WSGI : consulta dashboards\n[HTTPS intranet]
   SERVIDOR_WSGI --> Redis : sesion / throttling\n[Redis Protocol]
   SERVIDOR_WSGI --> BD_ANALYTICS : lee/escribe analytics\n[MySQL TCP]
   SERVIDOR_WSGI ---> LDAP_CORPORATIVO : autentica\n[LDAPS]
   SERVIDOR_WSGI ---> BD_OPERATIVA : lee llamadas\n[SQL read-only]

   ' Async (linea punteada)
   SERVIDOR_WSGI ..> Audit : registra evento\n[in-process bus]
   SERVIDOR_WSGI ..> Worker : encola export\n[CNST_019]
   Worker ..> BD_ANALYTICS : lee agregados
   @enduml

Lectura del diagrama:

- **Sync** (``-->``): operaciones donde el
  ``iact.wsgi`` espera respuesta — render de UI,
  query de Redis, autenticación LDAP.
- **Async** (``..>``): operaciones donde el
  ``iact.wsgi`` no bloquea — registro de audit
  (CNST_025), encolado de export (CNST_019). El
  ``Worker Export`` luego procesa async leyendo
  ``bd_analytics``.
- La distinción visual ayuda a ingenieros y SRE a
  identificar **dónde puede haber latencia** y
  **dónde NO se debe esperar**.
