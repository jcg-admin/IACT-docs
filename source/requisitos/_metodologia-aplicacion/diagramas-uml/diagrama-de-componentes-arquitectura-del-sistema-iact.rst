8. Diagrama de componentes — arquitectura del sistema IACT
==========================================================

.. uml::

   @startuml

   package "Frontend (React + Webpack)" {
     component "UI Components\nDashboards, Reportes" as UiComponents
     component "Redux Store\nState Management"      as Redux
     component "HTTP Client\nAxios + JWT"           as CLIENTE_HTTP
   }

   package "Backend (Django + DRF)" {
     component "REST API\nViewSets"                  as API_REST_DJANGO
     component "Auth Service\nJWT, Sessions"         as Auth
     component "RBAC Service\nFunciones, Grupos"     as SERVICIO_RBAC
     component "Reports Service\nMétricas, Export"   as SERVICIO_REPORTES
     component "Alerts Service\nUmbrales, Notif"     as SERVICIO_ALERTAS
     component "ETL Supervisor\nestado, reintento"   as SERVICIO_ETL
     component "Audit Service\nInmutable"            as SERVICIO_AUDITORIA
   }

   database "MySQL Analytics\nDatos IVR + RBAC + Audit" as MysqlAnalytics

   package "Infraestructura externa" {
     component "IVR Conmutador\n(read-only)" as SISTEMA_IVR
     component "Scheduler\nAPScheduler"      as Sched
     component "Buzón Interno\n(no email)"   as Buzon
   }

   UiComponents    --> Redux : state
   UiComponents    --> CLIENTE_HTTP  : fetch / post
   CLIENTE_HTTP  --> API_REST_DJANGO  : API_REST_DJANGO + JWT

   API_REST_DJANGO  --> Auth : usa
   API_REST_DJANGO  --> SERVICIO_RBAC : usa
   API_REST_DJANGO  --> SERVICIO_REPORTES  : usa
   API_REST_DJANGO  --> SERVICIO_ALERTAS  : usa
   API_REST_DJANGO  --> SERVICIO_ETL  : usa
   API_REST_DJANGO  --> SERVICIO_AUDITORIA  : usa

   Auth --> MysqlAnalytics : queries
   SERVICIO_RBAC --> MysqlAnalytics : queries
   SERVICIO_REPORTES  --> MysqlAnalytics : queries
   SERVICIO_ALERTAS  --> MysqlAnalytics : queries
   SERVICIO_ETL  --> MysqlAnalytics : queries
   SERVICIO_AUDITORIA  --> MysqlAnalytics : append-only

   SERVICIO_ETL   ..> SISTEMA_IVR   : ETL nocturno (read-only)
   SERVICIO_ETL   ..> Sched : programación
   SERVICIO_ALERTAS   ..> Buzon : notifica (CNST_001)
   @enduml

**Aplicación:** DOC-26 (Componentes + Distribución).
