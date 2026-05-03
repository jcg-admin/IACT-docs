.. meta::
 :artefacto: AT_UC_SUP_01
 :tipo: Diagrama Arquitectonico 4+1
 :dominio: arquitectura_tecnica
 :subdominio: uc
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_sup_01:

==========================================
UC_SUP_01 — Monitorear Llamada (Whisper)
==========================================

Modelo **4+1 de Kruchten** (variante 5+1 con Domain Model) aplicado a
:doc:`/requisitos/casos-uso/supervision/uc-sup-01/index`.
Cada seccion cubre una perspectiva arquitectonica del UC.

----

.. _uc_sup_01_domain:

1. Domain Model — Vista Logica
==============================

Entidades del dominio y sus relaciones para UC_SUP_01.

.. uml::
 :caption: UC_SUP_01 — Domain Model

 @startuml

 left to right direction

 class Call
 class AgentSession
 class SupervisionChannel

 Call --> AgentSession
 AgentSession --> SupervisionChannel

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`

----

.. _uc_sup_01_design:

2. Design View — Vista de Diseno
==================================

Secuencia del flujo principal de UC_SUP_01.

.. uml::
 :caption: UC_SUP_01 — Design View (secuencia)

 @startuml

 actor "monitor_live_calls" as monitor_live_calls
 participant "React Frontend" as Frontend <<frontend>>
 participant "Django API" as API <<api>>
 database "MariaDB (tbl_historico_*)" as BaseDatos <<sql>>

 monitor_live_calls -> Frontend : solicitar
 activate Frontend

 Frontend -> API : POST/GET endpoint
 activate API

 API -> BaseDatos : query / SP
 activate BaseDatos
 BaseDatos --> API : resultado
 deactivate BaseDatos

 API --> Frontend : respuesta JSON
 deactivate API

 Frontend --> monitor_live_calls : renderizar vista
 deactivate Frontend

 @enduml

----

.. _uc_sup_01_impl:

3. Implementation View — Vista de Implementacion
=================================================

Componentes de codigo que implementan UC_SUP_01.

.. uml::
 :caption: UC_SUP_01 — Implementation View

 @startuml

 package "MOD_Supervision" {
   component "View / Serializer" as ViewSerializer <<api>>
   component "Service / Repository" as ServiceRepo <<service>>
   component "ORM / SP" as ORMLayer <<orm>>
 }

 ViewSerializer --> ServiceRepo : invoca
 ServiceRepo --> ORMLayer : persiste / consulta

 @enduml

----

.. _uc_sup_01_usecase:

4. Use Case View — Vista de Casos de Uso
=========================================

Actores RBAC, relaciones y confines del MOD_Supervision.

.. uml::
 :caption: UC_SUP_01 — Use Case View

 @startuml

 left to right direction

 actor "monitor_live_calls"

 rectangle "MOD_Supervision" {
   usecase "UC_SUP_01\nMonitorear Llamada (Whisper)" as UCSUP01
 }

 monitor_live_calls --> UCSUP01

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`

----

.. _uc_sup_01_process:

5. Process View — Vista de Procesos
====================================

Flujo de actividades y concurrencia de UC_SUP_01.

.. uml::
 :caption: UC_SUP_01 — Process View (actividades)

 @startuml

 start
 :monitor_live_calls solicita Monitorear Llamada (Whisper);
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

.. _uc_sup_01_deploy:

6. Deployment View — Vista de Despliegue
=========================================

Distribucion fisica de componentes para UC_SUP_01.

.. uml::
 :caption: UC_SUP_01 — Deployment View

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
   - :doc:`/requisitos/casos-uso/supervision/uc-sup-01/index`
 * - **Indice arquitectonico UC**
   - :doc:`/arquitectura-tecnica/uc/index`
 * - **Modelo de dominio**
   - :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 * - **Catalogo RBAC**
   - :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 * - **Modulo**
   - :doc:`/arquitectura-tecnica/modulos/index`
