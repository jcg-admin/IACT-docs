.. meta::
 :artefacto: AT_UC_LOG_01
 :tipo: Diagrama Arquitectonico 4+1
 :dominio: arquitectura_tecnica
 :subdominio: uc
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_log_01:

========================================
UC_LOG_01 — Consultar Logs del Sistema
========================================

Modelo **4+1 de Kruchten** (variante 5+1 con Domain Model) aplicado a
:doc:`/requisitos/casos-uso/logs/uc-log-01/index`.
Cada seccion cubre una perspectiva arquitectonica del UC.

----

.. _uc_log_01_domain:

1. Domain Model — Vista Logica
==============================

Entidades del dominio y sus relaciones para UC_LOG_01.

.. uml::
 :caption: UC_LOG_01 — Domain Model

 @startuml

 left to right direction

 class LogEntry
 class LogFilter
 class LogEntry

 LogEntry --> LogFilter
 LogFilter --> LogEntry

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`

----

.. _uc_log_01_design:

2. Design View — Vista de Diseno
==================================

Secuencia del flujo principal de UC_LOG_01.

.. uml::
 :caption: UC_LOG_01 — Design View (secuencia)

 @startuml

 actor "view_application_logs" as view_application_logs
 participant "React Frontend" as Frontend <<frontend>>
 participant "Django API" as API <<api>>
 database "MariaDB / Sistema" as BaseDatos <<sql>>

 view_application_logs -> Frontend : solicitar
 activate Frontend

 Frontend -> API : POST/GET endpoint
 activate API

 API -> BaseDatos : query / SP
 activate BaseDatos
 BaseDatos --> API : resultado
 deactivate BaseDatos

 API --> Frontend : respuesta JSON
 deactivate API

 Frontend --> view_application_logs : renderizar vista
 deactivate Frontend

 @enduml

----

.. _uc_log_01_impl:

3. Implementation View — Vista de Implementacion
=================================================

Componentes de codigo que implementan UC_LOG_01.

.. uml::
 :caption: UC_LOG_01 — Implementation View

 @startuml

 package "MOD_Logs" {
   component "View / Serializer" as ViewSerializer <<api>>
   component "Service / Repository" as ServiceRepo <<service>>
   component "ORM / SP" as ORMLayer <<orm>>
 }

 ViewSerializer --> ServiceRepo : invoca
 ServiceRepo --> ORMLayer : persiste / consulta

 @enduml

----

.. _uc_log_01_usecase:

4. Use Case View — Vista de Casos de Uso
=========================================

Actores RBAC, relaciones y confines del MOD_Logs.

.. uml::
 :caption: UC_LOG_01 — Use Case View

 @startuml

 left to right direction

 actor "view_application_logs"

 rectangle "MOD_Logs" {
   usecase "UC_LOG_01\nConsultar Logs del Sistema" as UCLOG01
 }

 view_application_logs --> UCLOG01

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`

----

.. _uc_log_01_process:

5. Process View — Vista de Procesos
====================================

Flujo de actividades y concurrencia de UC_LOG_01.

.. uml::
 :caption: UC_LOG_01 — Process View (actividades)

 @startuml

 start
 :view_application_logs solicita Consultar Logs del Sistema;
 :Validar autenticacion y permisos RBAC;
 if (permisos validos?) then (si)
   :Ejecutar logica principal;
   :Persistir resultado;
   :Registrar AuditEvent;
   :Retornar respuesta exitosa;
 else (no)
   :Retornar error 403;
 endif
 stop

 @enduml

----

.. _uc_log_01_deploy:

6. Deployment View — Vista de Despliegue
=========================================

Distribucion fisica de componentes para UC_LOG_01.

.. uml::
 :caption: UC_LOG_01 — Deployment View

 @startuml

 node "React Frontend" as NodoFront
 node "Django API" as NodoAPI
 database "MariaDB / Sistema" as NodoBD

 NodoFront --> NodoAPI : HTTPS / REST
 NodoAPI --> NodoBD : TCP / SQL

 @enduml

----

Referencias
===========

.. list-table::
 :widths: 30 70
 :header-rows: 0

 * - **Especificacion UC**
   - :doc:`/requisitos/casos-uso/logs/uc-log-01/index`
 * - **Indice arquitectonico UC**
   - :doc:`/arquitectura-tecnica/uc/index`
 * - **Modelo de dominio**
   - :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 * - **Catalogo RBAC**
   - :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 * - **Modulo**
   - :doc:`/arquitectura-tecnica/modulos/index`
