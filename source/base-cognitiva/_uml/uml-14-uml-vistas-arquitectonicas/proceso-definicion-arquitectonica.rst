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

 rectangle " " as MidLabel #White {
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

 ReqPeak <-> ArchPeak : intertwined\n(specification)
 ArchPeak <-> ConsPeak : intertwined\n(design)

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

Habiendo definido el scope e contexto inicial con los stakeholders
adquirentes, se identifican y comprometen los demás stakeholders
importantes cuyos concerns deben ser abordados. Capturar sus concerns
proporciona una entrada primaria, junto con el scope y contexto, a la
definición de arquitectura. Una vez que se tiene una AD, se puede
crear un sistema esqueleto que actuará como prototipo evolucionable.

Las tablas 7-1 a 7-5 describen cada actividad en detalle:

.. list-table:: Tabla 7-1 — Definir el Scope e Contexto Inicial
 :header-rows: 0
 :widths: 20 80

 * - **Objetivo**
   - Delimitar claramente el comportamiento y las responsabilidades
     del sistema, y el contexto operacional y organizacional dentro
     del cual el sistema existe.
 * - **Entradas**
   - Necesidades y visión de los adquirentes; estrategia
     organizacional; arquitectura IT del entorno.

     *En IACT:* requisitos de las instituciones; normativa
     aplicable (CNST-007, Ley N); arquitectura IT existente
     (IVR legacy, bases de datos institucionales).
 * - **Salidas**
   - Declaraciones iniciales de los objetivos del sistema y qué
     está incluido y excluido de sus responsabilidades, junto con
     una definición inicial del contexto. Pueden capturarse en un
     borrador de la vista Context.

     *En IACT:* alcance (gestión de acciones ciudadanas), restricción
     fundamental (IVR es fuente de datos externa, solo lectura),
     borrador de vista Context con IVR como actor externo.
 * - **Notas**
   - Este paso es principalmente un proceso de comprender los
     objetivos estratégicos y organizacionales y cómo el sistema
     ayuda a cumplirlos, junto con un análisis de qué otros sistemas
     necesita integrar. El scope puede cambiar durante la definición
     de arquitectura con acuerdo de los stakeholders.

.. list-table:: Tabla 7-2 — Comprometer a los Stakeholders
 :header-rows: 0
 :widths: 20 80

 * - **Objetivo**
   - Identificar los stakeholders importantes del sistema y crear
     una relación de trabajo con ellos.
 * - **Entradas**
   - Scope y contexto del borrador de la vista Context; estructura
     organizacional.
 * - **Salidas**
   - Definición de cada grupo de stakeholders, con una o más
     personas nombradas y comprometidas que representarán al grupo.

     *En IACT:* grupos AGR_ADMIN, AGR_OPERADOR, AGR_AUDITOR
     con representantes nombrados por institución participante.
 * - **Notas**
   - Implica entender el contexto organizacional e identificar las
     personas clave que se verán afectadas por el sistema.
     En IACT los tres grupos tienen concerns muy distintos:
     AGR_ADMIN define permisos RBAC, AGR_OPERADOR ejecuta acciones,
     AGR_AUDITOR requiere trazabilidad regulatoria. Identificarlos
     temprano evita conflictos posteriores en la definición de
     concerns.

.. list-table:: Tabla 7-3 — Capturar los Concerns de Primera Pasada
 :header-rows: 0
 :widths: 20 80

 * - **Objetivo**
   - Comprender claramente los concerns que cada grupo de stakeholders
     tiene sobre el sistema y las prioridades que asignan a cada uno.
 * - **Entradas**
   - Lista de stakeholders; scope y contexto.
 * - **Salidas**
   - Definición inicial de un conjunto de concerns priorizados para
     cada grupo de stakeholders.

     *En IACT:* RBAC granular (AGR_ADMIN), disponibilidad del
     pipeline ETL (AGR_OPERADOR), trazabilidad regulatoria y
     cobertura CNST-007 (AGR_AUDITOR), separación IVR read-only
     y seguridad de datos (instituciones adquirentes).
 * - **Notas**
   - Suele comenzar con las reuniones iniciales con stakeholders.
     En IACT, los concerns suelen estar en conflicto: seguridad
     (acceso mínimo) vs. operabilidad (acceso amplio). Estos
     conflictos se capturan en `normativa/restricciones/cnst-*.rst`
     y orientan los compromisos arquitectónicos.

