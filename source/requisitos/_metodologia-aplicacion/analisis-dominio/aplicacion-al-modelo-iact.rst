Aplicación al modelo IACT
~~~~~~~~~~~~~~~~~~~~~~~~~

Modelo IACT consolidado con multiplicidad anclada a las
reglas del dominio:

.. uml::

   @startuml

   class Llamada
   class Segmento
   class EjecucionETL
   class VentanaETL
   class ErrorETL
   class Reporte
   class Filtro
   class Alerta
   class Supervisor
   class Usuario
   class Sesion
   class Grupo
   class Funcion
   class EventoAuditoria
   class ReglaSoD

   Llamada "1..*" -- "1" Segmento : pertenece a
   VentanaETL "1" -- "0..*" EjecucionETL : contiene
   EjecucionETL "1..*" -- "0..*" Llamada : carga
   EjecucionETL "1" *-- "0..*" ErrorETL : produce
   Reporte "1..*" -- "0..*" Llamada : agrega
   Reporte "1" o-- "0..*" Filtro : aplica
   Alerta "0..*" -- "0..1" Supervisor : es reconocida por
   Sesion "1" *-- "1" Usuario : pertenece a
   Usuario "0..*" o-- "0..*" Grupo : asignado a
   Grupo "1..*" o-- "0..*" Funcion : agrupa
   Usuario "1" --> "0..*" EventoAuditoria : genera
   ReglaSoD "0..*" -- "2..3" Funcion : restringe
   @enduml
