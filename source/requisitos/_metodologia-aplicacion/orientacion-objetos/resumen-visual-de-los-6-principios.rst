8. Resumen visual de los 6 principios
=====================================

.. uml::

   @startuml

   skinparam packageStyle rectangle
   rectangle "Orientación a Objetos en IACT" as OOP {
     rectangle "1. ABSTRACCIÓN\nLlamada / Métrica / Función\nsin ruido físico"             as 1AbstracciN
     rectangle "2. HERENCIA\nUsuario → Operador,\nSupervisor, Auditor..."                  as 2Herencia
     rectangle "3. POLIMORFISMO\ncalcularValor() por métrica\nexportar() por formato"      as 3Polimorfismo
     rectangle "4. ENCAPSULAMIENTO\ngenerar() público,\nsegmentación interna"              as 4Encapsulamiento
     rectangle "5. MENSAJES\nOperador → Dashboard\n→ Reporte → SecRules → BD"              as 5Mensajes
     rectangle "6. ASOCIACIONES\nUsuario 1:1 Sesion;\nGrupo *:* Funcion (agregación);\nEjecucionETL 1:* ErrorETL (composición)" as 6Asociaciones
   }
   @enduml
