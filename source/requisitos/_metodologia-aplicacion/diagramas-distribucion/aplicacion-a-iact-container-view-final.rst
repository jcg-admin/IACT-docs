Aplicación a IACT — Container view final
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

El equivalente IACT de la vista final del libro
(con todos los sistemas de apoyo agregados):

.. uml::

   @startuml
   title IACT C4 — Container view (final)

   actor "Supervisor\n[Person]" as Supervisor

   package "IACT" {
     rectangle "Browser\n[Navegador del supervisor]" as Browser <<c4_container>>
     rectangle "iact.wsgi\n[Django + mod_wsgi sobre Apache]" as WSGI <<c4_container>>
     database "Redis\n[Sesiones + throttling]" as Redis <<c4_container>>
     database "bd_analytics\n[MySQL]" as BDA <<c4_container>>
     database "audit_log\n[MySQL immutable]" as Audit <<c4_container>>
   }

   together {
     rectangle "ldap-corporativo\n[External]" as LDAP <<c4_externo>>
     database "bd-operativa\n[External, read-only]" as BDO <<c4_externo>>
     rectangle "ivr-host\n[External]" as IVR <<c4_externo>>
   }

   Supervisor -down-> Browser : opera el panel
   Browser -down-> WSGI : consulta dashboards\n[HTTPS intranet]
   WSGI -down-> Redis : sesiones y throttling\n[Redis Protocol]
   WSGI -down-> BDA : lee/escribe analytics\n[MySQL TCP]
   WSGI -down-> Audit : registra eventos\n[MySQL TCP append-only]

   WSGI -right-> LDAP : autentica\n[LDAPS]
   WSGI -right-> BDO : lee llamadas\n[SQL read-only]
   WSGI -right-> IVR : recibe eventos\n[protocolo IVR]
   @enduml

Decisiones de layout aplicadas:

- **``together { ... }``** agrupa los tres sistemas
  externos para que aparezcan juntos.
- **``-down->``** para flechas internas verticales.
- **``-right->``** para flechas hacia los sistemas
  externos — los empuja a la derecha sin que se
  dispersen.

Si el renderer aún produce un diagrama demasiado
ancho, alternativa: usar ``left to right direction``
al inicio para reorganizar todo el diagrama
horizontalmente.
