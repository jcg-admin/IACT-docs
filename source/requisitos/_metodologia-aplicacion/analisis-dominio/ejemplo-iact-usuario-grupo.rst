Ejemplo IACT — ``Usuario`` ↔ ``Grupo``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

En el modelo de dominio (§ 11 de
:doc:`agregacion-interfaces`):

- Un ``Usuario`` puede pertenecer a varios
  ``Grupo``.
- Un ``Grupo`` puede tener varios ``Usuario``.

Es una **agregación N:M**. En el dominio se
modela con una asociación bidireccional. En la
base relacional se requiere una **tabla
intermedia** ``Asignacion`` que materializa la
relación con la información adicional que el
dominio no captura (timestamp, quién hizo la
asignación, fecha de revisión SoD).

Schema correspondiente:

.. uml::

   @startuml
   title IACT — ERD snapshot: Usuario, Grupo y Asignacion

   entity Usuario {
     * usuario_id : int <<PK>>
     --
     * username : varchar(100)
     * email : varchar(150)
     activo : boolean
   }

   entity Grupo {
     * grupo_id : int <<PK>>
     --
     * nombre : varchar(50)
     descripcion : varchar(200)
   }

   entity Asignacion {
     * asignacion_id : int <<PK>>
     --
     * usuario_id : int <<FK>>
     * grupo_id : int <<FK>>
     * fecha_alta : datetime
     fecha_baja : datetime
     asignado_por : int <<FK>>
   }

   Usuario ||--o{ Asignacion : "es asignado en"
   Grupo ||--o{ Asignacion : "contiene"
   @enduml

Lectura del ERD:

- ``Usuario`` y ``Grupo`` son las entidades
  principales.
- ``Asignacion`` es la **tabla de unión**:
  resuelve la relación N:M en una base relacional.
- Cada lado de la N:M se descompone en
  **dos relaciones 1:N** hacia la tabla
  intermedia.
- ``Asignacion`` agrega información que **no está
  en el modelo de dominio**: cuándo se hizo la
  asignación, cuándo se dio de baja, quién la
  asignó (auditoría a nivel del cluster).
