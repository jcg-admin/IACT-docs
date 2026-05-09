.. meta::
 :artefacto: UML_14_RELACIONES_DEPENDENCIA_IACT
 :tipo: Leccion UML — Aplicacion al dominio IACT
 :dominio: base_cognitiva
 :subdominio: _uml
 :estado: Aprobado
 :version: 1.1.0
 :fecha_creacion: 2026-05-08
 :ultimo_cambio: 2026-05-09
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uml-14-relaciones-dependencia-iact:

======================================================================
Relaciones de dependencia entre vistas — aplicacion al dominio IACT
======================================================================

.. note::

 Este documento aplica el framework Rozanski de viewpoints
 (UML_14) al modelo Kruchten 4+1 adaptado al dominio
 documental del sistema IACT. Establece el **DAG de
 dependencias entre paquetes de vistas** y el**orden
 optimo de lectura/comprension** de los diferentes
 conjuntos de diagramas del corpus arquitectonico.

 Complementa el contenido teorico de UML_14
 (:doc:`framework-rozanski`,
 :doc:`vistas-y-viewpoints`,
 :doc:`perspectivas-arquitectonicas`) con la materializacion
 concreta en el corpus IACT.

.. contents:: Contenido
 :depth: 2

----

1. Mapeo Vista IACT ↔ Viewpoint Rozanski
=========================================

El proyecto IACT mantiene siete vistas arquitectonicas que
son **subset enfocado** de los viewpoints estandar del
framework Rozanski (mas el modelo Kruchten 4+1 clasico).

.. list-table::
 :widths: 25 30 45
 :header-rows: 1

 * - Vista IACT
   - Equivalente Rozanski
   - Diagramas UML usados
 * - **DomainModel**
   - Information viewpoint
   - Clases (uml-03), objetos (uml-06), estados (uml-08)
 * - **UseCaseView**
   - Functional viewpoint
   - Casos de uso (uml-07)
 * - **DesignView**
   - Functional + Information
   - Clases (uml-03), secuencias (uml-09),
     actividades (uml-11), estados (uml-08)
 * - **ImplementationView**
   - Development viewpoint
   - Componentes (uml-04)
 * - **ProcessView**
   - Concurrency viewpoint
   - Actividades (uml-11), secuencias (uml-09)
 * - **DeployView**
   - Deployment viewpoint
   - Distribucion (uml-12)
 * - **ContextView**
   - Context viewpoint
   - Componentes (uml-04), casos de uso (uml-07)

----

2. DAG de dependencias entre vistas
====================================

Las relaciones de dependencia sirven como **guia para
entender el orden optimo de lectura y comprension** de los
diferentes paquetes de diagramas. La direccion de las
flechas significa "depende de" / "requiere haber leido
previamente".

.. uml::
 :caption: DAG de dependencias entre vistas IACT.

 @startuml

 left to right direction

 package "Modelo base" {
   [DomainModel]
 }

 package "Vista funcional" {
   [UseCaseView]
   [ContextView]
 }

 package "Vistas de diseno y construccion" {
   [DesignView]
   [ImplementationView]
 }

 package "Vistas de runtime" {
   [ProcessView]
   [DeployView]
 }

 [UseCaseView] --> [DomainModel] : usa vocabulario
 [ContextView] --> [UseCaseView] : enmarca alcance

 [DesignView] --> [UseCaseView] : satisface UCs
 [DesignView] --> [DomainModel] : referencia clases

 [ImplementationView] --> [DesignView] : sigue estructura
 [ImplementationView] --> [UseCaseView] : satisface UCs

 [ProcessView] --> [UseCaseView] : alinea con UCs
 [ProcessView] --> [DesignView] : usa estructura
 [ProcessView] --> [DeployView] : considera distribucion

 [DeployView] --> [UseCaseView] : satisface UCs
 [DeployView] --> [ImplementationView] : distribuye componentes

 @enduml

----

3. Detalle de las dependencias por categoria
=============================================

3.1 Dependencias del Modelo base
---------------------------------

