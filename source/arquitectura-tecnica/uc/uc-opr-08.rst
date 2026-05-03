.. meta::
 :artefacto: AT_UC_OPR_08
 :tipo: Diagrama Arquitectonico 4+1
 :dominio: arquitectura_tecnica
 :subdominio: uc
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_opr_08:

==================================
UC_OPR_08 — Ver Propio Dashboard
==================================

Modelo **4+1 de Kruchten** (variante 5+1 con Domain Model) aplicado a
:doc:`/requisitos/casos-uso/operator/uc-opr-08/index`.
Cada seccion cubre una perspectiva arquitectonica del UC.

----

.. _uc_opr_08_domain:

1. Domain Model — Vista Logica
==============================

Entidades del dominio y sus relaciones para UC_OPR_08.

.. uml::
 :caption: UC_OPR_08 — Domain Model

 @startuml

 left to right direction

 class AgentDashboard
 class AgentSession
 class Call

 AgentDashboard --> AgentSession
 AgentSession --> Call

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`

----

.. _uc_opr_08_design:

2. Design View — Vista de Diseno
==================================

Secuencia del flujo principal de UC_OPR_08.

.. uml::
 :caption: UC_OPR_08 — Design View (secuencia)

 @startuml

 actor "view_own_performance_dashboard" as view_own_performance_dashboard
 participant "React Frontend" as Frontend <<frontend>>
 participant "Django API" as API <<api>>
 database "MariaDB (tbl_historico_*)" as BaseDatos <<sql>>

 view_own_performance_dashboard -> Frontend : solicitar
 activate Frontend

 Frontend -> API : POST/GET endpoint
 activate API

 API -> BaseDatos : query / SP
 activate BaseDatos
 BaseDatos --> API : resultado
 deactivate BaseDatos

 API --> Frontend : respuesta JSON
 deactivate API

 Frontend --> view_own_performance_dashboard : renderizar vista
 deactivate Frontend

 @enduml

----

.. _uc_opr_08_impl:

3. Implementation View — Vista de Implementacion
=================================================

Componentes de codigo que implementan UC_OPR_08.

.. uml::
 :caption: UC_OPR_08 — Implementation View

 @startuml

 package "MOD_Operator" {
   component "View / Serializer" as ViewSerializer <<api>>
   component "Service / Repository" as ServiceRepo <<service>>
   component "ORM / SP" as ORMLayer <<orm>>
 }

 ViewSerializer --> ServiceRepo : invoca
 ServiceRepo --> ORMLayer : persiste / consulta

 @enduml

----

.. _uc_opr_08_usecase:

4. Use Case View — Vista de Casos de Uso
=========================================

Actores RBAC, relaciones y confines del MOD_Operator.

.. uml::
 :caption: UC_OPR_08 — Use Case View

 @startuml

 left to right direction

 actor "view_own_performance_dashboard"

 rectangle "MOD_Operator" {
   usecase "UC_OPR_08\nVer Propio Dashboard" as UCOPR08
 }

 view_own_performance_dashboard --> UCOPR08

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`

----

.. _uc_opr_08_process:

5. Process View — Vista de Procesos
====================================

Flujo de actividades y concurrencia de UC_OPR_08.

.. uml::
 :caption: UC_OPR_08 — Process View (actividades)

 @startuml

 start
 :view_own_performance_dashboard solicita Ver Propio Dashboard;
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

.. _uc_opr_08_deploy:

6. Deployment View — Vista de Despliegue
=========================================

Distribucion fisica de componentes para UC_OPR_08.

.. uml::
 :caption: UC_OPR_08 — Deployment View

 @startuml

 node "Softphone / WebRTC" as NodoFront
 node "Django API" as NodoAPI
 database "MariaDB (tbl_historico_*)" as NodoBD

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
   - :doc:`/requisitos/casos-uso/operator/uc-opr-08/index`
 * - **Indice arquitectonico UC**
   - :doc:`/arquitectura-tecnica/uc/index`
 * - **Modelo de dominio**
   - :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 * - **Catalogo RBAC**
   - :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 * - **Modulo**
   - :doc:`/arquitectura-tecnica/modulos/index`
