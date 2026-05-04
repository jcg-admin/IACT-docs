.. meta::
 :artefacto: UML_14_ARQUITECTO
 :tipo: Referencia — El Arquitecto y el Proceso
 :dominio: base_cognitiva
 :subdominio: _uml
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uml-14-arquitecto:

=======================================================
El Arquitecto y el Proceso de Definición Arquitectónica
=======================================================

Fuente: Rozanski & Woods, *Software Systems Architecture* — Cap. 5.

Este capítulo cierra la Parte I del libro añadiendo al modelo conceptual
los dos elementos finales: el proceso de definición arquitectónica y el
arquitecto.

----

Proceso de definición arquitectónica
======================================

La **definición de arquitectura** es un proceso mediante el cual:

1. Se capturan las necesidades y concerns de los stakeholders.
2. Se diseña una arquitectura que satisfaga esas necesidades.
3. La arquitectura se describe de forma completa e inequívoca a través de una AD.

El rol del arquitecto permanece activo más allá de la creación de la AD,
a través de la construcción, aceptación y entrega del sistema (posiblemente
con un nivel reducido de participación).

----

Modelo conceptual completo — Figura 5-3
=========================================

Esta figura extiende el modelo de Figura 4-3 (Perspectivas en contexto)
añadiendo el **Arquitecto** y el **Proceso de Definición Arquitectónica**:

.. uml::
 :caption: Figura 5-3 — Definición de arquitectura y el Arquitecto en contexto

 @startuml uml14-arquitecto-modelo-completo

 skinparam classAttributeIconSize 0
 skinparam classBorderColor #333333
 skinparam classBackgroundColor White
 skinparam ArrowColor #444444
 skinparam shadowing false

 class "Architectural\nElement" as ArchElement
 class "Interelement\nRelationship" as InterRel
 class "Architecture" as Arch
 class "System" as System
 class "Stakeholder" as Stakeholder
 class "Concern" as Concern
 class "Architectural\nDescription (AD)" as ArchDescription
 class "View" as ArchView
 class "Viewpoint" as Viewpoint
 class "Perspective" as Perspective
 class "Architect" as Architect
 class "Architecture\nDefinition Process" as ArchDefProcess

 Arch "comprises 2..n" o-- ArchElement
 ArchElement --> InterRel : relates 1..n
 InterRel --> ArchElement : 1..n

 System --> Arch : has an
 ArchDescription --> Arch : documents\narchitecture for\n0..n
 ArchDescription "comprises 1..n" *-- ArchView

 System --> Stakeholder : addresses the\nneeds of 1..n
 Stakeholder --> Concern : has 1..n

 ArchView --> Viewpoint : conforms to\n0..n
 Viewpoint --> Concern : addresses 1..n

 Perspective --> Concern : addresses 1..n
 Perspective --> ArchView : shaped by\n0..n

 Architect --> Stakeholder : captures the\nconcerns of
 Architect --> Arch : designs
 Architect --> ArchDescription : creates\nand owns
 Architect --> ArchDefProcess : follows
 ArchDefProcess --> Arch : guides the\ndefinition of\n1..n

 @enduml

Relaciones añadidas respecto a Figura 4-3:

- El **arquitecto** captura y consolida los concerns de los stakeholders.
- El **arquitecto** diseña una arquitectura que satisface esos concerns.
- El **arquitecto** crea y posee la AD.
- Un **proceso de definición arquitectónica** guía la definición de la
  arquitectura.
- El **arquitecto** sigue el proceso de definición arquitectónica para
  llevar a cabo todas estas tareas.

----

El rol del arquitecto
======================

No existe una única definición comúnmente aceptada del rol del arquitecto
de software. En la mayoría de las organizaciones, "arquitecto" es un rol
de liderazgo tecnológico. Las cuatro responsabilidades principales son:

1. **Identificar y comprometer a los stakeholders**
2. **Entender y capturar sus concerns**
3. **Crear y apropiarse de la AD**
4. **Asumir un rol de liderazgo en la realización de la arquitectura**

Liderazgo arquitectónico
--------------------------

Desde la perspectiva del sistema, el liderazgo arquitectónico incluye
las actividades orientadas a las personas que ayudan a asegurar la
implementación exitosa del sistema:

- Explicar y promover la arquitectura ante los stakeholders de negocio
  y tecnológicos, y justificar los principios y decisiones que la
  sustentan.
- Proporcionar inputs y soporte para las tareas de planificación y
  estimación.
- Participar en los procesos de control de cambios.
- Asumir la responsabilidad y firmar la finalización de los hitos
  técnicos.
- Ayudar a resolver los problemas que surjan durante el desarrollo.
- Asumir roles de desarrollo más específicos como autoridad de diseño.
- Revisar documentación y posiblemente código.

----

Responsabilidades del arquitecto
==================================

