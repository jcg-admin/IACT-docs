.. meta::
 :artefacto: UML_14_CONCERNS
 :tipo: Referencia — Concerns, Principios y Decisiones
 :dominio: base_cognitiva
 :subdominio: _uml
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uml-14-concerns:

=======================================================
Concerns, Principios y Decisiones Arquitectónicas
=======================================================

Fuente: Rozanski & Woods, *Software Systems Architecture* — Cap. 8.

La definición de arquitectura es con frecuencia un viaje de
descubrimiento. Al inicio de cualquier proyecto, los objetivos
generales suelen estar acordados pero el detalle permanece vago.
El rol del arquitecto incluye tomar ese detalle y hacerlo firme
y ratificado con los stakeholders.

----

Taxonomía de Concerns
=======================

Los concerns son las entradas que dan forma y definen la solución
arquitectónica. Se organizan en dos categorías fundamentales:

- **Concerns centrados en el problema** — influyen o restringen el
  problema que el sistema intenta resolver (responden al *por qué*
  y al *qué*).
- **Concerns centrados en la solución** — influyen o restringen las
  posibles soluciones a ese problema (responden al *cómo* y al
  *con qué*).

Dentro de cada categoría, los concerns pueden ser **influyentes**
(sugieren o impulsan decisiones en cierta dirección) o **restrictivos**
(imponen límites a las decisiones posibles).

.. uml::
 :caption: Figura 8-1 — Taxonomía de Concerns: Problema vs. Solución × Influencia vs. Restricción

 @startuml uml14-concerns-taxonomy

 skinparam rectangleBorderColor #555555
 skinparam rectangleBackgroundColor #F9F9F9
 skinparam shadowing false
 skinparam ArrowColor #555555
 skinparam noteBorderColor #888888
 skinparam noteBackgroundColor #FFFCE6

 rectangle "CENTRADOS EN EL PROBLEMA\n(Why / What)" as ProblemFocused {
   rectangle "Influyentes" as PI #E8F4FD {
     rectangle "Estrategia de negocio\nObjectivos y drivers\nAlcance y requisitos" as PI_items #DCEEFB
   }
   rectangle "Restrictivos" as PC #FFE8CC {
     rectangle "Estándares y políticas\nde negocio" as PC_items #FFDDB5
   }
 }

 rectangle "CENTRADOS EN LA SOLUCIÓN\n(How / With What)" as SolFocused {
   rectangle "Influyentes" as SI #D5E8D4 {
     rectangle "Estrategia IT\nObjectivos y drivers\ntecnológicos" as SI_items #C5DEC3
   }
   rectangle "Restrictivos" as SC #F8CECC {
     rectangle "Estándares y políticas\ntecnológicas\nRestricciones reales" as SC_items #F5BDB9
   }
 }

 PI -[hidden]right- SI
 PC -[hidden]right- SC

 @enduml

.. admonition:: Definición

 Un **concern** sobre una arquitectura es un requisito, un objetivo,
 una restricción, una intención o una aspiración que un stakeholder
 tiene para esa arquitectura.

La definición es deliberadamente amplia. Un concern puede ser
específico, inequívoco y medible (entonces lo llamamos "requisito"
y usamos técnicas de análisis clásico). Pero también puede ser vago
y formulado de modo impreciso y aun así ser más importante para los
stakeholders que los requisitos formales.

----

Concerns centrados en el problema
====================================

Estrategia de negocio
-----------------------

La estrategia de negocio define la dirección de la organización:
qué bienes o servicios provee, quiénes son sus clientes, cómo se
diferencia de competidores. También puede incluir un roadmap para
pasar del estado actual al estado objetivo.

Aunque es poco probable que el arquitecto la consulte directamente,
comprender sus principios es útil para entender los concerns de los
stakeholders de negocio y asegurar que las decisiones arquitectónicas
están alineadas con las prioridades organizacionales.

*En IACT:* la estrategia institucional es digitalizar el registro de
acciones ciudadanas con trazabilidad completa para cumplimiento
regulatorio, reemplazando registros en papel o sistemas legacy. Esta
estrategia impulsa directamente los requisitos de RBAC granular y
auditoría inmutable.

Objetivos y drivers de negocio
---------------------------------

Los objetivos y drivers definen el contexto de negocio del proyecto y
son la razón fundamental de su existencia.