**UseCaseView → DomainModel:**

Los casos de uso requieren el vocabulario establecido en el
modelo de dominio para garantizar una especificacion clara
y consistente de los requisitos. Antes de leer los UCs, el
lector debe estar familiarizado con las entidades, atributos
y relaciones canonicas del DomainModel.

3.2 Dependencias de Diseño
---------------------------

**DesignView → UseCaseView:**

El diseño necesita comprender completamente los casos de uso
para crear una estructura de clases, secuencias y maquinas
de estado que satisfaga los requisitos del sistema. Cada
clase, metodo o transicion en DesignView se justifica por
algun UC.

**DesignView → DomainModel:**

El diseño NO duplica las definiciones del DomainModel — los
class diagrams referencian las clases canonicas via
``:doc:``. El DomainModel es la fuente de verdad del
vocabulario; DesignView lo usa.

3.3 Dependencias de Procesos
-----------------------------

**ProcessView → UseCaseView:**

Los procesos deben alinearse con los comportamientos
especificados en los casos de uso. Un flujo concurrente que
no satisface ningun UC carece de proposito.

**ProcessView → DesignView:**

La gestion de procesos requiere entender la estructura de
clases para la sincronizacion (locks, transactions,
queues). Sin DesignView no se puede razonar sobre
concurrencia sobre que entidades.

**ProcessView → DeployView:**

Los procesos necesitan considerar la distribucion del
sistema para una paralelizacion efectiva. Decisiones como
"este flujo se ejecuta en background workers" requieren
saber donde corren esos workers en la topologia.

3.4 Dependencias de Implementacion
-----------------------------------

**ImplementationView → UseCaseView:**

La implementacion debe basarse en los requisitos definidos
en los casos de uso. Cada componente justifica su
existencia por algun UC que cubre.

**ImplementationView → DesignView:**

Los componentes de software deben seguir la estructura de
clases establecida en el diseño. La capa ``<<service>>`` de
un componente expone los servicios diseñados; la capa
``<<repository>>`` persiste las entidades del DomainModel
materializadas en DesignView.

3.5 Dependencias de Despliegue
-------------------------------

**DeployView → UseCaseView:**

El despliegue debe satisfacer los requisitos del sistema —
en particular los requisitos no funcionales (latencia,
disponibilidad, escalabilidad). Sin UCs y sus
``requisitos-no-funcionales.rst``, las decisiones de
distribucion son arbitrarias.

**DeployView → ImplementationView:**

La distribucion del sistema debe considerar como se
organizan los componentes implementados. No se puede
desplegar lo que aun no se ha implementado.

----

4. Orden optimo de lectura del corpus IACT
============================================

Derivado del DAG, el orden recomendado para un lector que
abre el corpus por primera vez es:

#. **DomainModel** — vocabulario base. Sin esto, todo lo
   demas es opaco.

#. **UseCaseView** — que hace el sistema (functional
   intent). Usa el DomainModel.

#. **ContextView** — donde encaja el sistema en su entorno
   externo (system + adyacentes). Enmarca el alcance.

#. **DesignView** — como esta organizado internamente
   (estructura logica). Conecta UCs con clases.

#. **ImplementationView** — como se construye (componentes
   reales: API, service, repository, ORM, database).

#. **ProcessView** — como se ejecuta (concurrencia,
   asincronia, locks).

#. **DeployView** — donde corre (topologia de runtime).

Las primeras tres vistas son de **comprension del problema**
(que y para quien). Las siguientes son de **especificacion
de la solucion** (como). Las ultimas dos son de
**operacion** (cuando y donde).

----

5. Aplicacion al corpus actual
===============================

5.1 Estado de cada vista
-------------------------

