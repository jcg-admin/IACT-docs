Construcción incremental — IACT
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Paso 1**: declarar el primer actor.

.. uml::

   @startuml
   title IACT — paso 1: actor

   actor "Supervisor\n[Person]\n\nMonitorea llamadas\ny reportes" as Supervisor
   @enduml

**Paso 2**: agregar el sistema en diseño.

.. uml::

   @startuml
   title SISTEMA_IACT — paso 2: actor + sistema

   actor "Supervisor\n[Person]\n\nMonitorea llamadas\ny reportes" as Supervisor

   rectangle "IACT\n[Software System]\n\nPlataforma de analitica\nde call center" as SISTEMA_IACT
   @enduml

**Paso 3**: agregar sistemas externos.

.. uml::

   @startuml
   title SISTEMA_IACT — paso 3: con sistemas externos

   actor "Supervisor\n[Person]\n\nMonitorea llamadas\ny reportes" as Supervisor

   rectangle "IACT\n[Software System]\n\nPlataforma de analitica\nde call center" as SISTEMA_IACT

   rectangle "LDAP corporativo\n[External System]\n\nDirectorio de usuarios" as LDAP_CORPORATIVO
   rectangle "BD operativa\n[External System]\n\nDatos del call center\n(read-only)" as BD_OPERATIVA
   rectangle "IVR-host\n[External System]\n\nEventos de telefonia\n(read-only)" as SISTEMA_IVR
   @enduml

En este punto los nodos están aislados; el siguiente
paso (subsección siguiente) es **conectarlos** con
flechas etiquetadas.
