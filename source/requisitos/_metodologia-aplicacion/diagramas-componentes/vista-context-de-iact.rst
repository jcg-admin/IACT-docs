Vista Context de IACT
---------------------

Aplicada al sistema completo de IACT, la vista
Context muestra el sistema como una sola caja que
interactúa con sus actores humanos y los sistemas
corporativos externos:

.. uml::

   @startuml
   title SISTEMA_IACT — Vista Context (C4 nivel 1)

   skinparam actorBackgroundColor #E0E7FF
   skinparam rectangleBackgroundColor<<sistema>> #C7D2FE
   skinparam rectangleBorderColor<<sistema>> #1E40AF
   skinparam rectangleBackgroundColor<<externo>> #E0F2F1

   actor Supervisor as Supervisor
   actor Auditor as Aud
   actor "Operador ETL" as OPERADOR_ETL

   rectangle "IACT\n(Plataforma de analitica\nde call center)" as SISTEMA_IACT <<sistema>>

   rectangle "LDAP corporativo" as LDAP_CORPORATIVO <<externo>>
   rectangle "BD operativa\n(call center)" as BD_OPERATIVA <<externo>>
   rectangle "IVR-host" as SISTEMA_IVR <<externo>>

   Supervisor --> SISTEMA_IACT : consulta dashboards,\nreconoce alertas
   Aud --> SISTEMA_IACT : consulta auditoria,\nverifica SoD
   OPERADOR_ETL --> SISTEMA_IACT : monitorea ventana ETL

   SISTEMA_IACT --> LDAP_CORPORATIVO : autentica usuarios
   SISTEMA_IACT --> BD_OPERATIVA : lee datos de llamadas\n(read-only)
   SISTEMA_IACT --> SISTEMA_IVR : lee eventos del SISTEMA_IVR\n(read-only)
   @enduml
