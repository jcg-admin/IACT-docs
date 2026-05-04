.. meta::
 :artefacto: UML_14_PROCESO
 :tipo: Referencia — Proceso de Definicion Arquitectonica
 :dominio: base_cognitiva
 :subdominio: _uml
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uml-14-proceso:

=======================================================
El Proceso de Definición Arquitectónica
=======================================================

Fuente: Rozanski & Woods, *Software Systems Architecture* — Cap. 7.

La definición de arquitectura comienza temprano en el ciclo de vida
del proyecto, cuando el scope y los requisitos a menudo aún son poco
claros y la visión actual del sistema puede diferir sustancialmente de
lo que se construirá finalmente.

----

Principios rectores
=====================

Para que un proceso de definición arquitectónica sea exitoso, debe
adherirse a los siguientes principios:

.. list-table::
 :header-rows: 1
 :widths: 22 78

 * - Principio
   - Descripción
 * - **Dirigido por concerns**
   - Los concerns de los stakeholders son la entrada central —
     aunque no la única — del proceso. El proceso debe equilibrar
     esos concerns eficazmente donde conflicten o tengan
     implicaciones incompatibles.
 * - **Comunicación efectiva**
   - Debe fomentar la comunicación efectiva de decisiones
     arquitectónicas, principios y la solución misma a los
     stakeholders.
 * - **Conformidad continua**
   - Debe asegurar, de forma continua, que las decisiones y
     principios arquitectónicos se respetan a lo largo del ciclo
     de vida hasta el despliegue final.
 * - **Estructurado**
   - Debe comprender una serie de pasos o tareas con una
     definición clara de los objetivos, entradas y salidas de
     cada paso. Las salidas de un paso son las entradas de los
     pasos subsiguientes.
 * - **Pragmático**
   - Debe considerar problemas del mundo real: falta de tiempo o
     dinero, escasez de habilidades técnicas específicas,
     requisitos poco claros o cambiantes, contexto existente y
     consideraciones organizacionales.
 * - **Flexible**
   - Debe poder adaptarse a circunstancias particulares (enfoque
     de toolkit o framework). Se usan los elementos que se
     necesitan y se ignoran el resto.
 * - **Agnóstico de tecnología**
   - No debe imponer ninguna tecnología, patrón arquitectónico o
     estilo de desarrollo específico, ni dictar ningún estilo
     particular de modelado, diagramado o documentación.
 * - **Integrable con el SDLC**
   - Debe integrarse con el ciclo de vida de desarrollo de
     software elegido.
 * - **Alineado con buenas prácticas**
   - Debe alinearse con buenas prácticas de ingeniería de software
     y estándares de gestión de calidad (p.ej. ISO 9001) para
     integrarse fácilmente con enfoques existentes.

----

Resultados del proceso
========================

El objetivo principal de la definición de arquitectura es desarrollar
una arquitectura sólida y gestionar la producción y mantenimiento de
todos los elementos de la AD. Los resultados secundarios deseables son:

.. list-table::
 :header-rows: 1
 :widths: 30 70

 * - Resultado
   - Descripción
 * - **Clarificación de requisitos**
   - Los stakeholders pueden no estar completamente claros sobre
     lo que quieren. El proceso ayuda a concretarlos.
 * - **Gestión de expectativas**
   - La arquitectura inevitablemente necesita hacer compromisos.
     Es mejor hacerlos visibles y claramente entendidos temprano.
 * - **Identificación y evaluación de opciones**
   - Raramente existe solo una solución. El análisis revela las
     fortalezas y debilidades de cada opción y justifica la
     solución elegida.
 * - **Criterios de aceptación arquitectónica**
   - La definición de arquitectura debe llevar a una comprensión
     clara de las condiciones que deben cumplirse antes de que
     los stakeholders acepten la arquitectura como conforme a
     sus requisitos.
 * - **Entradas al diseño**
   - Orientación y restricciones para el proceso de diseño
     software que ayudan a garantizar la integridad de la
     arquitectura.

----

Contexto del proceso — Modelo de los Tres Picos
=================================================

La arquitectura forma el puente entre los requisitos y el diseño,
realizando los compromisos necesarios para satisfacer las demandas
de ambos. En términos de proceso, la definición de arquitectura
se sitúa entre el análisis de requisitos y la construcción del
software (diseño, código y pruebas).

El **Modelo de los Tres Picos** (*Three Peaks Model*, extensión del
Twin Peaks Model de Nuseibeh) ilustra este contexto:

