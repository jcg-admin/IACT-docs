Ejemplo IACT — diagrama limpio sin compartimentos
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Aplicando ``hide empty members``:

.. uml::

   @startuml
   title Modelo de dominio IACT — vista compacta

   hide empty members

   class Llamada
   class Segmento
   class EjecucionETL
   class Reporte
   class Usuario
   class Sesion
   class EventoAuditoria

   Llamada "1..*" -- "1" Segmento : pertenece a
   EjecucionETL "1..*" -- "0..*" Llamada : carga
   Reporte "1..*" -- "0..*" Llamada : agrega
   Sesion "1" *-- "1" Usuario : pertenece a
   Usuario "1" --> "0..*" EventoAuditoria : genera
   @enduml

Las cajas son más compactas: solo aparece el nombre de
la entidad, sin compartimentos vacíos.
