.. meta::
 :artefacto: AT_UC_USR_01
 :tipo: Diagrama Arquitectonico 4+1
 :dominio: arquitectura_tecnica
 :subdominio: uc
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_usr_01:

===========================
UC_USR_01 — Crear Usuario
===========================

Modelo **4+1 de Kruchten** (variante 5+1 con Domain Model) aplicado a
:doc:`/requisitos/casos-uso/users/uc-usr-01/index`.
Cada seccion cubre una perspectiva arquitectonica del UC.

----

.. _uc_usr_01_domain:

1. Domain Model — Vista Logica
==============================

Entidades del dominio y sus relaciones para UC_USR_01.

.. uml::
 :caption: UC_USR_01 — Domain Model

 @startuml

 left to right direction

 class User
 class AccessGroup
 class AuditEvent

 User --> AccessGroup
 AccessGroup --> AuditEvent

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`

----

.. _uc_usr_01_design:

2. Design View — Vista de Diseno
==================================

Secuencia del flujo principal de UC_USR_01.

.. uml::
 :caption: UC_USR_01 — Design View (secuencia)

 @startuml

 actor "create_users" as create_users
 participant "React Frontend" as Frontend <<frontend>>
 participant "Django API" as API <<api>>
 database "MariaDB" as BaseDatos <<sql>>

 create_users -> Frontend : solicitar
 activate Frontend

 Frontend -> API : POST/GET endpoint
 activate API

 API -> BaseDatos : query / SP
 activate BaseDatos
 BaseDatos --> API : resultado
 deactivate BaseDatos

 API --> Frontend : respuesta JSON
 deactivate API

 Frontend --> create_users : renderizar vista
 deactivate Frontend

 @enduml

----

.. _uc_usr_01_impl:

3. Implementation View — Vista de Implementacion
=================================================

Componentes de codigo que implementan UC_USR_01.

.. uml::
 :caption: UC_USR_01 — Implementation View

 @startuml

 package "MOD_Users" {
   component "View / Serializer" as ViewSerializer <<api>>
   component "Service / Repository" as ServiceRepo <<service>>
   component "ORM / SP" as ORMLayer <<orm>>
 }

 ViewSerializer --> ServiceRepo : invoca
 ServiceRepo --> ORMLayer : persiste / consulta

 @enduml

----

.. _uc_usr_01_usecase:

4. Use Case View — Vista de Casos de Uso
=========================================

Actores RBAC, relaciones y confines del MOD_Users.

.. uml::
 :caption: UC_USR_01 — Use Case View

 @startuml

 left to right direction

 actor "create_users"

 rectangle "MOD_Users" {
   usecase "UC_USR_01\nCrear Usuario" as UCUSR01
 }

 create_users --> UCUSR01

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`

----

.. _uc_usr_01_process:

5. Process View — Vista de Procesos
====================================

Flujo de actividades y concurrencia de UC_USR_01.

.. uml::
 :caption: UC_USR_01 — Process View (actividades)

 @startuml

 start
 :create_users solicita Crear Usuario;
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

.. _uc_usr_01_deploy:

6. Deployment View — Vista de Despliegue
=========================================

Distribucion fisica de componentes para UC_USR_01.

.. uml::
 :caption: UC_USR_01 — Deployment View

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
   - :doc:`/requisitos/casos-uso/users/uc-usr-01/index`
 * - **Indice arquitectonico UC**
   - :doc:`/arquitectura-tecnica/uc/index`
 * - **Modelo de dominio**
   - :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 * - **Catalogo RBAC**
   - :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 * - **Modulo**
   - :doc:`/arquitectura-tecnica/modulos/index`
