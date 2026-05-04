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
   - Definir claramente los límites del comportamiento y
     responsabilidades del sistema, y el contexto operacional y
     organizacional dentro del cual el sistema existe.
 * - **Entradas**
   - Necesidades y visión del adquirente; estrategia organizacional;
     arquitectura IT empresarial.
 * - **Salidas**
   - Declaraciones iniciales de los objetivos del sistema y qué está
     incluido y excluido de sus responsabilidades, junto con una
     definición inicial del contexto del sistema. Pueden capturarse
     en un borrador de la vista Context.
 * - **Notas**
   - Este paso es principalmente un proceso de comprender los
     objetivos estratégicos y organizacionales y cómo el sistema
     ayuda a cumplirlos, junto con un análisis para entender con
     qué otros sistemas necesita interactuar. El scope definido
     aquí puede cambiar (sujeto al acuerdo de los stakeholders)
     durante la definición de arquitectura.

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
   - Definición de cada grupo de stakeholders, con una o más personas
     nombradas y comprometidas que representarán al grupo.
 * - **Notas**
   - Este paso implica entender el contexto organizacional en el que
     se trabaja e identificar las personas clave que se verán
     afectadas por el sistema. Se comienza a conocer a sus
     representantes y a construir una relación de trabajo con ellos.
     Los concerns definidos aquí pueden cambiar durante la
     definición de arquitectura.

.. list-table:: Tabla 7-3 — Capturar los Concerns de Primera Pasada
 :header-rows: 0
 :widths: 20 80

 * - **Objetivo**
   - Comprender claramente los concerns que cada grupo de stakeholders
     tiene sobre el sistema y las prioridades que asignan a cada
     concern.
 * - **Entradas**
   - Lista de stakeholders; scope y contexto.
 * - **Salidas**
   - Definición inicial de un conjunto de concerns priorizados para
     cada grupo de stakeholders.
 * - **Notas**
   - Este paso suele comenzar con las reuniones iniciales con
     stakeholders. Normalmente implica una serie de presentaciones
     y reuniones con representantes de cada grupo que permiten
     explicar qué se pretende lograr y que los stakeholders
     expliquen sus intereses en el sistema. Los concerns pueden
     cambiar durante la definición de arquitectura.

.. list-table:: Tabla 7-4 — Definir la Arquitectura
 :header-rows: 0
 :widths: 20 80

 * - **Objetivo**
   - Crear la AD para el sistema.
 * - **Entradas**
   - Lista de stakeholders; scope y contexto.
 * - **Salidas**
   - AD; directrices y restricciones.
 * - **Notas**
   - Esta actividad se describe en detalle en la sección
     "Architecture Definition Activities" del capítulo original.
     Es la actividad central del proceso.

.. list-table:: Tabla 7-5 — Crear el Sistema Esqueleto (opcional)
 :header-rows: 0
 :widths: 20 80

 * - **Objetivo**
   - Paso opcional para crear una implementación funcional (aunque
     limitada) de la arquitectura que pueda evolucionar hacia el
     sistema entregado durante la fase de construcción del ciclo
     de vida.
 * - **Entradas**
   - AD; directrices y restricciones asociadas.
 * - **Salidas**
   - Un sistema funcional limitado que ilustra que el sistema puede
     abordar al menos uno de sus escenarios.
 * - **Notas**
   - Si se tiene el tiempo y los recursos, forma un puente efectivo
     entre la definición de arquitectura y la construcción de
     software. Permite al arquitecto y a los desarrolladores
     construir un sistema funcional que pueda ejecutar al menos un
     escenario funcional simple. El sistema esqueleto actúa como
     validación de la arquitectura (y una prueba de credibilidad
     importante para muchos stakeholders) así como un marco de
     trabajo para la fase de construcción de software.

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
   - Asegurar que se tienen todos los inputs necesarios para
     comenzar a definir la arquitectura y que estos son coherentes
     y completos en la medida de lo posible.
 * - **Entradas**
   - Concerns de los stakeholders; scope y contexto; cualquier
     restricción arquitectónica conocida; arquitecturas existentes.
 * - **Salidas**
   - Conjunto consolidado y priorizado de concerns, scope, contexto
     y restricciones, acordado entre los stakeholders.
 * - **Notas**
   - Es probable que los concerns sean incompletos e inconsistentes
     en esta etapa. El objetivo es identificar los concerns más
     importantes y asegurarse de que hay suficiente información para
     comenzar a definir la arquitectura.

.. list-table:: Tabla 7-7 — Paso 2: Identificar Escenarios
 :header-rows: 0
 :widths: 20 80

 * - **Objetivo**
   - Identificar un conjunto de escenarios que cubran los concerns
     más importantes y que puedan usarse para dirigir y evaluar el
     diseño de la arquitectura.
 * - **Entradas**
   - Concerns priorizados de los stakeholders; scope y contexto.
 * - **Salidas**
   - Conjunto de escenarios arquitectónicos priorizados que ilustran
     los aspectos más importantes del sistema propuesto.
 * - **Notas**
   - Los escenarios son casos de uso, escenarios de calidad u otras
     descripciones de las respuestas esperadas del sistema. Son una
     herramienta poderosa para asegurar que la arquitectura aborda
     los concerns de los stakeholders y para evaluar si lo hace.

