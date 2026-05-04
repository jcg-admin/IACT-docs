8. Diagrama de componentes — arquitectura del sistema IACT
==========================================================

.. uml::

   @startuml

   package "Frontend (React + Webpack)" {
     component "UI Components\nDashboards, Reportes" as UiComponents
     component "Redux Store\nState Management"      as Redux
     component "HTTP Client\nAxios + JWT"           as HTTP
   }

   package "Backend (Django + DRF)" {
     component "REST API\nViewSets"                  as REST
     component "Auth Service\nJWT, Sessions"         as Auth
     component "RBAC Service\nFunciones, Grupos"     as RBAC
     component "Reports Service\nMétricas, Export"   as RPT
     component "Alerts Service\nUmbrales, Notif"     as ALR
     component "ETL Supervisor\nestado, reintento"   as PIP
     component "Audit Service\nInmutable"            as AUD
   }

   database "MySQL Analytics\nDatos IVR + RBAC + Audit" as MysqlAnalytics

   package "Infraestructura externa" {
     component "IVR Conmutador\n(read-only)" as IVR
     component "Scheduler\nAPScheduler"      as Sched
     component "Buzón Interno\n(no email)"   as Buzon
   }

   UiComponents    --> Redux : state
   UiComponents    --> HTTP  : fetch / post
   HTTP  --> REST  : REST + JWT

   REST  --> Auth : usa
   REST  --> RBAC : usa
   REST  --> RPT  : usa
   REST  --> ALR  : usa
   REST  --> PIP  : usa
   REST  --> AUD  : usa

   Auth --> MysqlAnalytics : queries
   RBAC --> MysqlAnalytics : queries
   RPT  --> MysqlAnalytics : queries
   ALR  --> MysqlAnalytics : queries
   PIP  --> MysqlAnalytics : queries
   AUD  --> MysqlAnalytics : append-only

   PIP   ..> IVR   : ETL nocturno (read-only)
   PIP   ..> Sched : programación
   ALR   ..> Buzon : notifica (CNST_001)
   @enduml

**Aplicación:** DOC-26 (Componentes + Distribución).

----
