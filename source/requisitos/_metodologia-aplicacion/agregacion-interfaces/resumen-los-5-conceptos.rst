9. Resumen — los 5 conceptos
============================

.. uml::

   @startuml
   allowmixing

   skinparam packageStyle rectangle
   rectangle "Modelo UML completo (IACT)" as ModeloUmlCompletoIact {
     rectangle "1. AGREGACIÓN ◇\nGrupo ↔ Funcion\nCentro ↔ Operador"               as 1AgregaciN
     rectangle "2. COMPOSICIÓN ●\nEjecucionETL ↔ ErrorETL\nReporte ↔ Fila"          as 2ComposiciN
     rectangle "3. INTERFACES\nIExportable, INotificable,\nISegmentable"            as 3Interfaces
     rectangle "4. VISIBILIDAD\n+ público / # protegido / − privado"                as 4Visibilidad
     rectangle "5. ÁMBITO\nInstancia vs archivador\n(ConfiguracionSLA = static)"    as 5Mbito
   }
   @enduml

----