.. list-table:: Tabla 7-4 — Definir la Arquitectura
 :header-rows: 0
 :widths: 20 80

 * - **Objetivo**
   - Crear la AD del sistema documentando las decisiones
     arquitectónicas que satisfacen los concerns identificados.
 * - **Entradas**
   - Lista de stakeholders; concerns priorizados; restricciones
     conocidas.

     *En IACT:* H-01..H-15 del WP de auditoría; CNST-007 y
     restricciones de seguridad; normativa regulatoria.
 * - **Salidas**
   - AD completa; directrices y restricciones para la construcción.

     *En IACT:* `arquitectura-tecnica/` con las 6 vistas 5+1
     (Domain Model, Use Case View, Design View, Implementation
     View, Process View, Deployment View); STD-011 y ADR-GOB-*
     como directrices.
 * - **Notas**
   - Actividad central del proceso. Se describe en detalle en la
     sección de Architecture Definition Activities de este
     capítulo. En IACT se implementa en Stages 4-7 de THYROX
     (CONSTRAINTS, STRATEGY, PLAN, DESIGN/SPECIFY).

.. list-table:: Tabla 7-5 — Crear el Sistema Esqueleto (opcional)
 :header-rows: 0
 :widths: 20 80

 * - **Objetivo**
   - Paso opcional para crear una implementación funcional limitada
     de la arquitectura que pueda evolucionar hacia el sistema
     entregado durante la construcción.
 * - **Entradas**
   - AD; directrices y restricciones asociadas.
 * - **Salidas**
   - Sistema funcional limitado que ilustra que el sistema puede
     abordar al menos uno de sus escenarios.

     *En IACT:* flujo completo de acción ciudadana con RBAC +
     auditoría demostrado en un entorno de integración controlado.
 * - **Notas**
   - Si se tiene el tiempo y los recursos, forma un puente efectivo
     entre la definición de arquitectura y la construcción de
     software. El sistema esqueleto actúa como validación de la
     arquitectura y prueba de credibilidad ante los stakeholders.

     *En IACT:* corresponde al Stage 9 PILOT/VALIDATE de THYROX.
     Valida que el modelo RBAC granular es operable y que la
     integración IVR read-only funciona según lo descrito en la AD.

**Entradas al proceso:**

- *Scope and Context* — definición del alcance y contexto del sistema
- *Stakeholder Concerns* — concerns capturados de los stakeholders

**Salidas del proceso:**

- *Architectural Description* — la AD completa (vistas, viewpoints,
  perspectivas, principios)
- *Guidelines and Constraints* — directrices y restricciones para
  guiar la construcción

----

Actividades de definición arquitectónica — proceso iterativo
==============================================================

La mayor dificultad del arquitecto es la cantidad de incertidumbre y
cambio durante el trabajo con los stakeholders. El scope probablemente
cambie a medida que emergen las implicaciones de incluir o excluir
ciertas funcionalidades. Los requisitos funcionales y de propiedades
de calidad también evolucionarán.

Por esta razón, el proceso de definición arquitectónica es **iterativo**.
Es necesario repetir los pasos principales varias veces antes de
producir una AD terminada. La arquitectura seguirá evolucionando
conforme se desarrolla el sistema.

.. uml::
 :caption: Figura 7-3 — Detalle del proceso de Definición Arquitectónica

 @startuml uml14-arch-definition-detail

 skinparam ArrowColor #444444
 skinparam ActivityBorderColor #333333
 skinparam ActivityBackgroundColor #F5F5F5
 skinparam ActivityDiamondBackgroundColor #FFF9C4
 skinparam shadowing false

 start

 :1. Consolidate the Inputs;
 :2. Identify Scenarios;
 :3. Identify Relevant\nArchitectural Styles;
 :4. Produce a Candidate\nArchitecture;
 :5. Explore the\nArchitectural Options;
 :6. Evaluate the Architecture\nwith the Stakeholders;

 if (architecture\naccepted?) then (yes)
   stop
 else (no)
   fork
     :7A. Rework the\nArchitecture;
   fork again
     :7B. Revisit the\nRequirements;
   end fork
   -> iterate back to step 4;
 endif

 @enduml

.. note::

 Las flechas curvas entre 7A y 7B indican que estos pasos no se
 realizan de forma aislada: hay una interacción intensa entre ellos
 porque revisar la arquitectura puede sugerir cambios en los
 requisitos y viceversa. Por ejemplo, simplificar el modelo de
 concurrencia puede requerir cambios en el orden en que el sistema
 realiza algunas tareas. Todos estos cambios deben revisarse y
 ratificarse con los stakeholders.

