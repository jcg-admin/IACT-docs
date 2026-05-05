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
     rectangle "iact.wsgi" as SERVIDOR_WSGI <<c4_container>>
     database "Redis" as Redis <<c4_container>>
     database "bd_analytics" as BD_ANALYTICS <<c4_container>>
     database "audit_log" as Audit <<c4_container>>
   }

   rectangle "ldap-corporativo" as LDAP_CORPORATIVO <<c4_externo>>
   database "bd-operativa" as BD_OPERATIVA <<c4_externo>>
   rectangle "ivr-host" as SISTEMA_IVR <<c4_externo>>

   Supervisor --> Browser
   Browser --> SERVIDOR_WSGI
   SERVIDOR_WSGI --> Redis
   SERVIDOR_WSGI --> BD_ANALYTICS
   SERVIDOR_WSGI --> Audit

   ' Flechas alargadas hacia externos: las empujan al
   ' siguiente rango (debajo del package).
   SERVIDOR_WSGI ---> LDAP_CORPORATIVO : autentica\n[LDAPS]
   SERVIDOR_WSGI ---> BD_OPERATIVA : lee llamadas\n[SQL read-only]
   SERVIDOR_WSGI ---> SISTEMA_IVR : recibe eventos\n[protocolo SISTEMA_IVR]
   @enduml

Lectura: las flechas con tres guiones (``--->``)
empujan a los sistemas externos un rango más abajo
que las flechas internas con dos guiones (``-->``).
Esto produce una vista más compacta donde los
externos quedan debajo de la frontera.
