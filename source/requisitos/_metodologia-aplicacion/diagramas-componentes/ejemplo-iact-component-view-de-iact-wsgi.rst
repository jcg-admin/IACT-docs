14.2 Ejemplo IACT — Component view de iact.wsgi
-----------------------------------------------

El equivalente IACT del ejemplo del libro (componentes
del Web Application container) es la descomposición
de ``iact.wsgi`` en sus apps Django:

.. uml::

   @startuml
   title IACT C4 — Component view (iact.wsgi)

   actor "Supervisor\n[Person]" as Supervisor
   rectangle "Browser\n[Container]" as Browser <<c4_container>>

   package "iact.wsgi" {
     rectangle "auth_app\n[Django app]\nIdentificacion + sesion" as Auth <<c4_component>>
     rectangle "perm_app\n[Django app]\nPermisos + separacion de funciones" as Perm <<c4_component>>
     rectangle "rpt_app\n[Django app]\nReportes" as Rpt <<c4_component>>
     rectangle "alr_app\n[Django app]\nAlertas" as Alr <<c4_component>>
     rectangle "pip_app\n[Django app]\nETL coordinator" as Pip <<c4_component>>
     rectangle "aud_app\n[Django app]\nAuditoria CNST_025" as Aud <<c4_component>>
     rectangle "log_app\n[Django app]\nBuzon CNST_001" as Log <<c4_component>>
   }

   database "Redis\n[Container]" as Redis <<c4_container>>
   database "bd_analytics\n[Container]" as BD_ANALYTICS <<c4_container>>
   database "audit_log\n[Container]" as Audit <<c4_container>>
   rectangle "ldap-corporativo\n[External]" as LDAP_CORPORATIVO <<c4_externo>>

   Supervisor --> Browser
   Browser --> Auth : POST /login\n[HTTPS]
   Browser --> Rpt : consultas de reporte\n[HTTPS]
   Browser --> Alr : reconocer alerta\n[HTTPS]

   Auth --> LDAP_CORPORATIVO : autentica\n[LDAPS]
   Auth --> Redis : sesion (CNST_002)
   Auth ..> Aud : registra acceso

   Rpt --> Perm : verifica permiso
   Rpt --> BD_ANALYTICS : lee agregados
   Rpt ..> Log : notifica buzon
   Rpt ..> Aud : registra evento

   Alr --> Perm : verifica permiso
   Alr --> BD_ANALYTICS : evalua umbrales
   Alr ..> Aud : registra reconocimiento

   Pip --> BD_ANALYTICS : escribe agregados
   Pip ..> Aud : registra ejecucion ETL

   Perm ..> Aud : registra denegado / separacion
   @enduml

Lectura del diagrama
~~~~~~~~~~~~~~~~~~~~

- **Frontera ``iact.wsgi``** agrupa las siete apps
  Django.
- **Componentes** en azul claro
  (``<<c4_component>>``) — siete apps.
- **Containers IACT** fuera (Browser, Redis,
  bd_analytics, audit_log) en azul oscuro
  (``<<c4_container>>``).
- **Sistemas externos** (LDAP) en gris
  (``<<c4_externo>>``).
- **Sync** (``-->``) para llamadas que esperan
  respuesta.
- **Async** (``..>``) para registro de auditoría y
  notificaciones — fire-and-forget vía bus
  Observer.