.. list-table:: Tabla 7-8 — Paso 3: Identificar Estilos Arquitectónicos Relevantes
 :header-rows: 0
 :widths: 20 80

 * - **Objetivo**
   - Identificar los estilos arquitectónicos que son adecuados para
     el sistema en cuestión y que pueden usarse para guiar el diseño.
 * - **Entradas**
   - Concerns y escenarios priorizados; scope y contexto.
 * - **Salidas**
   - Uno o más estilos arquitectónicos candidatos que podrían aplicarse
     al sistema y criterios para evaluarlos.
 * - **Notas**
   - Un estilo arquitectónico es un patrón de alto nivel que define
     cómo organizar los elementos de un sistema. Ejemplos: cliente-
     servidor, arquitectura en capas, arquitectura orientada a
     servicios, arquitectura dirigida por eventos, microservicios.

.. list-table:: Tabla 7-9 — Paso 4: Producir una Arquitectura Candidata
 :header-rows: 0
 :widths: 20 80

 * - **Objetivo**
   - Crear una arquitectura candidata que aborde los concerns
     priorizados de los stakeholders.
 * - **Entradas**
   - Concerns y escenarios priorizados; estilos arquitectónicos
     candidatos; restricciones.
 * - **Salidas**
   - Versión preliminar de la AD: modelos de las vistas más
     importantes, con los elementos principales y sus relaciones.
 * - **Notas**
   - Es probable que la arquitectura candidata sea incompleta y
     requiera refinamiento. El objetivo es tener suficiente
     detalle para poder explorar opciones y evaluar con los
     stakeholders.

.. list-table:: Tabla 7-10 — Paso 5: Explorar las Opciones Arquitectónicas
 :header-rows: 0
 :widths: 20 80

 * - **Objetivo**
   - Identificar y evaluar las principales opciones arquitectónicas
     disponibles para los aspectos más importantes o inciertos del
     diseño.
 * - **Entradas**
   - Arquitectura candidata; concerns y escenarios priorizados.
 * - **Salidas**
   - Evaluación de las opciones disponibles y justificación de
     las decisiones tomadas.
 * - **Notas**
   - Es raro que exista una única solución a un problema. Cuando
     hay varias soluciones potenciales, el análisis debe revelar
     las fortalezas y debilidades de cada una y justificar la
     solución elegida. Puede implicar prototipos, spikes técnicos
     o análisis formales.

.. list-table:: Tabla 7-11 — Paso 6: Evaluar la Arquitectura con los Stakeholders
 :header-rows: 0
 :widths: 20 80

 * - **Objetivo**
   - Asegurar que la arquitectura candidata aborda los concerns de
     todos los stakeholders de manera satisfactoria.
 * - **Entradas**
   - Arquitectura candidata; concerns y escenarios priorizados.
 * - **Salidas**
   - Lista de comentarios, preguntas y concerns de los stakeholders
     sobre la arquitectura. Confirmación (o no) de que la arquitectura
     satisface los concerns de los stakeholders.
 * - **Notas**
   - Esta evaluación puede ser formal (p.ej. ATAM — Architecture
     Tradeoff Analysis Method) o informal. En cualquier caso, deben
     implicarse los stakeholders clave y deben tenerse en cuenta sus
     concerns antes de finalizar la arquitectura.

.. list-table:: Tabla 7-12 — Paso 7A: Revisar la Arquitectura
 :header-rows: 0
 :widths: 20 80

 * - **Objetivo**
   - Modificar la arquitectura candidata para abordar los comentarios
     y concerns surgidos de la evaluación con los stakeholders.
 * - **Entradas**
   - Arquitectura candidata; lista de comentarios y concerns de los
     stakeholders.
 * - **Salidas**
   - Arquitectura candidata revisada.
 * - **Notas**
   - Este paso y el 7B (revisar requisitos) están íntimamente
     relacionados. Revisar la arquitectura puede sugerir cambios
     en los requisitos y viceversa. Todos los cambios deben
     revisarse y ratificarse con los stakeholders.

.. list-table:: Tabla 7-13 — Paso 7B: Revisar los Requisitos
 :header-rows: 0
 :widths: 20 80

 * - **Objetivo**
   - Actualizar los requisitos y concerns para reflejar una
     comprensión más profunda del sistema resultante de la
     definición de arquitectura.
 * - **Entradas**
   - Requisitos y concerns actuales; cambios identificados en
     el paso 7A.
 * - **Salidas**
   - Requisitos y concerns actualizados, acordados con los
     stakeholders.
 * - **Notas**
   - Los requisitos nunca son estáticos. A medida que la
     arquitectura se define con más detalle, suelen surgir
     inconsistencias, ambigüedades o lagunas en los requisitos.
     Actualizar los requisitos en este punto mantiene la
     coherencia entre la AD y la especificación del sistema.

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