.. admonition:: Definición

 Un **objetivo de negocio** (*business goal*) es un fin específico
 que persigue la organización. Un **driver de negocio** (*business
 driver*) es una fuerza que actúa sobre la organización y le exige
 comportarse de cierta manera para proteger y hacer crecer su negocio.

Estos suelen exhibir características que dificultan su traducción en
funcionalidades arquitectónicas: lenguaje impreciso, no cuantificables,
y con foco de negocio que oscurece las implicaciones técnicas.

Tácticas para trabajar con objetivos y drivers:

- **Convertirlos en requisitos** — por ejemplo, un objetivo de
  disponibilidad puede traducirse en requisitos de SLA medibles.
- **Gestionar expectativas** — cuando un objetivo es vago o
  inalcanzable, hacer visible a los stakeholders por qué es el caso.
- **Desarrollar principios arquitectónicos** que traduzcan el objetivo
  en características físicas y cualidades de la arquitectura.

*En IACT:* los drivers de negocio son la demanda de trazabilidad
regulatoria (AGR_AUDITOR), la operabilidad diaria para registro de
acciones (AGR_OPERADOR), y el control de acceso granular por institución
(AGR_ADMIN). Los hallazgos H-01..H-15 del WP de auditoría reflejan el
estado actual respecto a estos drivers.

Alcance y requisitos del sistema
-----------------------------------

El alcance del sistema define sus responsabilidades principales. Los
requisitos especifican con más detalle qué se requiere que haga el
sistema, desagregados en requisitos funcionales y propiedades de
calidad (quality properties).

El arquitecto rara vez está involucrado en la especificación detallada
de requisitos funcionales, pero debe estar al tanto de su evolución
para asegurar que el diseño los soporta. Las propiedades de calidad,
sin embargo, suelen requerir que el arquitecto las clarifique y defina,
ya que raramente hay consenso en etapas tempranas.

*En IACT:* el alcance se captura en `source/requisitos/` (BReqs, UCs,
FRs, RNFs). Las propiedades de calidad relevantes son disponibilidad
del pipeline ETL, tiempo de respuesta de consultas ciudadanas y
trazabilidad de auditoría (no degradable bajo carga).

Estándares y políticas de negocio
------------------------------------

Los estándares y políticas de negocio establecen aspectos de cómo la
organización opera. Pueden estar impulsados por regulación, por buenas
prácticas aceptadas, o por el ethos organizacional.

Incluso cuando el arquitecto no los consulta directamente, deben estar
en su radar ya que pueden restringir significativamente la arquitectura
(p.ej., una política de retención de datos se traduce en capacidades
de archivado y controles de seguridad).

*En IACT:* CNST-007 (restricciones de red y acceso) y los requisitos
de retención de datos para auditoría regulatoria son estándares de
negocio que acotan directamente las decisiones de despliegue y el
modelo de datos.

----

Concerns centrados en la solución
====================================

Estrategia IT
---------------

La estrategia IT define la dirección tecnológica a largo plazo de la
organización. Puede impulsar requisitos o restricciones tecnológicas
(p.ej., construir sistemas de forma débilmente acoplada y en múltiples
capas, o usar servicios centrales compartidos).

*En IACT:* la estrategia IT apunta a una arquitectura modular con
pipeline ETL desacoplado del core de registro ciudadano, permitiendo
actualizar la fuente IVR sin afectar la lógica de negocio.

Objetivos y drivers tecnológicos
-----------------------------------

Los objetivos tecnológicos son fines específicos del departamento IT,
mientras que los drivers tecnológicos son fuerzas que exigen comportarse
de cierta manera en el espacio de solución.

*En IACT:* objetivo tecnológico — el pipeline ETL debe procesar la
carga diaria del IVR en menos de N horas (SLA por definir). Driver
tecnológico — los datos del IVR son de solo lectura (el sistema no puede
modificarlos), lo que restringe la arquitectura de integración.

Estándares y políticas tecnológicas
--------------------------------------

Los estándares tecnológicos pueden tener foco técnico puro (protocolos
de red) o foco de negocio (sintaxis de mensajes de negocio). Adoptar
estándares simplifica el diseño y facilita la integración.

Se clasifican en:

- **Estándares abiertos** — definidos por ISO, IEEE, W3C. Aceptados
  broadly y aplican en múltiples entornos.
- **Estándares propietarios** — creados por organizaciones comerciales.
  Suelen aplicar solo a sus productos.
