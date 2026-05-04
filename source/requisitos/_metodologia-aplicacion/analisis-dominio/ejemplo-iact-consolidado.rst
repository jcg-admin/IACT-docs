Ejemplo IACT consolidado
~~~~~~~~~~~~~~~~~~~~~~~~

ERD del cluster RBAC (snapshot) con claves y
estereotipos completos:

.. uml::

   @startuml
   title IACT — ERD snapshot: cluster RBAC

   entity Usuario {
     * usuario_id : int <<PK>>
     --
     * username : varchar(100) <<UQ>>
     * email : varchar(150) <<UQ>>
     activo : boolean
     creado_en : datetime
   }

   entity Grupo {
     * grupo_id : int <<PK>>
     --
     * nombre : varchar(50) <<UQ>>
     descripcion : varchar(200)
     creado_en : datetime
   }

   entity Funcion {
     * funcion_id : varchar(100) <<PK>>
     --
     * nombre : varchar(150)
     descripcion : varchar(300)
     categoria : varchar(50) <<IDX>>
   }

   entity Asignacion {
     * asignacion_id : int <<PK>>
     --
     * usuario_id : int <<FK>>
     * grupo_id : int <<FK>>
     * fecha_alta : datetime <<IDX>>
     fecha_baja : datetime
     asignado_por : int <<FK>>
   }

   entity GrupoFuncion {
     * grupo_id : int <<PK>> <<FK>>
     * funcion_id : varchar(100) <<PK>> <<FK>>
     --
     fecha_asignacion : datetime
     adr_aprobacion : varchar(100)
   }

   Usuario ||--o{ Asignacion : es asignado en
   Grupo ||--o{ Asignacion : contiene
   Grupo ||--o{ GrupoFuncion : agrupa
   Funcion ||--o{ GrupoFuncion : esta en
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
