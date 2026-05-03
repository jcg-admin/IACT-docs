.. meta::
 :artefacto: AT_UC_LOG_07
 :tipo: Diagrama Arquitectonico 4+1
 :dominio: arquitectura_tecnica
 :subdominio: uc
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_log_07:

===================================
UC_LOG_07 — Ver Metricas Tecnicas
===================================

Modelo **4+1 de Kruchten** (variante 5+1 con Domain Model) aplicado a
:doc:`/requisitos/casos-uso/logs/uc-log-07/index`.
Cada seccion cubre una perspectiva arquitectonica del UC.

----

.. _uc_log_07_domain:

1. Domain Model — Vista Logica
==============================

Entidades del dominio y sus relaciones para UC_LOG_07.

.. uml::
 :caption: UC_LOG_07 — Domain Model

 @startuml

 left to right direction

 class MetricaTecnica
 class LogEntry
 class MetricaTecnica

 MetricaTecnica --> LogEntry
 LogEntry --> MetricaTecnica

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`

----

.. _uc_log_07_design:

2. Design View — Vista de Diseno
==================================

Secuencia del flujo principal de UC_LOG_07.

.. uml::
 :caption: UC_LOG_07 — Design View (secuencia)

 @startuml

 actor "view_technical_metrics" as view_technical_metrics
 participant "React Frontend" as Frontend <<frontend>>
 participant "Django API" as API <<api>>
 database "MariaDB / Sistema" as BaseDatos <<sql>>

 view_technical_metrics -> Frontend : solicitar
 activate Frontend

 Frontend -> API : POST/GET endpoint
 activate API

 API -> BaseDatos : query / SP
 activate BaseDatos
 BaseDatos --> API : resultado
 deactivate BaseDatos

 API --> Frontend : respuesta JSON
 deactivate API

 Frontend --> view_technical_metrics : renderizar vista
 deactivate Frontend

 @enduml

----

.. _uc_log_07_impl:

3. Implementation View — Vista de Implementacion
=================================================

Componentes de codigo que implementan UC_LOG_07.

.. uml::
 :caption: UC_LOG_07 — Implementation View

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

.. _uc_log_07_usecase:

4. Use Case View — Vista de Casos de Uso
=========================================

Actores RBAC, relaciones y confines del MOD_Logs.

.. uml::
 :caption: UC_LOG_07 — Use Case View

 @startuml

 left to right direction

 actor "view_technical_metrics"

 rectangle "MOD_Logs" {
   usecase "UC_LOG_07\nVer Metricas Tecnicas" as UCLOG07
 }

 view_technical_metrics --> UCLOG07

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`

----

.. _uc_log_07_process:

5. Process View — Vista de Procesos
====================================

Flujo de actividades y concurrencia de UC_LOG_07.

.. uml::
 :caption: UC_LOG_07 — Process View (actividades)

 @startuml

 start
 :view_technical_metrics solicita Ver Metricas Tecnicas;
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

.. _uc_log_07_deploy:

6. Deployment View — Vista de Despliegue
=========================================

Distribucion fisica de componentes para UC_LOG_07.

.. uml::
 :caption: UC_LOG_07 — Deployment View

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
   - :doc:`/requisitos/casos-uso/logs/uc-log-07/index`
 * - **Indice arquitectonico UC**
   - :doc:`/arquitectura-tecnica/uc/index`
 * - **Modelo de dominio**
   - :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 * - **Catalogo RBAC**
   - :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 * - **Modulo**
   - :doc:`/arquitectura-tecnica/modulos/index`