- **Estándares de facto** — no ratificados formalmente pero ampliamente
  seguidos.
- **Estándares organizacionales** — desarrollados para uso interno.
  Pueden prescribir proveedores o formas de usar infraestructura.

*En IACT:* **STD-011** (convención de aliases en diagramas PlantUML),
**ADR-GOB-002** (PlantUML como lenguaje de modelado), normativa de
vistas 5+1 y las restricciones en `normativa/restricciones/cnst-*.rst`
son estándares organizacionales que acotan las decisiones de modelado
y despliegue.

Restricciones del mundo real
-------------------------------

Más allá de requisitos y estándares, el arquitecto debe enfrentar
restricciones reales que a menudo no están escritas:

.. list-table::
 :header-rows: 1
 :widths: 22 78

 * - Tipo de restricción
   - Descripción e instancia en IACT
 * - **Técnicas**
   - Limitaciones de tecnología en funcionalidad, escalado o
     seguridad. *En IACT:* IVR como fuente de datos externa y de
     solo lectura — IACT no puede modificar registros IVR ni
     depender de su disponibilidad para transacciones ciudadanas.
 * - **Tiempo**
   - Plazos de entrega que limitan la complejidad de la solución.
     *En IACT:* los stages THYROX tienen exit criteria que deben
     cumplirse antes de avanzar al siguiente stage.
 * - **Costo**
   - Restricciones presupuestarias que acotan tecnologías y
     despliegue. *En IACT:* stack PostgreSQL + Node.js como
     elección de costo-beneficio frente a alternativas enterprise.
 * - **Habilidades**
   - Tecnologías nicho o enfoques inusuales pueden limitar la
     disponibilidad de personal. *En IACT:* el equipo conoce el
     stack definido; las vistas arquitectónicas deben ser
     comprensibles para desarrolladores sin background de
     arquitectura formal.
 * - **Operacionales**
   - Necesidad de operar en horarios específicos, cumplir
     estándares operacionales o encajar en ciclos existentes.
     *En IACT:* la carga ETL desde IVR tiene ventanas de
     mantenimiento que restringen cuándo puede ejecutarse.
 * - **Organizacionales**
   - Enfoques de desarrollo preferidos o razones "políticas" para
     ciertas elecciones. *En IACT:* la separación entre AGR_ADMIN
     y AGR_AUDITOR responde a una restricción organizacional de
     independencia entre quien opera y quien audita.

----

Relaciones entre Concerns, Requisitos y Arquitectura
=======================================================

.. uml::
 :caption: Figura 8-2 — Relaciones entre Concerns, Requisitos y Arquitectura

 @startuml uml14-concerns-relationships

 skinparam ArrowColor #444444
 skinparam rectangleBorderColor #555555
 skinparam rectangleBackgroundColor #F9F9F9
 skinparam shadowing false

 rectangle "Business\nStrategy" as BizStrat #E8F4FD
 rectangle "Business Goals\n& Drivers" as BizGoals #E8F4FD
 rectangle "IT Strategy" as ITStrat #D5E8D4
 rectangle "Tech Goals\n& Drivers" as TechGoals #D5E8D4
 rectangle "Requirements" as Reqs #FFF9C4
 rectangle "Architecture" as Arch #F8CECC

 BizStrat --> BizGoals : shapes
 BizGoals --> Reqs : drives
 ITStrat --> TechGoals : shapes
 TechGoals --> Arch : constrains
 Reqs --> Arch : informs

 Arch ..> Reqs : reveals\ninconsistencies
 Arch ..> BizGoals : may change\n(tech opportunities)

 note bottom of Arch
   Las líneas sólidas van del
   espacio problema → solución.
   Las punteadas van en sentido
   inverso (retroalimentación).
 end note

 @enduml

Los concerns centrados en la solución influyen o restringen la
arquitectura directamente. Los centrados en el problema lo hacen de
forma más indirecta, definiendo requisitos que sugieren arquitecturas
candidatas. Pero también hay flujo en dirección opuesta: la arquitectura
puede revelar requisitos inconsistentes y faltantes, retroalimentando
el análisis.

----

Qué hace un buen concern
===========================

Un concern bien expresado tiene estas características:

- **Cuantificable y medible** — evitar "el sistema debe responder
  rápido" o "la interfaz debe ser fácil de usar".
- **Verificable** — debe poder demostrarse objetivamente si se ha
  cumplido.
