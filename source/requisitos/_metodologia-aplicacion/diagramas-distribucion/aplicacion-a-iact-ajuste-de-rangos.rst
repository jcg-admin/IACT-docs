Aplicación a IACT — ajuste de rangos
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Para que los tres sistemas externos
(``ldap-corporativo``, ``bd-operativa``,
``ivr-host``) queden **debajo** de la frontera del
sistema en lugar de a la derecha, alargar las
flechas que cruzan la frontera:

.. uml::

   @startuml
   title IACT C4 — Container view (rangos ajustados)

   actor "Supervisor\n[Person]" as Supervisor

   package "IACT" {
     rectangle "Browser" as Browser <<c4_container>>
     rectangle "iact.wsgi" as WSGI <<c4_container>>
     database "Redis" as Redis <<c4_container>>
     database "bd_analytics" as BDA <<c4_container>>
     database "audit_log" as Audit <<c4_container>>
   }

   rectangle "ldap-corporativo" as LDAP <<c4_externo>>
   database "bd-operativa" as BDO <<c4_externo>>
   rectangle "ivr-host" as IVR <<c4_externo>>

   Supervisor --> Browser
   Browser --> WSGI
   WSGI --> Redis
   WSGI --> BDA
   WSGI --> Audit

   ' Flechas alargadas hacia externos: las empujan al
   ' siguiente rango (debajo del package).
   WSGI ---> LDAP : autentica\n[LDAPS]
   WSGI ---> BDO : lee llamadas\n[SQL read-only]
   WSGI ---> IVR : recibe eventos\n[protocolo IVR]
   @enduml

Lectura: las flechas con tres guiones (``--->``)
empujan a los sistemas externos un rango más abajo
que las flechas internas con dos guiones (``-->``).
Esto produce una vista más compacta donde los
externos quedan debajo de la frontera.