.. list-table::
 :widths: 30 70
 :header-rows: 1

 * - Vista
   - Estado en el corpus
 * - DomainModel
   - 109+ clases en
     ``source/arquitectura-tecnica/domain-model/``
 * - UseCaseView
   - 88 UCs en estructura modular
     (``casos-uso/<cluster>/uc-X/``) + 13 cluster index
     en ``arquitectura-tecnica/use-case-view/``
 * - DesignView
   - 10 modulos en estructura modular
     (``arquitectura-tecnica/design-view/<modulo>/``)
 * - ImplementationView
   - 10 modulos en estructura modular
     (``arquitectura-tecnica/implementation-view/<modulo>/``)
 * - ProcessView
   - Pendiente migracion a estructura modular
 * - DeployView
   - Pendiente migracion a estructura modular
 * - ContextView
   - Estructura plana correcta (granularidad apropiada)

5.2 Modulos out-of-scope para vistas internas
-----------------------------------------------

Los modulos ``operator``, ``supervision`` y ``caller``
estan documentados en UseCaseView como vista de
**requisitos** pero**NO entran** en DesignView,
ImplementationView, ProcessView ni DeployView. Razones:

- ``caller``: representa al actor externo (sistema IVR del
  cliente). IACT no lo diseña ni implementa internamente.
- ``operator``, ``supervision``: deferidos a WPs futuros
  segun decision documentada en
  ``design-view/index.rst`` v4.0.0.

----

6. Implicaciones para la documentacion del corpus
==================================================

6.1 No duplicacion entre vistas
--------------------------------

Cada vista referencia (no duplica) las definiciones de
vistas previas en el DAG. Reglas operativas:

- DesignView class diagrams **no redefinen** atributos ya
  declarados en DomainModel; los referencian via ``:doc:``.
- ImplementationView **no redefine** clases; muestra los
  componentes (API, service, repository, ORM) que las
  implementan.
- ProcessView **no redibuja** secuencias canonicas de
  DesignView; muestra el aspecto concurrente/asincrono
  cuando difiere de la secuencia canonica.

6.2 Lectura cruzada
--------------------

Cuando un UC referencia un componente de implementacion,
la cadena de lectura es:

::

   UC textual (casos-uso/.../uc-X/index.rst)
     → UseCaseView del modulo (.../use-case-view/<modulo>/index)
     → DesignView del modulo (.../design-view/<modulo>/<vista-de-contenido>)
     → ImplementationView del modulo (.../implementation-view/<modulo>/<vista-de-contenido>)

----

7. Referencias
===============

- :doc:`framework-rozanski` — fundamentos del framework
  Rozanski.
- :doc:`vistas-y-viewpoints` — diferencia entre vistas y
  viewpoints.
- :doc:`perspectivas-arquitectonicas` — perspectivas
  ortogonales (cross-cutting concerns).
- :doc:`concerns-principles-decisions` — relacion con
  drivers arquitectonicos.
- :doc:`/arquitectura-tecnica/use-case-view/index` —
  UseCaseView del corpus IACT.
- :doc:`/arquitectura-tecnica/design-view/index` —
  DesignView del corpus IACT.
- :doc:`/arquitectura-tecnica/domain-model/index` —
  DomainModel canonico.

----

8. Diagrama de cajas — vistas y tipos de diagrama
==================================================

Esta seccion muestra cada vista como una caja que contiene
los tipos de diagrama UML que la componen, con las relaciones
de dependencia entre vistas. Complementa el diagrama de
componentes de las secciones anteriores con el patron de
cajas usado en ``use-case-view``.

