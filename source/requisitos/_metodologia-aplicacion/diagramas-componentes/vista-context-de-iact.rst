Vista Context de IACT
---------------------

Aplicada al sistema completo de IACT, la vista
Context muestra el sistema como una sola caja que
interactúa con sus actores humanos y los sistemas
corporativos externos:

.. uml::

   @startuml
   title IACT — Vista Context (C4 nivel 1)

   skinparam actorBackgroundColor #E0E7FF
   skinparam rectangleBackgroundColor<<sistema>> #C7D2FE
   skinparam rectangleBorderColor<<sistema>> #1E40AF
   skinparam rectangleBackgroundColor<<externo>> #E0F2F1

   actor Supervisor as Supervisor
   actor Auditor as Aud
   actor "Operador ETL" as OETL

   rectangle "IACT\n(Plataforma de analitica\nde call center)" as IACT <<sistema>>

   rectangle "LDAP corporativo" as LDAP <<externo>>
   rectangle "BD operativa\n(call center)" as BDO <<externo>>
   rectangle "IVR-host" as IVR <<externo>>

   Supervisor --> IACT : consulta dashboards,\nreconoce alertas
   Aud --> IACT : consulta auditoria,\nverifica SoD
   OETL --> IACT : monitorea ventana ETL

   IACT --> LDAP : autentica usuarios
   IACT --> BDO : lee datos de llamadas\n(read-only)
   IACT --> IVR : lee eventos del IVR\n(read-only)
   @enduml