- **Trazable** — puede justificarse hacia atrás (hacia estrategia u
  objetivos) y hacia adelante (hacia decisiones arquitectónicas o de
  diseño).

*En IACT:*

.. list-table::
 :header-rows: 1
 :widths: 30 20 50

 * - Concern
   - Tipo
   - Formulación mejorable → mejorada
 * - RBAC granular
   - Problema / Restricción
   - "El acceso debe ser controlado" → "AGR_ADMIN puede asignar
     permisos a nivel de acción ciudadana; sin permiso explícito,
     el acceso es denegado por defecto."
 * - Trazabilidad de auditoría
   - Problema / Restricción
   - "Las acciones deben quedar registradas" → "Toda acción que
     modifique el estado de un registro ciudadano genera una
     entrada en audit_log con actor_id, timestamp, tipo de acción
     y estado anterior/posterior. La entrada es inmutable."
 * - Disponibilidad del ETL
   - Solución / Influencia
   - "El pipeline debe estar disponible" → "El pipeline ETL debe
     completar la carga diaria de IVR dentro de la ventana de
     mantenimiento nocturna (N horas); un fallo no debe corromper
     datos ya cargados."

----

Principios Arquitectónicos
============================

Un **principio arquitectónico** es una declaración fundamental de
creencia, enfoque o intención que guía la definición de una
arquitectura.

Los principios son útiles porque:

- Exponen los supuestos subyacentes de los stakeholders y los hacen
  explícitos.
- Proporcionan un marco de toma de decisiones cuando hay múltiples
  soluciones posibles.
- Permiten justificar decisiones arquitectónicas ante los stakeholders.
- Son útiles cuando la motivación o el alcance son poco claros, o
  cuando hay conflictos significativos entre stakeholders.

Qué hace un buen principio
-----------------------------

Un buen principio tiene estas características:

.. list-table::
 :header-rows: 1
 :widths: 22 78

 * - Característica
   - Descripción
 * - **Constructivo**
   - Ayuda a destacar issues, impulsar decisiones y establecer el
     marco arquitectónico correcto.
 * - **Razonado**
   - Está fuertemente motivado por drivers, objetivos y otros
     principios. Tiene una *rationale* explícita.
 * - **Bien articulado**
   - Puede ser comprendido por todos los stakeholders y no está
     abierto a malinterpretación.
 * - **Verificable**
   - Es posible determinar objetivamente si se está respetando.
 * - **Significativo**
   - No es una tautología. Test de significado: si la afirmación
     opuesta nunca podría tener sentido, el principio es trivial
     y tiene poco valor.

Principios arquitectónicos de IACT
-------------------------------------

Los siguientes principios se derivan de los concerns y drivers del
proyecto IACT:

.. list-table::
 :header-rows: 1
 :widths: 8 30 62

 * - ID
   - Principio
   - Rationale e implicaciones
 * - **P-01**
   - El IVR es fuente de datos de solo lectura; IACT nunca escribe
     ni modifica registros IVR.
   - *Rationale:* los datos IVR son propiedad de las instituciones
     y IACT no tiene autorización de escritura (driver organizacional
     y restricción técnica).
     *Implicaciones:* el adaptador de integración IVR es
     unidireccional; no se puede implementar retroescritura como
     fallback de ningún flujo.
 * - **P-02**
   - Toda acción que modifique el estado de un registro ciudadano
     genera una entrada de auditoría inmutable.
   - *Rationale:* requisito regulatorio de trazabilidad; concern de
     AGR_AUDITOR sobre conformidad con normativa.
     *Implicaciones:* el modelo de datos incluye tabla `audit_log`
     con constraints NOT NULL en actor_id, action_type y timestamp;
     ninguna operación de modificación puede omitir este registro.
 * - **P-03**
   - El acceso se deniega por defecto; AGR_ADMIN debe otorgar
     permisos explícitamente por acción ciudadana y por actor.
   - *Rationale:* principio de mínimo privilegio; concern de
     seguridad de las instituciones adquirentes.
     *Implicaciones:* no existen permisos implícitos ni herencia
     automática; el modelo RBAC es granular a nivel de acción.
 * - **P-04**
   - Un fallo en el pipeline ETL no debe corromper datos ya cargados
     ni bloquear la operación de registro ciudadano.
   - *Rationale:* driver de disponibilidad de AGR_OPERADOR; las
     operaciones de registro ciudadano son independientes de la
     sincronización con IVR.
     *Implicaciones:* el ETL opera en transacciones atómicas con
     rollback; el sistema core no tiene dependencia de disponibilidad
     del ETL para procesar acciones ciudadanas.
 * - **P-05**
   - La AD se describe mediante las 6 vistas del modelo 5+1 usando
     el framework de viewpoints de Rozanski & Woods.
   - *Rationale:* estándar organizacional (ADR-GOB-*); facilita
     la comunicación con stakeholders de distintos perfiles.
     *Implicaciones:* todo diagrama en `arquitectura-tecnica/`
     pertenece a una vista específica del modelo 5+1; los diagramas
     que no encajan deben ser reclasificados o eliminados.