.. uml::
 :caption: Figura 7-1 — Contexto de la Definición Arquitectónica: el Modelo de los Tres Picos

 @startuml uml14-tres-picos

 skinparam rectangleBorderColor #555555
 skinparam rectangleBackgroundColor #F9F9F9
 skinparam ArrowColor #555555
 skinparam shadowing false
 skinparam noteBorderColor #888888
 skinparam noteBackgroundColor #FFFCE6

 rectangle "SPECIFICATION" as SpecLabel #White {
   rectangle "Requirements\n\n\n(Independent)" as ReqPeak #E8F4FD
 }

 rectangle "" as MidLabel #White {
   rectangle "Architecture\n\n\n" as ArchPeak #D5E8D4
 }

 rectangle "DESIGN" as DesignLabel #White {
   rectangle "Construction\n\n\n(Dependent)" as ConsPeak #FFE6CC
 }

 note top of ReqPeak
   Level of Detail
   ▲ General
   |
   ▼ Detailed
 end note

 ReqPeak <--> ArchPeak : intertwined\n(specification)
 ArchPeak <--> ConsPeak : intertwined\n(design)

 @enduml

Los tres triángulos (picos) representan las actividades principales
de desarrollo: análisis de requisitos, definición de arquitectura y
construcción. Las flechas espirales muestran cómo los requisitos y
la arquitectura, así como la arquitectura y la construcción, están
entrelazados a un grado progresivamente mayor durante el desarrollo.

Relaciones clave entre arquitectura, requisitos y construcción:

- El **análisis de requisitos** provee el contexto para la definición
  de arquitectura definiendo el scope y las propiedades funcionales y
  de calidad deseadas del sistema.
- La **definición de arquitectura** a menudo revela requisitos
  inconsistentes y faltantes, y ayuda a los stakeholders a entender
  los costes y complejidades relativos de satisfacer sus concerns.
  Esto retroalimenta el análisis de requisitos para clarificar,
  añadir y priorizar requisitos.
- Cuando la definición de arquitectura resulta en una arquitectura
  que parece satisfacer un conjunto aceptable de requisitos de usuario,
  se puede planificar la **construcción** del sistema.
- La **construcción** se organiza típicamente como un conjunto de
  entregas incrementales. Cada pieza de construcción proporciona
  retroalimentación sobre la efectividad y utilidad de la arquitectura
  en uso — por lo que hay actividad de definición arquitectónica a
  lo largo de todo el ciclo de vida.

----

Actividades del proceso
=========================

El proceso de definición arquitectónica supone que antes de comenzar
están disponibles y aceptados:

- Una definición del scope y contexto de base del sistema.
- Una definición de los concerns clave de los stakeholders.
- Los stakeholders correctos han sido identificados y comprometidos.

El siguiente diagrama de actividad muestra cómo la definición de
arquitectura se relaciona con sus actividades de soporte:

.. uml::
 :caption: Figura 7-2 — Actividades de soporte a la Definición Arquitectónica

 @startuml uml14-process-activities

 skinparam ArrowColor #444444
 skinparam ActivityBorderColor #333333
 skinparam ActivityBackgroundColor #F5F5F5
 skinparam ActivityDiamondBackgroundColor #FFF9C4
 skinparam shadowing false
 skinparam NoteBackgroundColor #FFFCE6
 skinparam NoteBorderColor #888888

 start

 :Define Initial Scope\nand Context;

 :Engage\nStakeholders;

 :Capture First-Cut\nConcerns;

 note left
   INPUTS
   ....
   Stakeholder
   Concerns
   ....
   Scope and
   Context
 end note

 :Define Architecture;

 note right
   OUTPUTS
   ....
   Architectural
   Description
   ....
   Guidelines and
   Constraints
 end note

 if (skeleton required?) then ([ skeleton required ])
   :Create Skeleton\nSystem;
   note right
     skeleton
     system
   end note
 else ([ skeleton not required ])
 endif

 stop

 @enduml

Las actividades son:

1. **Definir el scope e contexto inicial** — establecer los límites
   del sistema y su relación con el entorno.
2. **Comprometer a los stakeholders** — identificar y enfranchiser a
   todas las partes interesadas relevantes.
3. **Capturar los concerns de primera pasada** — obtener los concerns
   arquitectónicos clave de los stakeholders.
4. **Definir la arquitectura** — la actividad central: diseñar,
   documentar y validar la arquitectura.
5. **Crear el sistema esqueleto** (opcional) — una implementación
   esqueleto puede ser valiosa como validación práctica de la
   arquitectura, prueba de credibilidad ante stakeholders y marco
   de trabajo para el equipo de desarrollo.

**Entradas al proceso:**

- *Scope and Context* — definición del alcance y contexto del sistema
- *Stakeholder Concerns* — concerns capturados de los stakeholders

**Salidas del proceso:**

- *Architectural Description* — la AD completa (vistas, viewpoints,
  perspectivas, principios)
