ERD consolidado
~~~~~~~~~~~~~~~

.. uml::

   @startuml
   title IACT — ERD snapshot consolidado (2026-04-30)

   ' === RBAC ===
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

   entity SoDRule {
     * rule_id : int <<PK>>
     --
     * name : varchar(100) <<UQ>>
     description : varchar(300)
   }

   entity SoDRuleFunction {
     * rule_id : int <<PK>> <<FK>>
     * function_id : varchar(100) <<PK>> <<FK>>
   }

   ' === ETL ===
   entity ETLWindow {
     * window_id : int <<PK>>
     --
     * start : datetime
     * end : datetime
     state : varchar(20)
   }

   entity ETLExecution {
     * etl_execution_id : int <<PK>>
     --
     * window_id : int <<FK>>
     user_id : int <<FK>>
     * state : varchar(20)
     * start : datetime
     end : datetime
   }

   entity ETLError {
     * etl_execution_id : int <<PK>> <<FK>>
     * error_seq : int <<PK>>
     --
     * error_type : varchar(50)
     message : text
   }

   entity IngestRecord {
     * etl_execution_id : int <<PK>> <<FK>>
     * ingest_seq : int <<PK>>
     --
     * target_table : varchar(100)
     rows_inserted : int
   }

   ' === Reportería ===
   entity Report {
     * report_id : int <<PK>>
     --
     * type : varchar(50)
     * name : varchar(150)
     created_by : int <<FK>>
     created_at : datetime
   }

   entity ExportTask {
     * task_id : int <<PK>>
     --
     * report_id : int <<FK>>
     * requested_by : int <<FK>>
     * state : varchar(20)
     format : varchar(10)
     requested_at : datetime
     completed_at : datetime
   }

   ' === Auditoría ===
   entity EventType {
     * type_id : int <<PK>>
     --
     * name : varchar(50) <<UQ>>
   }

   entity AuditEvent {
     * event_id : bigint <<PK>>
     --
     * user_id : int <<FK>>
     * type_id : int <<FK>>
     * timestamp : datetime <<IDX>>
     report_id : int <<FK>>
     etl_execution_id : int <<FK>>
     payload : text
     source_ip : varchar(45)
   }

   entity AuditDetail {
     * event_id : bigint <<PK>> <<FK>>
     * detail_seq : int <<PK>>
     --
     * field : varchar(100)
     previous_value : text
     new_value : text
   }

   ' === Relaciones RBAC ===
   User ||..o{ Assignment : "is assigned in"
   Group ||..o{ Assignment : contains
   Group ||--o{ GroupFunction : groups
   Function ||--o{ GroupFunction : "is in"
   SoDRule ||--|{ SoDRuleFunction : restricts
   Function ||--o{ SoDRuleFunction : "appears in"

   ' === Relaciones ETL ===
   ETLWindow ||..o{ ETLExecution : "contains (no-id)"
   ETLExecution ||--o{ ETLError : "produces (id)"
   ETLExecution ||--o{ IngestRecord : "produces (id)"
   User ||..o{ ETLExecution : "triggers (manual)"

   ' === Relaciones Reportería ===
   User ||..o{ Report : creates
   Report ||..o{ ExportTask : "is exported as"
   User ||..o{ ExportTask : requests

   ' === Relaciones Auditoría ===
   EventType ||--o{ AuditEvent : classifies
   User ||..o{ AuditEvent : generates
   AuditEvent ||--o{ AuditDetail : details
   Report ||..o{ AuditEvent : "originates (optional)"
   ETLExecution ||..o{ AuditEvent : "originates (optional)"
   @enduml