----

Decisiones Arquitectónicas
============================

La arquitectura de un sistema es, en parte, el resultado acumulado de
las decisiones significativas tomadas en su definición. Tomar las
decisiones arquitectónicas correctas es vital porque son difíciles,
costosas y lentas de cambiar una vez que se ha construido una cantidad
significativa de software.

Decisiones explícitas vs. implícitas
---------------------------------------

Muchas decisiones arquitectónicas son **implícitas** — no se documentan
ni discuten. Esto ocurre porque la decisión parece "obvia", porque se
pierde en el detalle, o porque no hay tiempo para reflexionar sobre
ella. Las decisiones implícitas son más difíciles de gestionar porque
a menudo no se reconoce que se tomaron hasta que es demasiado tarde
para cambiarlas.

Hacer las decisiones arquitectónicas **explícitas** es una buena forma
de involucrar a stakeholders que de otro modo no participarían en la
definición arquitectónica.

Decisiones arquitectónicamente significativas
-----------------------------------------------

No tiene sentido documentar y revisar cada decisión. Se aplica el
criterio de **significancia arquitectónica** para determinar qué
decisiones necesitan revisión y ratificación de los stakeholders.

Las decisiones arquitectónicamente significativas responden a las
preguntas importantes sobre la arquitectura:

.. list-table::
 :header-rows: 1
 :widths: 15 35 50

 * - Tipo
   - Pregunta
   - Instancia en IACT
 * - **Qué** (*What*)
   - ¿Cuáles son los componentes funcionales, almacenes de datos,
     mecanismos de concurrencia, plataformas de despliegue?
   - Modelo 5+1 de vistas, tabla audit_log inmutable, pipeline ETL
     asíncrono, adaptador IVR unidireccional.
 * - **Cómo** (*How*)
   - ¿Cómo se construirán los elementos? ¿Qué patrones se usan?
   - Transacciones atómicas en ETL, mínimo privilegio en RBAC,
     arquitectura en capas con separación core/adaptadores.
 * - **Con qué** (*With What*)
   - ¿Qué tecnologías se usarán?
   - PostgreSQL para audit_log y datos ciudadanos, Node.js para
     API, PlantUML/Sphinx para la AD.

Criterios para identificar una decisión arquitectónicamente significativa:

- ¿Tiene impacto significativo en la funcionalidad del sistema o en
  sus propiedades de calidad?
- ¿Aborda un riesgo significativo del proyecto?
- ¿Tiene implicaciones en tiempo o costo?
- ¿Es la decisión o su rationale compleja o inesperada?
- ¿Se ha invertido un esfuerzo significativo en alcanzarla?
- ¿Es controvertida o políticamente importante?

----

Trazabilidad: Vinculando Concerns y Decisiones mediante Principios
===================================================================

El uso más poderoso de los principios es proporcionar **trazabilidad**
para las decisiones arquitectónicas: se puede usar los principios para
justificar y explicar características o elementos de la arquitectura.

La cadena de trazabilidad se construye así:

1. Empezar con los **drivers y objetivos de negocio**.
2. Usar los drivers para desarrollar **principios de negocio** (cuya
   rationale son los drivers).
3. Usar los principios de negocio para desarrollar **principios
   tecnológicos** (cuya rationale son los principios de negocio).
4. Usar los principios tecnológicos para llegar a **decisiones
   arquitectónicas** (cuya rationale son los principios tecnológicos).

