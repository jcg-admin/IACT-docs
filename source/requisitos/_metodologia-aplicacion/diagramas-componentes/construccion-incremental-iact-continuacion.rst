Construcción incremental — IACT (continuación)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Paso 4**: conectar el actor con el sistema en
diseño.

.. uml::

   @startuml
   title SISTEMA_IACT — paso 4: actor conectado al sistema

   actor "Supervisor\n[Person]" as Supervisor
   rectangle "IACT\n[Software System]" as SISTEMA_IACT

   Supervisor --> SISTEMA_IACT : consulta dashboards,\nreconoce alertas
   @enduml

**Paso 5**: agregar las dependencias del sistema en
diseño hacia los sistemas externos.

.. uml::

   @startuml
   title SISTEMA_IACT — paso 5: con sistemas externos conectados

   actor "Supervisor\n[Person]" as Supervisor
   actor "Auditor\n[Person]" as Auditor
   actor "Operador ETL\n[Person]" as OPERADOR_ETL

   rectangle "IACT\n[Software System]\n\nPlataforma de analitica\nde call center" as SISTEMA_IACT

   rectangle "LDAP corporativo\n[External System]" as LDAP_CORPORATIVO
   rectangle "BD operativa\n[External System]" as BD_OPERATIVA
   rectangle "IVR-host\n[External System]" as SISTEMA_IVR

   Supervisor --> SISTEMA_IACT : consulta dashboards,\nreconoce alertas
   Auditor --> SISTEMA_IACT : consulta auditoria,\nverifica separacion
   OPERADOR_ETL --> SISTEMA_IACT : monitorea ventana ETL

   SISTEMA_IACT --> LDAP_CORPORATIVO : autentica usuarios
   SISTEMA_IACT --> BD_OPERATIVA : lee datos del call center\n(read-only)
   SISTEMA_IACT --> SISTEMA_IVR : recibe eventos del SISTEMA_IVR\n(read-only)
   @enduml

Resultado: el Context diagram completo, equivalente a
la imagen final de la sección "Vista Context de IACT"
de § 13. Cualquier colega técnico o no técnico puede
leerlo y entender quién usa IACT, qué hace y con qué
sistemas dialoga.
