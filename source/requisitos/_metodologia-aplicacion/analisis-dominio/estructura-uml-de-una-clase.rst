2. Estructura UML de una clase
==============================

Una clase tiene 4 áreas: **nombre**, **atributos**,
**operaciones** y **responsabilidades**.

.. uml::

   @startuml

   class Call {
     - id : Integer
     - center_id : Integer
     - duration_sec : Integer
     - outcome : Enum
     + getDuration() : Integer
     + isAbandoned() : Boolean
     -- responsabilidades --
     Representar una llamada del IVR
     consumida por reportes y alertas.
   }
   note right of Call
     {duration_sec ≥ 0}
     {outcome ∈ ANSWERED |
                ABANDONED |
                TRANSFERRED}
   end note
   @enduml

**Convenciones:**

- **Nombre:** ``PascalCase`` (``Llamada``,
  ``EjecucionETL``, ``SegmentoDatos``).
- **Atributos:** ``camelCase`` con visibilidad ``-`` privado /
  ``+`` público / ``#`` protegido.
- **Operaciones:** ``camelCase`` con paréntesis y firma.
- **Restricciones:** entre llaves ``{…}`` en notas.