.. uml::
 :caption: Figura 8-3 — Trazabilidad: de Drivers a Decisiones mediante Principios

 @startuml uml14-traceability-chain

 skinparam ArrowColor #444444
 skinparam rectangleBorderColor #555555
 skinparam shadowing false
 skinparam noteBackgroundColor #FFFCE6
 skinparam noteBorderColor #888888

 rectangle "Business\nDrivers / Goals" as BizGoals #E8F4FD
 rectangle "Business\nPrinciples" as BizPrinciples #D5E8D4
 rectangle "Technology\nPrinciples" as TechPrinciples #FFF9C4
 rectangle "Architectural\nDecisions" as ArchDecisions #F8CECC

 BizGoals --> BizPrinciples : implication →\nrationale
 BizPrinciples --> TechPrinciples : implication →\nrationale
 TechPrinciples --> ArchDecisions : implication →\nrationale

 note right of BizGoals
   Why: motivación organizacional
 end note
 note right of BizPrinciples
   What: principios de negocio
 end note
 note right of TechPrinciples
   How: principios tecnológicos
 end note
 note right of ArchDecisions
   With What: decisiones concretas
 end note

 @enduml

Ejemplo de trazabilidad en IACT
-----------------------------------

.. list-table::
 :header-rows: 1
 :widths: 10 15 75

 * - Nivel
   - ID
   - Enunciado
 * - Driver
   - G-01
   - Las instituciones necesitan registrar acciones ciudadanas con
     trazabilidad completa para cumplimiento regulatorio. Todo
     acceso y modificación debe ser atribuible a un actor con rol
     verificado.
 * - Principio de negocio
   - B-01
   - Toda modificación del estado de un registro ciudadano queda
     registrada con el actor, su rol en el momento de la acción,
     y el timestamp de la operación.
     *Rationale:* G-01.
 * - Principio tecnológico
   - T-01
   - El modelo de datos incluye una tabla de auditoría (`audit_log`)
     con registro inmutable. Ninguna operación de escritura en
     datos ciudadanos puede omitir la entrada de auditoría.
     *Rationale:* B-01.
 * - Decisión arquitectónica
   - D-01
   - `audit_log` en PostgreSQL con constraints `NOT NULL` en
     `actor_id`, `action_type`, `timestamp`, `record_before` y
     `record_after`. Las entradas no tienen operación `UPDATE` ni
     `DELETE` a nivel de aplicación.
     *Rationale:* T-01.

A partir de este ejemplo se puede justificar la decisión D-01 desde
el driver G-01, pasando por B-01 y T-01. Esta trazabilidad permite
a los stakeholders (especialmente AGR_AUDITOR) validar que las
decisiones técnicas satisfacen sus concerns regulatorios.

----

Aplicación al WP activo de auditoría
=======================================

El WP `2026-05-04-08-32-37-estructura-requisitos-arq-audit` está en
transición a Stage 5 STRATEGY. El marco de Concerns, Principios y
Decisiones de este capítulo provee la estructura para ese stage:

.. list-table::
 :header-rows: 1
 :widths: 30 70

 * - Artefacto STRATEGY
   - Contenido según Cap. 8
 * - **Concerns consolidados**
   - H-01..H-15 clasificados como problem-focused (hallazgos de
     estructura actual) y solution-focused (restricciones IVR,
     STD-011, viewpoints requeridos).
 * - **Principios P-01..P-05**
   - Base para las decisiones de reestructuración de
     `arquitectura-tecnica/`. Cada ADR-GOB-* debe referenciar
     el principio que lo fundamenta.
 * - **Decisiones pendientes (Stage 5)**
   - H-14: consolidar `uc-module-view/` en `use-case-view/` →
     decisión tipo *What*.

     H-15: reclasificar diagramas de `process-view/` →
     decisión tipo *What* (viewpoint Concurrency real).

     Operational viewpoint ausente → decisión tipo *What* sobre
     si crear vista o cubrir con perspectivas.

----

Referencias cruzadas
=====================

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **Viewpoints y Concerns (Cap. 3)**
   - :doc:`vistas-y-viewpoints`
 * - **Perspectivas como cross-cutting (Cap. 4)**
   - :doc:`perspectivas-arquitectonicas`
 * - **Proceso de definición (Cap. 7)**
   - :doc:`proceso-definicion-arquitectonica`
 * - **El Arquitecto (Cap. 5)**
   - :doc:`arquitecto-y-proceso`
 * - **WP de auditoría activo**
   - `.thyrox/context/work/2026-05-04-08-32-37-estructura-requisitos-arq-audit/`
 * - **Restricciones IACT**
   - :doc:`/normativa/restricciones/index`