Tablas de detalle — pasos del proceso iterativo
-------------------------------------------------

.. list-table:: Tabla 7-6 — Paso 1: Consolidar los Inputs
 :header-rows: 0
 :widths: 20 80

 * - **Objetivo**
   - Comprender, validar y refinar los inputs disponibles para
     producir una línea base sólida antes de comenzar a diseñar.
 * - **Entradas**
   - Inputs brutos del proceso: scope y contexto del borrador de
     vista Context; concerns de los stakeholders.

     *En IACT:* hallazgos H-01..H-15 del WP de auditoría
     (`2026-05-04-08-32-37`); restricciones CNST-\*.
 * - **Actividades**
   - Tomar los inputs brutos, resolver inconsistencias entre ellos,
     responder preguntas abiertas y profundizar donde sea necesario
     para producir una línea base acordada por los stakeholders clave.

     *En IACT:* reconciliar conflictos entre concerns de
     AGR_ADMIN (RBAC restrictivo) y AGR_OPERADOR (acceso
     operacional amplio); validar que CNST-007 es compatible
     con los requisitos de disponibilidad del pipeline ETL.
 * - **Salidas**
   - Inputs consolidados con inconsistencias mayores resueltas,
     preguntas abiertas respondidas y áreas que requieren
     exploración adicional identificadas.

     *En IACT:* H-14 (uc-module-view/ vs use-case-view/) y H-15
     (misclasificación de process-view/) marcados como áreas
     de exploración prioritaria en Stage 5 STRATEGY.
 * - **Notas**
   - Es infrecuente recibir un set de inputs consistente y acordado.
     Este paso llena las lagunas, resuelve inconsistencias y obtiene
     acuerdo formal de los stakeholders clave antes de avanzar.

