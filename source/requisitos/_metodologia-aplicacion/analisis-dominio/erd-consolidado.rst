ERD consolidado
~~~~~~~~~~~~~~~

.. uml::

   @startuml
   title IACT — ERD snapshot consolidado (2026-04-30)

   ' === RBAC ===
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

   entity ReglaSoD {
     * regla_id : int <<PK>>
     --
     * nombre : varchar(100) <<UQ>>
     descripcion : varchar(300)
   }

   entity ReglaSoDFuncion {
     * regla_id : int <<PK>> <<FK>>
     * funcion_id : varchar(100) <<PK>> <<FK>>
   }

   ' === ETL ===
   entity VentanaETL {
     * ventana_id : int <<PK>>
     --
     * inicio : datetime
     * fin : datetime
     estado : varchar(20)
   }

   entity EjecucionETL {
     * ejecucion_etl_id : int <<PK>>
     --
     * ventana_id : int <<FK>>
     usuario_id : int <<FK>>
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
   }

   entity RegistroIngesta {
     * ejecucion_etl_id : int <<PK>> <<FK>>
     * ingesta_seq : int <<PK>>
     --
     * tabla_destino : varchar(100)
     filas_insertadas : int
   }

   ' === Reportería ===
   entity Reporte {
     * reporte_id : int <<PK>>
     --
     * tipo : varchar(50)
     * nombre : varchar(150)
     creado_por : int <<FK>>
     creado_en : datetime
   }

   entity TareaExport {
     * tarea_id : int <<PK>>
     --
     * reporte_id : int <<FK>>
     * solicitado_por : int <<FK>>
     * estado : varchar(20)
     formato : varchar(10)
     solicitado_en : datetime
     completado_en : datetime
   }

   ' === Auditoría ===
   entity TipoEvento {
     * tipo_id : int <<PK>>
     --
     * nombre : varchar(50) <<UQ>>
   }

   entity EventoAuditoria {
     * evento_id : bigint <<PK>>
     --
     * usuario_id : int <<FK>>
     * tipo_id : int <<FK>>
     * timestamp : datetime <<IDX>>
     reporte_id : int <<FK>>
     ejecucion_etl_id : int <<FK>>
     payload : text
     ip_origen : varchar(45)
   }

   entity DetalleAuditoria {
     * evento_id : bigint <<PK>> <<FK>>
     * detalle_seq : int <<PK>>
     --
     * campo : varchar(100)
     valor_anterior : text
     valor_nuevo : text
   }

   ' === Relaciones RBAC ===
   Usuario ||..o{ Asignacion : "es asignado en"
   Grupo ||..o{ Asignacion : contiene
   Grupo ||--o{ GrupoFuncion : agrupa
   Funcion ||--o{ GrupoFuncion : "esta en"
   ReglaSoD ||--|{ ReglaSoDFuncion : restringe
   Funcion ||--o{ ReglaSoDFuncion : "aparece en"

   ' === Relaciones ETL ===
   VentanaETL ||..o{ EjecucionETL : "contiene (no-id)"
   EjecucionETL ||--o{ ErrorETL : "produce (id)"
   EjecucionETL ||--o{ RegistroIngesta : "produce (id)"
   Usuario ||..o{ EjecucionETL : "dispara (manual)"

   ' === Relaciones Reportería ===
   Usuario ||..o{ Reporte : crea
   Reporte ||..o{ TareaExport : "se exporta como"
   Usuario ||..o{ TareaExport : solicita

   ' === Relaciones Auditoría ===
   TipoEvento ||--o{ EventoAuditoria : clasifica
   Usuario ||..o{ EventoAuditoria : genera
   EventoAuditoria ||--o{ DetalleAuditoria : detalla
   Reporte ||..o{ EventoAuditoria : "origina (opcional)"
   EjecucionETL ||..o{ EventoAuditoria : "origina (opcional)"
   @enduml
