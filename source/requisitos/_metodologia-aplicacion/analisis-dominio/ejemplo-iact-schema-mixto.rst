Ejemplo IACT — schema mixto
~~~~~~~~~~~~~~~~~~~~~~~~~~~

ERD del cluster ETL combinando relaciones
identificantes y no-identificantes:

.. uml::

   @startuml
   title IACT — ERD snapshot: cluster ETL (mixto)

   entity VentanaETL {
     * ventana_id : int <<PK>>
     --
     * inicio : datetime
     * fin : datetime
   }

   entity EjecucionETL {
     * ejecucion_etl_id : int <<PK>>
     --
     * ventana_id : int <<FK>>
     * estado : varchar(20)
     * inicio : datetime
     fin : datetime
   }

   entity ErrorETL {
     * ejecucion_etl_id : int <<PK>> <<FK>>
     * error_seq : int <<PK>>
     --
     * tipo_error : varchar(50)
     mensaje : text
     timestamp : datetime
   }

   entity RegistroIngesta {
     * ejecucion_etl_id : int <<PK>> <<FK>>
     * ingesta_seq : int <<PK>>
     --
     * tabla_destino : varchar(100)
     filas_insertadas : int
   }

   ' No-identificante: la ejecucion sobrevive al
   ' cierre de la ventana
   VentanaETL ||..o{ EjecucionETL : "contiene (no-id)"

   ' Identificante: errores y registros mueren con
   ' la ejecucion
   EjecucionETL ||--o{ ErrorETL : "produce (id)"
   EjecucionETL ||--o{ RegistroIngesta : "produce (id)"
   @enduml

Lectura del schema:

- **``VentanaETL`` ↔ ``EjecucionETL``** — línea
  punteada: la ejecución tiene identidad propia
  (``ejecucion_etl_id``), aunque referencie su
  ventana. Si la ventana se invalida, las
  ejecuciones permanecen en ``audit_log``.
- **``EjecucionETL`` ↔ ``ErrorETL``** — línea
  continua: el error usa ``ejecucion_etl_id`` como
  parte de su PK (``(ejecucion_etl_id,
  error_seq)``). No hay error sin ejecución.
- **``EjecucionETL`` ↔ ``RegistroIngesta``** —
  igual: PK compuesta. Ingesta no existe sin
  ejecución que la produjo.
