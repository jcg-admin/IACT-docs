.. meta::
 :artefacto: UML_14_ROZANSKI
 :tipo: Referencia — Framework de Viewpoints
 :dominio: base_cognitiva
 :subdominio: _uml
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uml-14-rozanski:

=======================================================
Framework Rozanski et al. — Viewpoints, Model Types y UML
=======================================================

La tabla siguiente describe las relaciones entre los viewpoints
de Rozanski et al., los tipos de modelo (*model types*) que cada
viewpoint utiliza, los diagramas UML empleados como notación de
modelado para instanciar esos model types, y las herramientas
UML CASE como editores de modelo.

Los diagramas UML y herramientas listados fueron determinados
mediante el feedback de un estudio piloto conducido entre
practitioners antes de publicar la encuesta principal.

.. note::

 Las herramientas listadas en la columna **UML Tools** aplican
 a todos los viewpoints: ArgoUML, BoUML, Enterprise Architect,
 MagicDraw, MS Visual Studio, Obeo UML Designer, Modelio,
 Papyrus, Rational Rhapsody, StarUML, Umbrello UML, Visual
 Paradigm.

.. list-table:: Tabla 1 — Viewpoints Rozanski et al. × Model Types × Diagramas UML
 :header-rows: 1
 :widths: 16 26 58

 * - Viewpoint
   - Model Type
   - Diagramas UML
 * - **Functional**
   - Functional structure
   - Class, Component, Composite Structure, Deployment,
     Object, Package, Profile
 * - **Information**
   - Data flow
   - Activity, Class, Component, Composite Structure,
     Object, Package, Profile
 * - **Information**
   - Data structure
   - Class, Component, Composite Structure, Deployment,
     Object, Package, Profile
 * - **Information**
   - Data life-cycle
   - Activity, Profile, Sequence/Communication,
     State, Timing
 * - **Concurrency**
   - Concurrency structure
   - Class, Component, Composite Structure, Deployment,
     Object, Package, Profile
 * - **Concurrency**
   - Mapping between functional and concurrent components
   - Component, Composite Structure, Deployment,
     Package, Profile
 * - **Development**
   - Software modules structure
   - Class, Component, Composite Structure, Deployment,
     Object, Package, Profile
 * - **Development**
   - Software code structure
   - Class, Component, Composite Structure, Deployment,
     Object, Package, Profile
 * - **Development**
   - Software build process
   - Activity, Class, Component, Composite Structure,
     Deployment, Object, Package, Profile,
     Sequence/Communication, State
 * - **Development**
   - Software release process
   - Activity, Class, Component, Composite Structure,
     Deployment, Object, Package, Profile,
     Sequence/Communication, State
 * - **Deployment**
   - Physical structure
   - Class, Component, Composite Structure, Deployment,
     Object, Package, Profile
 * - **Deployment**
   - Mapping between functional and physical components
   - Composite Structure, Deployment, Package, Profile
 * - **Operational**
   - System installation
   - Activity, Class, Composite Structure, Component,
     Deployment, Object, Package, Profile
 * - **Operational**
   - System administration
   - Activity, Class, Component, Composite Structure,
     Deployment, Object, Package, Profile,
     Sequence/Communication, State, Timing, Use-case
 * - **Operational**
   - System configuration
   - Activity, Class, Component, Composite Structure,
     Deployment, Object, Package, Profile,
     Sequence/Communication, State, Use case
 * - **Operational**
   - System support
   - Activity, Class, Component, Composite Structure,
     Deployment, Object, Package, Profile,
     Sequence/Communication, State, Use case
 * - **Operational**
   - System migration
   - Activity, Class, Component, Composite Structure,
     Deployment, Object, Package, Profile,
     Sequence/Communication, State, Timing, Use case

Patrones observables
=====================

Analizando la tabla, emergen tres patrones:

**1. Núcleo estructural universal**

Los diagramas Class, Component, Composite Structure, Deployment,
Object, Package y Profile aparecen en prácticamente todos los
viewpoints y model types. Constituyen el núcleo estructural de
UML para la descripción arquitectónica.

**2. Diagramas de comportamiento selectivos**

Activity, Sequence/Communication y State aparecen únicamente en
model types que modelan flujos dinámicos: ciclos de vida de
datos, procesos de build/release, administración y operación del
sistema. No aparecen en viewpoints puramente estructurales
(Functional, Deployment físico).

**3. Use case restringido a Operational**

El diagrama de casos de uso aparece *únicamente* en el viewpoint
Operational (system administration, configuration, support,
migration) — no en el viewpoint Functional. Esto se debe a que
en Rozanski et al. el Functional viewpoint describe la estructura
funcional (qué componentes existen), mientras que Operational
describe cómo se gestiona el sistema en producción, donde los
casos de uso modelan las interacciones de los operadores con el
sistema.

**4. Timing restringido a concurrencia/operación**

El diagrama Timing solo aparece en contextos donde el tiempo es
un *concern* explícito: ciclo de vida de datos (Information),
administración y migración del sistema (Operational).

Relación con los diagramas actuales en IACT
=============================================

.. list-table::
 :header-rows: 1
 :widths: 22 22 56

 * - Viewpoint Rozanski
   - Vista 5+1 IACT
   - Observación
 * - Functional
   - Use Case View
   - ``use-case-view/`` tiene 13 ``mod-*.rst`` canónicos
     (uno por módulo funcional). ✓ Reestructurado (WP
     estructura-requisitos-arq-audit, Bloque A).
 * - Information
   - Domain Model
   - ``domain-model/`` tiene ``overview.rst`` + 26 archivos
     de clase canónica (uno por clase) + 8 ``bc-*.rst`` BC
     diagrams. ✓ Reestructurado (Bloque B).
 * - Concurrency
   - Process View
   - ``process-view/`` tiene 4 diagramas de concurrencia
     real: ETL pipeline, alertas paralelas, sesiones JWT,
     dashboard. ✓ Reestructurado (Bloque F, antes H-15).
 * - Development
   - Implementation + Design View
   - ``implementation-view/`` 12 ``mod-*.rst`` canónicos
     con stack de 5 capas. ``design-view/`` 12 ``mod-*.rst``
     con secuencias reales por módulo. ✓ Reestructurado
     (Bloques D y E).
 * - Deployment
   - Deployment View (+1)
   - ``deploy-view/`` tiene 3 variantes canónicas:
     ``deploy-estandar.rst``, ``deploy-auth-cache.rst``,
     ``deploy-etl.rst``. ✓ Reestructurado (Bloque C,
     antes H-10).
 * - Operational
   - Sin vista dedicada
   - No existe viewpoint Operational en IACT actualmente.

----

Referencias cruzadas
=====================

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **Contexto empírico**
   - :doc:`contexto-empirico`
 * - **Meta-modelo**
   - :doc:`metamodelo-descripcion`
 * - **Vistas arquitectónicas IACT**
   - :doc:`/arquitectura-tecnica/vistas-kruchten`
