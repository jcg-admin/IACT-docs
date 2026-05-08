Ejemplo IACT — ``Usuario`` ↔ ``Grupo``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

En el modelo de dominio (§ 11 de
:doc:`/requisitos/_metodologia-aplicacion/agregacion-interfaces/index`):

- Un ``Usuario`` puede pertenecer a varios
  ``Grupo``.
- Un ``Grupo`` puede tener varios ``Usuario``.

Es una **agregación N:M**. En el dominio se
modela con una asociación bidireccional. En la
base relacional se requiere una **tabla
intermedia** ``Asignacion`` que materializa la
relación con la información adicional que el
dominio no captura (timestamp, quién hizo la
asignación, fecha de revisión de separacion).

Schema correspondiente:

.. uml::

   @startuml
   title IACT — ERD snapshot: User, Group y Assignment

   entity User {
     * user_id : int <<PK>>
     --
     * username : varchar(100)
     * email : varchar(150)
     active : boolean
   }

   entity Group {
     * group_id : int <<PK>>
     --
     * name : varchar(50)
     description : varchar(200)
   }

   entity Assignment {
     * assignment_id : int <<PK>>
     --
     * user_id : int <<FK>>
     * group_id : int <<FK>>
     * start_date : datetime
     end_date : datetime
     assigned_by : int <<FK>>
   }

   User ||--o{ Assignment : "is assigned in"
   Group ||--o{ Assignment : "contains"
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
