2. Diagrama de objetos — instancia concreta de llamada
======================================================

.. uml::

   @startuml

   object "llamada_001 : Llamada" as Llamada001Llamada {
     id = 4732112
     centro_id = 7
     campana_id = 22
     servicio_id = 3
     tipo = "INBOUND"
     duracion_seg = 184
     tiempo_espera_seg = 23
     resultado = "ATENDIDA"
     fecha = "2026-04-29 10:14:32"
   }
   @enduml

**Aplicación:** los casos de prueba de UC_RPT y UC_ALR deben
usar instancias concretas como ésta.
