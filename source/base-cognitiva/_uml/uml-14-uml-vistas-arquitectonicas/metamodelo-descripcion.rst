.. meta::
 :artefacto: UML_14_METAMODELO
 :tipo: Referencia — Metamodelo
 :dominio: base_cognitiva
 :subdominio: _uml
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uml-14-metamodelo:

=========================================================
Meta-modelo: descripción de arquitecturas multi-viewpoint
=========================================================

El meta-modelo define las relaciones entre los conceptos
fundamentales que intervienen al describir arquitecturas de
software desde múltiples viewpoints usando UML.

.. uml::
 :caption: Figura 1 — Meta-modelo para describir arquitecturas de software desde múltiples viewpoints

 @startuml uml14-metamodelo-viewpoints

 skinparam classAttributeIconSize 0
 skinparam classBorderColor #333333
 skinparam classBackgroundColor White
 skinparam ArrowColor #444444
 skinparam shadowing false

 class "Software Architecture\nDescription Language" as SADL
 class "Modeling Notation\nSet" as MNS
 class "Modeling Editor" as ModelingEditor
 class "Software Architecture\nDescription" as SAD
 class "Viewpoint\nFramework" as ViewpointFramework
 class "View" as ArchView
 class "Viewpoint" as Viewpoint
 class "Concern" as Concern
 class "Model Type" as ModelType

 SADL --> MNS : offers
 SADL --> ModelingEditor : supportedWith\n{0..n}
 SADL --> SAD : usedFor

 SAD --> ArchView : includes\n{1..n}

 ViewpointFramework --> Viewpoint : proposes\n{1..n}

 ArchView --> Viewpoint : instanceOf\n{1}
 Viewpoint --> Concern : dealsWith\n{1..n}

 ArchView --> ModelType : presentedBy\n{1..n}
 MNS --> ModelType : describes\n{1..n}
 ModelType --> Concern : solves

 @enduml

Descripción de las relaciones
===============================

.. list-table::
 :header-rows: 1
 :widths: 30 30 40

 * - Origen
   - Destino
   - Relación
 * - Software Architecture Description Language
   - Modeling Notation Set
   - **offers** — El lenguaje ofrece un conjunto de notaciones
     de modelado (p.ej. UML ofrece sus 14 tipos de diagramas).
 * - Software Architecture Description Language
   - Modeling Editor
   - **supportedWith** (0..n) — El lenguaje está soportado por
     cero o más herramientas de edición (p.ej. Enterprise
     Architect, MagicDraw, Papyrus).
 * - Software Architecture Description Language
   - Software Architecture Description
   - **usedFor** — El lenguaje se usa para crear descripciones
     de arquitectura.
 * - Software Architecture Description
   - View
   - **includes** (1..n) — Una descripción arquitectónica
     incluye una o más vistas.
 * - Viewpoint Framework
   - Viewpoint
   - **proposes** (1..n) — Un framework de viewpoints define
     uno o más viewpoints (p.ej. Kruchten 4+1, Rozanski et al.).
 * - View
   - Viewpoint
   - **instanceOf** (1) — Cada view es instancia de exactamente
     un viewpoint.
 * - Viewpoint
   - Concern
   - **dealsWith** (1..n) — Cada viewpoint aborda uno o más
     *concerns* del sistema.
 * - View
   - Model Type
   - **presentedBy** (1..n) — Una view se presenta mediante
     uno o más tipos de modelo (p.ej. diagrama de clases,
     diagrama de secuencias).
 * - Modeling Notation Set
   - Model Type
   - **describes** (1..n) — El conjunto de notaciones describe
     los tipos de modelo disponibles.
 * - Model Type
   - Concern
   - **solves** — Cada tipo de modelo resuelve (representa)
     determinados *concerns*.

Interpretación para el proyecto IACT
======================================

Aplicando el meta-modelo al proyecto:

.. list-table::
 :header-rows: 1
 :widths: 30 70

 * - Concepto del meta-modelo
   - Instancia en IACT
 * - Software Architecture Description Language
   - UML (con PlantUML como sintaxis concreta)
 * - Modeling Notation Set
   - Los 9 tipos de diagramas UML usados en el proyecto
 * - Modeling Editor
   - PlantUML + Sphinx (generación automática)
 * - Viewpoint Framework
   - Modelo 5+1 (variante DDD de Kruchten)
 * - Viewpoint (×6)
   - Domain Model, Use Case View, Design View,
     Implementation View, Process View, Deployment View
 * - View
   - Cada directorio: ``use-case-view/``,
     ``design-view/``, ``deploy-view/``, etc.
 * - Model Type
   - Diagrama de casos de uso, secuencias, componentes,
     distribución, estados, actividades, clases
 * - Concern
   - Comportamiento funcional, estructura de código,
     despliegue físico, concurrencia, dominio del negocio

----

Referencias cruzadas
=====================

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **Contexto empírico**
   - :doc:`contexto-empirico`
 * - **Framework Rozanski (Tabla 1)**
   - :doc:`framework-rozanski`
