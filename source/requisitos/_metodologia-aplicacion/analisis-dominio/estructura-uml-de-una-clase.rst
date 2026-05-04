2. Estructura UML de una clase
==============================

Una clase tiene 4 áreas: **nombre**, **atributos**,
**operaciones** y **responsabilidades**.

.. uml::

   @startuml

   class Llamada {
     - id : Integer
     - centro_id : Integer
     - duracion_seg : Integer
     - resultado : Enum
     + getDuracion() : Integer
     + esAbandonada() : Boolean
     -- responsabilidades --
     Representar una llamada del IVR
     consumida por reportes y alertas.
   }
   note right of Llamada
     {duracion_seg ≥ 0}
     {resultado ∈ ATENDIDA |
                  ABANDONADA |
                  TRANSFERIDA}
   end note
   @enduml

**Convenciones:**

- **Nombre:** ``PascalCase`` (``Llamada``,
  ``EjecucionETL``, ``SegmentoDatos``).
- **Atributos:** ``camelCase`` con visibilidad ``-`` privado /
  ``+`` público / ``#`` protegido.
- **Operaciones:** ``camelCase`` con paréntesis y firma.
- **Restricciones:** entre llaves ``{…}`` en notas.

----