.. list-table::
 :header-rows: 1
 :widths: 5 95

 * - #
   - Responsabilidad
 * - 1
   - Asegurar que el scope, contexto y restricciones están documentados
     y aceptados.
 * - 2
   - Identificar, comprometer y enfranchiser a los stakeholders.
 * - 3
   - Facilitar la toma de decisiones a nivel de sistema, asegurando que
     se toman con la mejor información disponible y están alineadas con
     las necesidades de los stakeholders.
 * - 4
   - Arbitrar y asegurar que se alcanza consenso cuando las necesidades
     de los stakeholders están en conflicto o son incompatibles.
 * - 5
   - Arbitrar y asegurar que se alcanza consenso cuando se deben hacer
     compromisos arquitectónicos (por ejemplo, rendimiento vs. flexibilidad
     o seguridad vs. facilidad de uso).
 * - 6
   - Capturar e interpretar input de especialistas técnicos y de dominio.
 * - 7
   - Definir y documentar la arquitectura del sistema.
 * - 8
   - Definir y documentar estrategias, estándares y directrices para
     guiar la construcción y despliegue del sistema.
 * - 9
   - Asegurar que la arquitectura satisface los atributos de calidad del
     sistema.
 * - 10
   - Desarrollar y poseer la AD (gestionar todos los cambios a la misma).
 * - 11
   - Ayudar a asegurar que los principios y estándares arquitectónicos
     acordados se aplican al sistema o producto terminado.
 * - 12
   - Proporcionar liderazgo técnico.

----

Especializaciones arquitectónicas
====================================

.. list-table::
 :header-rows: 1
 :widths: 22 78

 * - Especialización
   - Descripción
 * - **Product Architect**
   - Responsable de la entrega de una o más versiones de un producto
     software a clientes externos. Permanece asociado al producto en
     múltiples ciclos de release y supervisa la integridad técnica del
     producto.
 * - **Domain Architect**
   - Especialización de la función arquitectónica general en un dominio
     particular: arquitectura de negocio, datos, red, etc. Valioso para
     sistemas grandes o para cubrir brechas de conocimiento.
 * - **Infrastructure Architect**
   - Posee la provisión de infraestructura hardware y software. Incluye
     centros de datos, servidores, almacenamiento, redes, seguridad
     empresarial, DBMS, mensajería, identidad.
 * - **Solution Architect**
   - Toma una visión amplia y de alto nivel de toda la solución. Se
     enfoca en cuestiones más amplias que la tecnología: cambio de
     proceso de negocio, adquisición, personal.
 * - **Enterprise Architect**
   - Responsable de la arquitectura de sistemas de información
     cross-system de toda la empresa. También se ocupa de principios,
     estándares y políticas a nivel corporativo.

----

Contexto organizacional
=========================

La siguiente tabla compara el rol del arquitecto con otros roles clave
en proyectos de desarrollo:

.. list-table::
 :header-rows: 1
 :widths: 22 78

 * - Rol
   - Relación con el arquitecto
 * - **Business Analyst**
   - Captura y documenta requisitos de negocio detallados, enfocándose
     en stakeholders de la comunidad de usuarios. El arquitecto se apoya
     en el BA especialmente al tratar con vistas de interés para
     adquirentes, usuarios y evaluadores.
 * - **Project Manager**
   - Responsable de asegurar la entrega del producto. El arquitecto
     ayuda al PM a desarrollar planes o evaluarlos, y proporciona
     información técnica, feedback, asesoría y evaluación de riesgos.
     La relación más productiva es el modelo de **partnership**: el PM
     se enfoca en stakeholders, planes, presupuestos, personal y plazos;
     el arquitecto se enfoca en stakeholders, concerns, scope, requisitos,
     vistas y modelos.
 * - **Design Authority**
   - Asume la responsabilidad general de la calidad de los diseños de
     elementos internos del sistema. El arquitecto a menudo ocupa este
     rol cuando el proyecto avanza a la fase de diseño. **Regla clave:**
     si la decisión tiene impacto significativo en stakeholders
     importantes o requiere compromisos entre necesidades de stakeholders,
     el arquitecto debe ser responsable. Si la decisión solo es visible
     dentro del equipo de desarrollo, probablemente es un tema de Design
     Authority.
 * - **Technology Specialist**
   - Proporciona expertise detallado en un área específica. El arquitecto
     provee amplitud; el especialista provee profundidad. El especialista
     evalúa la arquitectura para viabilidad técnica y detecta pitfalls
     temprano.
 * - **Developers**
   - El arquitecto mantiene un rol de liderazgo tecnológico durante
     construcción y pruebas para asegurar que el equipo se adhiere al
     espíritu y la letra de la AD. Incluye mentoría, revisión de diseños,
     arbitraje de disputas tecnológicas y participación en integración
     y pruebas del sistema.

.. admonition:: Principio

 El arquitecto provee y supervisa la amplitud arquitectónica y trabaja
 estrechamente con especialistas orientados al negocio y a la tecnología
 que proveen la profundidad especializada.

----

Habilidades del arquitecto
============================

