.. meta::
 :artefacto: AT_UC_ACC_05
 :tipo: Diagrama Arquitectonico 4+1
 :dominio: arquitectura_tecnica
 :subdominio: uc
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_acc_05:

==================================
UC_ACC_05 — Gestionar Reglas SoD
==================================

Modelo **4+1 de Kruchten** (variante 5+1 con Domain Model) aplicado a
:doc:`/requisitos/casos-uso/access/uc-acc-05/index`.
Cada seccion cubre una perspectiva arquitectonica del UC.

----

.. _uc_acc_05_domain:

1. Domain Model — Vista Logica
==============================

Entidades del dominio y sus relaciones para UC_ACC_05.

.. uml::
 :caption: UC_ACC_05 — Domain Model

 @startuml

 left to right direction

 class SodRule
 class Function
 class AuditEvent

 SodRule --> Function
 Function --> AuditEvent

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`

----

.. _uc_acc_05_design:

2. Design View — Vista de Diseno
==================================

Secuencia del flujo principal de UC_ACC_05.

.. uml::
 :caption: UC_ACC_05 — Design View (secuencia)

 @startuml

 actor "view_separation_rules" as view_separation_rules
 participant "React Frontend" as Frontend <<frontend>>
 participant "Django API" as API <<api>>
 database "MariaDB" as BaseDatos <<sql>>

 view_separation_rules -> Frontend : solicitar
 activate Frontend

 Frontend -> API : POST/GET endpoint
 activate API

 API -> BaseDatos : query / SP
 activate BaseDatos
 BaseDatos --> API : resultado
 deactivate BaseDatos

 API --> Frontend : respuesta JSON
 deactivate API

 Frontend --> view_separation_rules : renderizar vista
 deactivate Frontend

 @enduml

----

.. _uc_acc_05_impl:

3. Implementation View — Vista de Implementacion
=================================================

Componentes de codigo que implementan UC_ACC_05.

.. uml::
 :caption: UC_ACC_05 — Implementation View

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

.. _uc_acc_05_usecase:

4. Use Case View — Vista de Casos de Uso
=========================================

Actores RBAC, relaciones y confines del MOD_Access.

.. uml::
 :caption: UC_ACC_05 — Use Case View

 @startuml

 left to right direction

 actor "view_separation_rules"

 rectangle "MOD_Access" {
   usecase "UC_ACC_05\nGestionar Reglas SoD" as UCACC05
 }

 view_separation_rules --> UCACC05

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`

----

.. _uc_acc_05_process:

5. Process View — Vista de Procesos
====================================

Flujo de actividades y concurrencia de UC_ACC_05.

.. uml::
 :caption: UC_ACC_05 — Process View (actividades)

 @startuml

 start
 :view_separation_rules solicita Gestionar Reglas SoD;
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

.. _uc_acc_05_deploy:

6. Deployment View — Vista de Despliegue
=========================================

Distribucion fisica de componentes para UC_ACC_05.

.. uml::
 :caption: UC_ACC_05 — Deployment View

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
   - :doc:`/requisitos/casos-uso/access/uc-acc-05/index`
 * - **Indice arquitectonico UC**
   - :doc:`/arquitectura-tecnica/uc/index`
 * - **Modelo de dominio**
   - :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 * - **Catalogo RBAC**
   - :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 * - **Modulo**
   - :doc:`/arquitectura-tecnica/modulos/index`