- *Guidelines and Constraints* — directrices y restricciones para
  guiar la construcción

----

Aplicación al proyecto IACT
==============================

El proceso de definición arquitectónica de Rozanski & Woods se
implementa en IACT mediante la metodología THYROX. La siguiente
tabla muestra la correspondencia:

Modelo de los Tres Picos en THYROX
--------------------------------------

.. list-table::
 :header-rows: 1
 :widths: 25 25 50

 * - Tres Picos (Rozanski)
   - THYROX
   - Artefactos IACT
 * - **Requirements** (Pico 1)
   - Stages 1-3 (DISCOVER, BASELINE, DIAGNOSE)
   - `source/requisitos/` — BReqs, UCs, FRs, RNFs
 * - **Architecture** (Pico 2)
   - Stages 4-7 (CONSTRAINTS, STRATEGY, PLAN, DESIGN)
   - `source/arquitectura-tecnica/` — vistas 5+1
 * - **Construction** (Pico 3)
   - Stages 8-10 (PLAN EXECUTION, PILOT, IMPLEMENT)
   - Implementación del sistema, diagramas ejecutables

Actividades del proceso en THYROX
------------------------------------

.. list-table::
 :header-rows: 1
 :widths: 30 20 50

 * - Actividad (Rozanski Cap. 7)
   - Stage THYROX
   - Resultado concreto en IACT
 * - Define Initial Scope and Context
   - Stage 1 — DISCOVER
   - `discover/*-analysis.md` con H-01..H-NN
 * - Engage Stakeholders
   - Stage 1 — DISCOVER
   - Stakeholder map en análisis; `normativa/gobernanza/`
 * - Capture First-Cut Concerns
   - Stages 2-3 — BASELINE / DIAGNOSE
   - Concerns documentados: RBAC, auditoría, pipeline ETL, IVR
 * - Define Architecture
   - Stages 4-7 — CONSTRAINTS/STRATEGY/PLAN/DESIGN
   - `arquitectura-tecnica/` vistas 5+1 + perspectivas Rozanski
 * - Create Skeleton System
   - Stage 9 — PILOT/VALIDATE
   - Prototipo o spike de validación antes de implementación masiva

Principios del proceso vs. THYROX
-------------------------------------

.. list-table::
 :header-rows: 1
 :widths: 30 70

 * - Principio Rozanski
   - Implementación en THYROX/IACT
 * - **Dirigido por concerns**
   - H-NN en `discover/` capturan concerns. Gate Stage N→N+1
     requiere concerns documentados antes de avanzar.
 * - **Estructurado (pasos claros)**
   - 12 Stages con exit criteria y tollgates definidos. Plan de
     ejecución con T-NNN en `plan-execution/`.
 * - **Pragmático**
   - Work packages con timestamp real. Tasks atómicas. Sin
     formalismo innecesario.
 * - **Flexible (toolkit)**
   - WPs pueden usar solo los stages relevantes. El proceso se
     adapta a la naturaleza del trabajo (audit, feature, fix).
 * - **Agnóstico de tecnología**
   - THYROX no impone stack. PlantUML/Sphinx son convenciones,
     no prescripciones del proceso arquitectónico.
 * - **Integrable con SDLC**
   - THYROX coexiste con git-flow, PRs y CI/CD. Los stages se
     mapean a ramas y work packages.
 * - **Conformidad continua**
   - Stage 11 TRACK/EVALUATE verifica conformidad. Stage 12
     STANDARDIZE formaliza patrones reutilizables.

Inputs y outputs para IACT
-----------------------------

**Inputs al proceso (actuales en este WP):**

- *Scope and Context:* `arquitectura-tecnica/` — 815 archivos RST
  auditados (WP `2026-05-04-08-32-37`)
- *Stakeholder Concerns:* H-01..H-15 documentados en `discover/`

**Outputs esperados:**

- *Architectural Description:* `arquitectura-tecnica/` reestructurada
  con las 6 vistas 5+1 en nivel correcto (módulo-indexado)
- *Guidelines and Constraints:* STD-011 (aliases), ADR-GOB-002
  (PlantUML), normativa de viewpoints Rozanski

----

Referencias cruzadas
=====================

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **El Arquitecto (Cap. 5)**
   - :doc:`arquitecto-y-proceso`
 * - **Perspectivas (Cap. 4)**
   - :doc:`perspectivas-arquitectonicas`
 * - **Vistas y Viewpoints (Cap. 3)**
   - :doc:`vistas-y-viewpoints`
 * - **WP activo de auditoría**
   - `.thyrox/context/work/2026-05-04-08-32-37-estructura-requisitos-arq-audit/`
 * - **Vistas arquitectónicas IACT**
   - :doc:`/arquitectura-tecnica/vistas-kruchten`