.. list-table::
 :header-rows: 1
 :widths: 22 78

 * - Habilidad
   - Descripción
 * - **Captura de información**
   - Capturar tipos de información de stakeholders con diferentes
     intereses y niveles de expertise. Mantener a los stakeholders
     enfocados en los concerns arquitectónicos importantes y "profundizar"
     donde sea apropiado.
 * - **Facilitación**
   - Gestionar workshops y reuniones eficazmente, especialmente con una
     mezcla de stakeholders senior y junior, o cuando hay conflicto.
 * - **Negociación**
   - Alcanzar consenso entre stakeholders con concerns a menudo
     conflictivos o incompatibles. Entender y actuar sobre lo que
     realmente tiene valor para cada parte.
 * - **Comunicación**
   - Comunicar la arquitectura de forma efectiva a diferentes
     stakeholders con diferentes intereses — en persona o por documentos,
     concisamente o en detalle.
 * - **Flexibilidad**
   - Aprender rápidamente sobre áreas de negocio y tecnologías no
     familiares. Hacer cambios de dirección rápidos cuando sea apropiado.
     Saber cuándo mantener la postura.

----

Aplicación al proyecto IACT
==============================

Mapeando los conceptos de Rozanski & Woods al proyecto IACT:

.. list-table::
 :header-rows: 1
 :widths: 30 35 35

 * - Concepto Rozanski
   - Instancia en IACT
   - Evidencia / Artefacto
 * - **Architecture Definition Process**
   - Metodología THYROX (Stages 1-12: DISCOVER → STANDARDIZE)
   - `.thyrox/context/work/` + `ROADMAP.md`
 * - **Architect**
   - Arquitecto/lead técnico del proyecto
   - `source/arquitectura-tecnica/`
 * - **Architectural Description (AD)**
   - `source/arquitectura-tecnica/` (todas las vistas 5+1)
   - `vistas-kruchten.rst`
 * - **Design Authority**
   - Revisión de diagramas en PRs y vistas 5+1
   - `arquitectura-tecnica/*/diagramas/`
 * - **Business Analyst**
   - Equipo que define `source/requisitos/`
   - `requisitos/casos-uso/`, `requisitos/business-requirements/`
 * - **Technology Specialist**
   - Especialistas por dominio (RBAC, pipeline ETL, IVR, auth)
   - `modulos/*/responsabilidades.rst`
 * - **Stakeholders**
   - AGR_ADMIN, AGR_OPERADOR, AGR_AUDITOR + instituciones
   - `normativa/gobernanza/`, `requisitos/actores/`
 * - **Concerns**
   - RBAC granular, auditoría regulatoria, pipeline ETL,
     disponibilidad, seguridad
   - `normativa/restricciones/cnst-*.rst`

Especialización aplicable a IACT
-----------------------------------

IACT combina elementos de:

- **Solution Architect** — visión amplia de la solución incluyendo
  cambio de proceso institucional y requisitos regulatorios.
- **Domain Architect** — especialización en arquitectura de datos
  (IVR read-only, ETL, modelo RBAC) y arquitectura de seguridad.
- **Infrastructure Architect** — diseño de nodos de procesamiento,
  red, almacenamiento y restricciones CNST-007.

Proceso THYROX como Architecture Definition Process
------------------------------------------------------

La metodología THYROX implementa el proceso de definición
arquitectónica de Rozanski & Woods en 12 stages:

.. list-table::
 :header-rows: 1
 :widths: 12 20 68

 * - Stage
   - THYROX
   - Actividad arquitectónica (Rozanski)
 * - 1
   - DISCOVER
   - Captura inicial de concerns y contexto del sistema
 * - 2
   - BASELINE
   - Inventario del estado actual de la arquitectura
 * - 3
   - DIAGNOSE
   - Análisis adversarial de la AD existente
 * - 4
   - CONSTRAINTS
   - Documentar restricciones que acotan las decisiones
 * - 5
   - STRATEGY
   - Definir principios y dirección arquitectónica
 * - 6
   - PLAN
   - Planificación de la AD objetivo
 * - 7
   - DESIGN/SPECIFY
   - Diseño detallado de vistas y viewpoints
 * - 8
   - PLAN EXECUTION
   - Descomposición en tareas ejecutables (T-NNN)
 * - 9
   - PILOT/VALIDATE
   - Validación de decisiones antes de implementación masiva
 * - 10
   - IMPLEMENT
   - Construcción de la AD (diagramas, documentos)
 * - 11
   - TRACK/EVALUATE
   - Evaluación de conformidad con la AD
 * - 12
   - STANDARDIZE
   - Formalización de estándares y patrones reutilizables

----

Referencias cruzadas
=====================

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **Modelo base (Caps. 3-4)**
   - :doc:`vistas-y-viewpoints` · :doc:`perspectivas-arquitectonicas`
 * - **Meta-modelo (Figura 1)**
   - :doc:`metamodelo-descripcion`
 * - **Framework Rozanski**
   - :doc:`framework-rozanski`
 * - **Vistas arquitectónicas IACT**
   - :doc:`/arquitectura-tecnica/vistas-kruchten`