.. list-table:: Tabla 7-7 — Paso 2: Identificar Escenarios
 :header-rows: 0
 :widths: 20 80

 * - **Objetivo**
   - Identificar un conjunto de escenarios que ilustren los requisitos
     más importantes del sistema y permitan evaluar propuestas
     arquitectónicas.
 * - **Entradas**
   - Inputs consolidados (según el estado actual).
 * - **Actividades**
   - Producir escenarios que caractericen los atributos más
     importantes requeridos de la arquitectura y que puedan usarse
     para evaluar qué tan bien una arquitectura propuesta satisface
     los requisitos funcionales y de propiedades de calidad.

     *En IACT:* escenarios funcionales (UC-RBAC: asignación
     de permisos por AGR_ADMIN; UC-ETL: carga de datos IVR;
     UC-ACCION: registro de acción ciudadana) y escenarios
     de calidad (disponibilidad del pipeline ETL ante fallo
     de IVR; trazabilidad ante auditoría regulatoria).
 * - **Salidas**
   - Escenarios arquitectónicos priorizados para el sistema.

     *En IACT:* set de escenarios cubriendo RBAC granular,
     pipeline ETL, integración IVR read-only y auditoría.
 * - **Notas**
   - Un escenario describe una situación que el sistema
     probablemente enfrentará. Puede identificarse para comportamiento
     funcional ("¿Cómo registra IACT una acción ciudadana?") o
     propiedades de calidad ("¿Cómo mantiene IACT trazabilidad ante
     un fallo del pipeline ETL?").

.. list-table:: Tabla 7-8 — Paso 3: Identificar Estilos Arquitectónicos
 :header-rows: 0
 :widths: 20 80

 * - **Objetivo**
   - Identificar uno o más estilos arquitectónicos probados que
     puedan servir de base para la organización general del sistema.
 * - **Entradas**
   - Inputs consolidados; escenarios arquitectónicos.
 * - **Actividades**
   - Revisar catálogos de estilos arquitectónicos; considerar
     organizaciones que hayan funcionado bien en sistemas similares;
     identificar los relevantes para la arquitectura según se
     entiende actualmente.

     *En IACT:* sistemas con perfil OLTP + DSS + alta disponibilidad
     + regulatorio sugieren arquitectura en capas (separación
     RBAC/dominio/persistencia), orientada a eventos (pipeline ETL
     asíncrono), y puertos-y-adaptadores para aislar la fuente IVR
     read-only del núcleo de negocio.
 * - **Salidas**
   - Estilos arquitectónicos a considerar como base para las
     principales estructuras del sistema.

     *En IACT:* layered + event-driven + hexagonal (ports and
     adapters para IVR); ADR-GOB-* documentará la elección.
 * - **Notas**
   - Usar un estilo arquitectónico probado permite reutilizar
     conocimiento que ha demostrado efectividad en situaciones
     anteriores, reduciendo el riesgo de introducir ideas no
     probadas.

.. list-table:: Tabla 7-9 — Paso 4: Crear Vistas Arquitectónicas
 :header-rows: 0
 :widths: 20 80

 * - **Objetivo**
   - Crear una arquitectura de primera pasada que refleje los
     concerns arquitectónicos primarios y sirva como base para
     evaluación y refinamiento posteriores.
 * - **Entradas**
   - Inputs consolidados (según el estado actual); estilos
     arquitectónicos, viewpoints y perspectivas relevantes.
 * - **Actividades**
   - Producir un set inicial de vistas arquitectónicas para definir
     las ideas arquitectónicas iniciales, usando guía de los
     viewpoints y perspectivas y los estilos arquitectónicos
     relevantes.

     *En IACT:* generar borradores de las 6 vistas del modelo
     5+1 (Domain Model, Use Case View, Design View,
     Implementation View, Process View real, Deployment View)
     aplicando los viewpoints Rozanski: Functional, Information,
     Concurrency, Development, Deployment, Operational.
 * - **Salidas**
   - Borradores de vistas arquitectónicas.

     *En IACT:* primeros diagramas en `arquitectura-tecnica/`
     con los elementos principales de cada vista 5+1; posibles
     lagunas o inconsistencias son esperables en esta etapa.
 * - **Notas**
   - Aunque los borradores pueden contener lagunas,
     inconsistencias o errores, forman el punto de partida para
     el trabajo arquitectónico más detallado. No esperar perfección
     en esta etapa.

.. list-table:: Tabla 7-10 — Paso 5: Explorar las Opciones Arquitectónicas
 :header-rows: 0
 :widths: 20 80

 * - **Objetivo**
   - Explorar las distintas posibilidades arquitectónicas del sistema
     y tomar las decisiones arquitectónicas clave.
 * - **Entradas**
   - Inputs consolidados; borradores de vistas arquitectónicas;
     escenarios arquitectónicos, viewpoints y perspectivas.
 * - **Actividades**
   - Aplicar los escenarios a los borradores para demostrar que son
     factibles y no tienen problemas ocultos. Tomar las áreas de
     riesgo o incertidumbre y explorarlas. Donde haya más de una
     solución posible, evaluar fortalezas y debilidades de cada
     una y seleccionar la mejor.

     *En IACT:* aplicar el escenario UC-RBAC sobre el borrador
     de Use Case View para verificar que la granularidad de
     permisos es modelable; explorar H-14 (¿qué queda en
     use-case-view/ vs qué se migra de uc-module-view/?) y
     H-15 (¿qué diagramas de process-view/ corresponden a
     Use Case View vs cuáles al Concurrency viewpoint real?).
 * - **Salidas**
   - Vistas arquitectónicas más detalladas o precisas para las
     partes del sistema donde se exploraron opciones.

     *En IACT:* resolución documentada de H-14 y H-15 con
     decisión ADR-GOB-* sobre reclasificación de vistas.
 * - **Notas**
   - El objetivo de este paso es rellenar lagunas, eliminar
     inconsistencias y proporcionar el detalle necesario. La
     exploración puede implicar prototipos o spikes técnicos para
     las áreas de mayor incertidumbre.

.. list-table:: Tabla 7-11 — Paso 6: Evaluar la Arquitectura
 :header-rows: 0
 :widths: 20 80

 * - **Objetivo**
   - Evaluar la arquitectura con los stakeholders clave, capturar
     problemas o deficiencias y obtener su aceptación.
 * - **Entradas**
   - Inputs consolidados; vistas arquitectónicas y outputs de
     perspectivas.
 * - **Actividades**
   - Evaluar la arquitectura con una colección representativa de
     stakeholders. Capturar y acordar mejoras o comentarios sobre
     los modelos.

     *En IACT:* revisión con AGR_ADMIN (verificar modelado
     RBAC granular), AGR_AUDITOR (verificar trazabilidad
     regulatoria y cobertura CNST-007), representantes de
     instituciones (verificar integración IVR read-only).
 * - **Salidas**
   - Comentarios de la revisión arquitectónica — conformidades
     y no-conformidades por grupo de stakeholders.

     *En IACT:* lista de observaciones sobre las vistas 5+1
     con prioridad por grupo (bloqueante / importante / menor).
 * - **Notas**
   - El objetivo global es confirmar que los concerns de los
     stakeholders están cubiertos y que la arquitectura es de
     calidad. Puede requerirse trabajo para alcanzar consenso cuando
     los concerns de distintos grupos conflicten entre sí.

.. list-table:: Tabla 7-12 — Paso 7A: Revisar la Arquitectura
 :header-rows: 0
 :widths: 20 80

 * - **Objetivo**
   - Abordar los concerns surgidos durante la evaluación para producir
     una arquitectura que mejor cumpla sus objetivos.
 * - **Entradas**
   - Vistas arquitectónicas; comentarios de la revisión
     arquitectónica; estilos, viewpoints y perspectivas relevantes.
 * - **Actividades**
   - Tomar los resultados de la evaluación arquitectónica y
     abordarlos para producir una arquitectura mejorada. Este paso
     normalmente implica análisis funcional, uso de viewpoints y
     perspectivas, y prototipado.

     *En IACT:* incorporar feedback de AGR_AUDITOR sobre
     trazabilidad en la vista Process View real; actualizar
     la vista Deployment View para reflejar restricciones
     de red CNST-007; refinar el modelo RBAC en Design View.
 * - **Salidas**
   - Vistas arquitectónicas revisadas; áreas para investigación
     adicional (opcional).

     *En IACT:* vistas 5+1 actualizadas en `arquitectura-tecnica/`
     tras incorporar los comentarios de revisión.
 * - **Notas**
   - Este paso se realiza concurrente y colaborativamente con el 7B
     (Revisar Requisitos). Los dos pasos retroalimentan al Paso 5
     (Explorar opciones). Revisar la arquitectura puede sugerir
     cambios en los requisitos y viceversa.

.. list-table:: Tabla 7-13 — Paso 7B: Revisar los Requisitos
 :header-rows: 0
 :widths: 20 80

 * - **Objetivo**
   - Considerar los cambios en los requisitos originales que pueden
     ser necesarios a la luz de la evaluación arquitectónica.
 * - **Entradas**
   - Vistas arquitectónicas; comentarios de la revisión
     arquitectónica.
 * - **Actividades**
   - El trabajo realizado puede revelar requisitos inadecuados,
     inconsistentes o inviables de implementar. En ese caso,
     revisar los requisitos con los stakeholders y obtener su
     acuerdo sobre las revisiones necesarias.

     *En IACT:* si la vista Process View (concurrencia ETL)
     revela que ciertos requisitos de disponibilidad entran
     en conflicto con restricciones de la fuente IVR read-only,
     este paso reconcilia los BReqs afectados con las
     instituciones. Si H-15 muestra que los UC-flow actuales
     no son Process View real, actualizar `requisitos/` para
     reclasificarlos como comportamiento funcional.
 * - **Salidas**
   - Requisitos revisados (si los hay).

     *En IACT:* actualizaciones en `source/requisitos/casos-uso/`
     y `source/requisitos/business-requirements/` para reflejar
     las decisiones tomadas en la revisión arquitectónica.
 * - **Notas**
   - Este paso se realiza concurrente y colaborativamente con el 7A
     (Revisar Arquitectura). Los dos pasos retroalimentan al Paso 5
     (Explorar opciones). Los requisitos nunca son estáticos:
     la definición arquitectónica revela inconsistencias y lagunas
     que deben reconciliarse con los stakeholders.

----

Criterios de salida del proceso
=================================

En un mundo ideal, la definición de arquitectura continuaría hasta
que la arquitectura estuviera completa, correcta y completamente
documentada en la AD. Sin embargo, intentar fijar cada detalle antes
de que se haya escrito una línea de código puede ser bastante
contraproducente.

La clave para decidir cuándo se ha completado suficiente trabajo de
arquitectura es considerar los **riesgos** que afronta el proyecto.

.. admonition:: Principio

 La definición de arquitectura (o una iteración de ella) puede
 considerarse completa una vez que los riesgos materiales que afronta
 el sistema han sido mitigados, lo que puede juzgarse por la ausencia
 de comentarios o acciones significativas después de la evaluación de
 la arquitectura por parte de los stakeholders.

Una buena indicación de si se han abordado los riesgos es cuando no
hay comentarios, preguntas o concerns pendientes de la evaluación
arquitectónica. Esto significa que los stakeholders (incluyendo el
propio arquitecto) creen que el sistema propuesto satisfará sus
concerns y que los riesgos conocidos han sido mitigados.

.. admonition:: Estrategia

 Incluirse a uno mismo en los revisores de la descripción
 arquitectónica, y no finalizar la definición arquitectónica inicial
 hasta estar satisfecho de que no hay problemas significativos con la
 arquitectura.

.. admonition:: Estrategia

 Aspirar a producir una descripción arquitectónica que sea suficientemente
 buena para satisfacer las necesidades de sus usuarios, en lugar de
 aspirar a una versión perfecta que requiera significativamente más
 recursos sin proporcionar ningún beneficio real para los stakeholders.

En la práctica, en todos los proyectos salvo los más grandes, se debe
aspirar a completar la producción de la AD en **uno a tres meses**.

Una vez que la AD ha sido aprobada y colocada bajo control de
configuración, debe continuar siendo un **documento vivo**, mantenido
actualizado a lo largo de los pasos de construcción y hasta el
despliegue.

----

La definición arquitectónica en el ciclo de vida SDLC
=======================================================

La definición de arquitectura no reemplaza el ciclo de vida de
desarrollo de software normal, sino que debe considerarse una parte
integral de él.

Modelo en cascada (Waterfall)
-------------------------------

.. uml::
 :caption: Figura 7-4 — El Modelo en Cascada de Desarrollo

 @startuml uml14-waterfall-model

 skinparam ArrowColor #444444
 skinparam ActivityBorderColor #333333
 skinparam ActivityBackgroundColor #E8F4FD
 skinparam shadowing false

 :Requirements\nDefinition;
 :Architecture\nDefinition;
 :Design;
 :Build &\nUnit Test;
 :Integration &\nSystem Test;
 :Deployment;

 @enduml

En el modelo en cascada clásico, la definición de arquitectura es
una tarea separada temprana en el ciclo de vida (antes, después o
a veces junto a la definición de requisitos). La integración es
sencilla por la naturaleza lineal del proceso.

Enfoques iterativos
---------------------

.. uml::
 :caption: Figura 7-5 — Desarrollo Iterativo

 @startuml uml14-iterative-model

 skinparam ArrowColor #444444
 skinparam rectangleBorderColor #555555
 skinparam rectangleBackgroundColor #D5E8D4
 skinparam shadowing false

 rectangle "Iteration 1" {
   :Analyze → Arch → Design → Build → Test;
 }
 rectangle "Iteration 2" {
   :Analyze → Arch → Design → Build → Test;
 }
 rectangle "Iteration N" {
   :Analyze → Arch → Design → Build → Test;
 }

 @enduml

La motivación de los enfoques iterativos (como Feature Driven
Development o el Rational Unified Process) es reducir el riesgo
mediante la entrega temprana de funcionalidad parcial. La definición
de arquitectura formaría parte de la fase de análisis o podría
ejecutarse en paralelo. (Para el RUP en particular, el proceso
encaja bien en su fase de Elaboración).

Métodos ágiles
----------------

Los métodos ágiles son métodos ligeros que se enfocan en la entrega
rápida y continua de software a los usuarios finales. En proyectos
que usan metodologías ágiles, el arquitecto debe:

- **Entregar el trabajo arquitectónico incrementalmente.** Definir las
  estructuras arquitectónicas básicas en las etapas tempranas y
  refinarlas con un enfoque demand-based.
- **Trabajar colaborativamente** con el equipo para acordar un conjunto
  claro de principios de diseño y asegurar que se usan para garantizar
  consistencia en la implementación.
- **Definir los componentes claramente** con responsabilidades e
  interfaces documentadas para evitar confusión y retrabajo.
- **Compartir información ampliamente** usando herramientas simples
  (wikis, presentaciones) en lugar de sofisticadas herramientas de
  modelado.
- **Asegurarse de que cada entregable tiene un cliente** (¿sino por
  qué se hace?) y que los clientes entienden y están de acuerdo con
  el valor que aporta.
- **Crear documentos "suficientemente buenos"** que puedan entregarse
  tan pronto como sean utilizables, en lugar de esperar a que estén
  perfeccionados.
- **Crear ejemplos funcionales o prototipos** para probar ideas y
  guiar partes críticas o arriesgadas del trabajo de desarrollo.
- **Enfocarse en concerns transversales** (cross-cutting). La posición
  y experiencia del arquitecto le dan una posición única para
  identificar estos concerns y definir estrategias y soluciones
  a nivel de sistema. Se pueden usar perspectivas para esto.
- **Enfocarse en áreas de significado arquitectónico** y dejar el
  diseño más detallado a los desarrolladores.

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
