Ejemplo IACT consolidado
~~~~~~~~~~~~~~~~~~~~~~~~

ERD del cluster RBAC (snapshot) con claves y
estereotipos completos:

.. uml::

   @startuml
   title IACT — ERD snapshot: cluster RBAC

   entity User {
     * user_id : int <<PK>>
     --
     * username : varchar(100) <<UQ>>
     * email : varchar(150) <<UQ>>
     active : boolean
     created_at : datetime
   }

   entity Group {
     * group_id : int <<PK>>
     --
     * name : varchar(50) <<UQ>>
     description : varchar(200)
     created_at : datetime
   }

   entity Function {
     * function_id : varchar(100) <<PK>>
     --
     * name : varchar(150)
     description : varchar(300)
     category : varchar(50) <<IDX>>
   }

   entity Assignment {
     * assignment_id : int <<PK>>
     --
     * user_id : int <<FK>>
     * group_id : int <<FK>>
     * start_date : datetime <<IDX>>
     end_date : datetime
     assigned_by : int <<FK>>
   }

   entity GroupFunction {
     * group_id : int <<PK>> <<FK>>
     * function_id : varchar(100) <<PK>> <<FK>>
     --
     assignment_date : datetime
     adr_approval : varchar(100)
   }

   User ||--o{ Assignment : is assigned in
   Group ||--o{ Assignment : contains
   Group ||--o{ GroupFunction : groups
   Function ||--o{ GroupFunction : is in
   @enduml

Lectura del schema:

- ``GrupoFuncion`` tiene una **PK compuesta** —
  el par ``(grupo_id, funcion_id)`` debe ser
  único; ambas son FK también.
- ``categoria`` en ``Funcion`` lleva ``<<IDX>>``
  porque ``perm_app`` consulta funciones por
  categoría con frecuencia.
- ``adr_aprobacion`` en ``GrupoFuncion`` permite
  rastrear la decisión que aprobó la asignación
  SoD (CNST_030 + auditoría a nivel del cluster).
- ``fecha_alta`` indexada en ``Asignacion``
  facilita reportes de "asignaciones del periodo".
