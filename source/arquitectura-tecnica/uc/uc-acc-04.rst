.. meta::
 :artefacto: AT_UC_ACC_04
 :tipo: Diagrama Arquitectonico 4+1
 :dominio: arquitectura_tecnica
 :subdominio: uc
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_acc_04:

===============================
UC_ACC_04 — Asignar Agrupador
===============================

Modelo **4+1 de Kruchten** (variante 5+1 con Domain Model) aplicado a
:doc:`/requisitos/casos-uso/access/uc-acc-04/index`.
Cada seccion cubre una perspectiva arquitectonica del UC.

----

.. _uc_acc_04_domain:

1. Domain Model — Vista Logica
==============================

Entidades del dominio y sus relaciones para UC_ACC_04.

.. uml::
 :caption: UC_ACC_04 — Domain Model

 @startuml

 left to right direction

 class AccessGroup
 class User
 class AuditEvent

 AccessGroup --> User
 User --> AuditEvent

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`

----

.. _uc_acc_04_design:

2. Design View — Vista de Diseno
==================================

Secuencia del flujo principal de UC_ACC_04.

.. uml::
 :caption: UC_ACC_04 — Design View (secuencia)

 @startuml

 actor "assign_function_groups" as assign_function_groups
 participant "React Frontend" as Frontend <<frontend>>
 participant "Django API" as API <<api>>
 database "MariaDB" as BaseDatos <<sql>>

 assign_function_groups -> Frontend : solicitar
 activate Frontend

 Frontend -> API : POST/GET endpoint
 activate API

 API -> BaseDatos : query / SP
 activate BaseDatos
 BaseDatos --> API : resultado
 deactivate BaseDatos

 API --> Frontend : respuesta JSON
 deactivate API

 Frontend --> assign_function_groups : renderizar vista
 deactivate Frontend

 @enduml

----

.. _uc_acc_04_impl:

3. Implementation View — Vista de Implementacion
=================================================

Componentes de codigo que implementan UC_ACC_04.

.. uml::
 :caption: UC_ACC_04 — Implementation View

 @startuml

 package "MOD_Access" {
   component "View / Serializer" as ViewSerializer <<api>>
   component "Service / Repository" as ServiceRepo <<service>>
   component "ORM / SP" as ORMLayer <<orm>>
 }

 ViewSerializer --> ServiceRepo : invoca
 ServiceRepo --> ORMLayer : persiste / consulta

 @enduml

----

.. _uc_acc_04_usecase:

4. Use Case View — Vista de Casos de Uso
=========================================

Actores RBAC, relaciones y confines del MOD_Access.

.. uml::
 :caption: UC_ACC_04 — Use Case View

 @startuml

 left to right direction

 actor "assign_function_groups"

 rectangle "MOD_Access" {
   usecase "UC_ACC_04\nAsignar Agrupador" as UCACC04
 }

 assign_function_groups --> UCACC04

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`

----

.. _uc_acc_04_process:

5. Process View — Vista de Procesos
====================================

Flujo de actividades y concurrencia de UC_ACC_04.

.. uml::
 :caption: UC_ACC_04 — Process View (actividades)

 @startuml

 start
 :assign_function_groups solicita Asignar Agrupador;
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

.. _uc_acc_04_deploy:

6. Deployment View — Vista de Despliegue
=========================================

Distribucion fisica de componentes para UC_ACC_04.

.. uml::
 :caption: UC_ACC_04 — Deployment View

 @startuml

 node "React Frontend" as NodoFront
 node "Django API" as NodoAPI
 database "MariaDB" as NodoBD

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
   - :doc:`/requisitos/casos-uso/access/uc-acc-04/index`
 * - **Indice arquitectonico UC**
   - :doc:`/arquitectura-tecnica/uc/index`
 * - **Modelo de dominio**
   - :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 * - **Catalogo RBAC**
   - :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 * - **Modulo**
   - :doc:`/arquitectura-tecnica/modulos/index`
