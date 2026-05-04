Construcción incremental — IACT (continuación)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Paso 4**: conectar el actor con el sistema en
diseño.

.. uml::

   @startuml
   title IACT — paso 4: actor conectado al sistema

   actor "Supervisor\n[Person]" as Supervisor
   rectangle "IACT\n[Software System]" as IACT

   Supervisor --> IACT : consulta dashboards,\nreconoce alertas
   @enduml

**Paso 5**: agregar las dependencias del sistema en
diseño hacia los sistemas externos.

.. uml::

   @startuml
   title IACT — paso 5: con sistemas externos conectados

   actor "Supervisor\n[Person]" as Supervisor
   actor "Auditor\n[Person]" as Auditor
   actor "Operador ETL\n[Person]" as OETL

   rectangle "IACT\n[Software System]\n\nPlataforma de analitica\nde call center" as IACT

   rectangle "LDAP corporativo\n[External System]" as LDAP
   rectangle "BD operativa\n[External System]" as BDO
   rectangle "IVR-host\n[External System]" as IVR

   Supervisor --> IACT : consulta dashboards,\nreconoce alertas
   Auditor --> IACT : consulta auditoria,\nverifica SoD
   OETL --> IACT : monitorea ventana ETL

   IACT --> LDAP : autentica usuarios
   IACT --> BDO : lee datos del call center\n(read-only)
   IACT --> IVR : recibe eventos del IVR\n(read-only)
   @enduml

Resultado: el Context diagram completo, equivalente a
la imagen final de la sección "Vista Context de IACT"
de § 13. Cualquier colega técnico o no técnico puede
leerlo y entender quién usa IACT, qué hace y con qué
sistemas dialoga.