.. uml::
 :caption: Vistas IACT — cajas con tipos de diagrama y dependencias.

 @startuml
 left to right direction

 rectangle "DomainModel" as PDM {
   rectangle "Diagrama de clases" as DM_CLS
   rectangle "Diagrama de objetos" as DM_OBJ
   rectangle "Diagrama de estados" as DM_EST
 }

 rectangle "UseCaseView" as PUC {
   rectangle "Diagrama de casos de uso" as UC_UCX
 }

 rectangle "DesignView" as PDV {
   rectangle "Diagrama de clases\n(bounded-context)" as DV_CLS
   rectangle "Diagrama de secuencias\n(interaction-pattern)" as DV_SEQ
   rectangle "Diagrama de actividades\n(*-flow)" as DV_ACT
   rectangle "Diagrama de estados\n(*-lifecycle)" as DV_EST
 }

 rectangle "ImplementationView" as PIV {
   rectangle "Diagrama de componentes\n(layer-structure)" as IV_CMP
   rectangle "Diagrama de secuencias\n(interaction-pattern)" as IV_SEQ
 }

 rectangle "ProcessView" as PPV {
   rectangle "Diagrama de actividades\n(concurrencia)" as PV_ACT
   rectangle "Diagrama de secuencias\n(sincronizacion)" as PV_SEQ
 }

 rectangle "DeployView" as PDEV {
   rectangle "Diagrama de despliegue\n(topologia)" as DEPV_DEP
 }

 rectangle "ContextView" as PCV {
   rectangle "Diagrama de componentes\n(context-diagram)" as CV_CMP
 }

 PUC    ..> PDM  : usa vocabulario
 PDV    ..> PUC  : satisface UCs
 PDV    ..> PDM  : referencia clases
 PIV    ..> PDV  : sigue estructura
 PIV    ..> PUC  : satisface UCs
 PPV    ..> PUC  : alinea con UCs
 PPV    ..> PDV  : usa estructura
 PPV    ..> PDEV : considera distribucion
 PDEV   ..> PUC  : satisface UCs
 PDEV   ..> PIV  : distribuye componentes
 PCV    ..> PUC  : enmarca alcance

 @enduml

Los tipos de diagrama dentro de cada caja son los archivos
reales del corpus, nombrados por contenido segun CLEAN_CODE
§6.2:

.. list-table::
 :widths: 25 75
 :header-rows: 1

 * - Tipo de diagrama
   - Archivos representativos
 * - bounded-context (DesignView)
   - ``design-view/{modulo}/bounded-context.rst``
 * - interaction-pattern (DesignView, ImplementationView)
   - ``{view}/{modulo}/interaction-pattern.rst``
 * - ``*-lifecycle`` (DesignView)
   - ``user-lifecycle.rst``,
     ``menu-item-lifecycle.rst``,
     ``audit-event-lifecycle.rst``,
     ``alert-event-lifecycle.rst``,
     ``session-lifecycle.rst``,
     ``pipeline-execution-lifecycle.rst``,
     ``export-job-lifecycle.rst``,
     ``assignment-lifecycle.rst``
 * - ``*-flow`` (DesignView)
   - ``log-retention-flow.rst``,
     ``alert-evaluation-flow.rst``,
     ``etl-execution-flow.rst``,
     ``async-export-flow.rst``,
     ``separation-check-flow.rst``,
     ``effective-set-evaluation-flow.rst``,
     ``jwt-authentication-flow.rst``
 * - layer-structure (ImplementationView)
   - ``implementation-view/{modulo}/layer-structure.rst``
 * - concurrencia (ProcessView)
   - ``alert-evaluation-concurrency.rst``,
     ``etl-pipeline-concurrency.rst``,
     ``jwt-session-synchronization.rst``,
     ``realtime-dashboard-concurrency.rst``
 * - topologia (DeployView)
   - ``standard-topology.rst``,
     ``auth-cache-topology.rst``,
     ``etl-pipeline-topology.rst``

----

9. Historial
=============

.. list-table::
 :widths: 15 15 70
 :header-rows: 1

 * - Version
   - Fecha
   - Cambios
 * - 1.0.0
   - 2026-05-08
   - Documento inicial — formaliza el DAG de dependencias
     entre vistas arquitectonicas IACT y el orden optimo
     de lectura del corpus. Adapta el framework Rozanski
     al subset de vistas materializadas en el proyecto.
 * - 1.1.0
   - 2026-05-09
   - Agregada seccion 8 con diagrama de cajas (rectangles)
     mostrando cada vista con sus tipos de diagrama UML
     y las dependencias entre vistas, alineado al patron
     usado en ``use-case-view``. Tabla de tipos de diagrama
     y archivos representativos del corpus.
