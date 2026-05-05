Equivalente IACT — ``EjecucionETL`` y sus partes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Aplicada al dominio IACT, la entidad ``EjecucionETL``
juega el rol de ``Title``: tiene relaciones de distinto
tipo con sus vecinas.

.. uml::

   @startuml
   class EjecucionETL
   class VentanaETL
   class Llamada
   class ErrorETL
   class RegistroIngesta
   class DetalleError

   VentanaETL "1" -- "*" EjecucionETL : contiene
   EjecucionETL "1" *-- "*" ErrorETL : produce
   EjecucionETL "1" *-- "*" RegistroIngesta : produce
   EjecucionETL "*" -- "*" Llamada : carga
   ErrorETL "1" *-- "*" DetalleError : detalla
   @enduml

Lectura del diagrama:

- ``VentanaETL`` ↔ ``EjecucionETL`` — **asociación**.
  Las ventanas existen como conceptos del calendario
  aunque no haya ejecuciones aún.
- ``EjecucionETL`` ↔ ``Llamada`` — **asociación**. Las
  llamadas existen independientemente; una ejecución
  las **carga**, no las posee. Eliminada la ejecución
  (en el sentido del dominio), las llamadas siguen.
- ``EjecucionETL`` ↔ ``ErrorETL`` — **composición**. Un
  error solo tiene sentido si pertenece a una ejecución;
  invalidada la ejecución, el error como entidad de
  dominio desaparece (su rastro en ``audit_log``
  permanece, pero el objeto del dominio no).
- ``EjecucionETL`` ↔ ``RegistroIngesta`` — **composición**.
  Idéntica lógica: los registros de ingesta son partes
  internas de la ejecución.
- ``ErrorETL`` ↔ ``DetalleError`` — **composición** en
  segundo nivel. Análogo al ``Season`` ↔ ``Episode``
  del libro: el detalle no existe sin el error.
