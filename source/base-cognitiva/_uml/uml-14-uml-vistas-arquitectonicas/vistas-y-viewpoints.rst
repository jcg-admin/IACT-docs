.. meta::
 :artefacto: UML_14_VISTAS
 :tipo: Referencia — Fundamentos Arquitectonicos
 :dominio: base_cognitiva
 :subdominio: _uml
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uml-14-vistas:

=======================================================
Vistas y Viewpoints — Fundamentos
=======================================================

Fuente: Rozanski & Woods, *Software Systems Architecture* — Cap. 3.

Al comenzar el diseño de la arquitectura de un sistema, se
presentan preguntas difíciles:

- ¿Cuáles son los principales elementos funcionales?
- ¿Cómo interactúan entre sí y con el exterior?
- ¿Qué información se gestionará, almacenará y presentará?
- ¿Qué elementos físicos de hardware y software serán necesarios?
- ¿Qué características y capacidades operacionales se ofrecerán?
- ¿Qué entornos de desarrollo, prueba, soporte y formación
  se proporcionarán?

----

El problema del modelo único
==============================

Una tentación común — que debe evitarse — es intentar responder
todas estas preguntas mediante un único modelo que lo abarque
todo. Este tipo de modelo usa habitualmente una mezcla de
notaciones formales e informales para describir múltiples
aspectos del sistema en una sola hoja: estructura funcional,
capas de software, concurrencia, comunicación entre componentes,
entorno de despliegue físico, etc.

.. important::

 **Principio:** No es posible capturar las características
 funcionales y las propiedades de calidad de un sistema complejo
 en un único modelo comprensible que sea entendible y de valor
 para sus stakeholders.

Un modelo único monolítico es el peor de todos los escenarios:

- Es difícil de entender
- Rara vez identifica claramente las características más
  importantes de la arquitectura
- Sirve mal a los stakeholders individuales porque les cuesta
  encontrar los aspectos que les interesan
- Por su complejidad, suele estar incompleto, ser incorrecto o
  estar desactualizado

**Ejemplo — Sistema de reservas de vuelos:**

Aunque conceptualmente simple, en la práctica tiene aspectos
muy complejos: datos distribuidos en múltiples sistemas y
ubicaciones físicas, distintos tipos de dispositivos de entrada,
requisitos multiidioma, soporte para múltiples impresoras,
abundante regulación internacional.

El arquitecto dibuja una primera versión que intenta representar
todos los aspectos importantes en un único diagrama: dispositivos
de entrada, sistemas físicos con datos replicados, dispositivos
de impresión, anotaciones de texto para multiidioma y auditoría
regulatoria. Los detalles de red se abstraen en un icono porque
son demasiado complejos — aunque la red es probablemente el
aspecto más complicado de la arquitectura.

Resultado: ningún stakeholder puede usarlo. Los usuarios lo
encuentran demasiado complejo (demasiados componentes hardware).
Los stakeholders técnicos lo descartan por lo que falta (topología
de red). El equipo legal no puede verificar el cumplimiento
regulatorio. El patrocinador lo encuentra incomprensible. El
arquitecto pasa tiempo excesivo manteniéndolo actualizado. Pronto
queda obsoleto y se olvida — pero los problemas que no aborda
no desaparecen y causan problemas durante la implementación.

.. admonition:: Estrategia

 Un sistema complejo se describe de forma mucho más eficaz
 mediante un conjunto de vistas interrelacionadas que
 colectivamente ilustran sus características funcionales y
 propiedades de calidad y demuestran que cumple sus objetivos,
 que mediante un único modelo sobrecargado.

----

Vistas arquitectónicas
========================

Una vista arquitectónica es una forma de representar aquellos
aspectos o elementos de la arquitectura que son relevantes para
las preocupaciones (*concerns*) que la vista pretende abordar
— y, por implicación, para los stakeholders a quienes esas
preocupaciones son importantes.

Esta idea no es nueva: se remonta al trabajo de David Parnas en
los años 70 y más recientemente a Dewayne Perry y Alexander Wolf
a principios de los 90. Sin embargo, no fue hasta 1995 cuando
Philippe Kruchten publicó su descripción de las vistas:
*Architectural Blueprints — The "4+1" View Model of Software
Architecture*, que propone cuatro vistas distintas y el uso
de escenarios (casos de uso) para elucidar el comportamiento.

La norma IEEE Std 1471 (predecesora de ISO Std 42010) formalizó
estos conceptos en 2000.

.. admonition:: Definición

 Una **vista** es una representación de uno o más aspectos
 estructurales de una arquitectura que ilustra cómo esta
 aborda una o más preocupaciones (*concerns*) sostenidas por
 uno o más de sus stakeholders.

Al decidir qué incluir en una vista, considerar:

.. list-table::
 :header-rows: 1
 :widths: 25 75

 * - Dimensión
   - Pregunta a responder
 * - **Scope de la vista**
   - ¿Qué aspectos estructurales de la arquitectura se están
     representando? ¿Elementos runtime y su intercomunicación,
     o el entorno de runtime y cómo se despliega? ¿Elementos
     dinámicos o estáticos?
 * - **Tipos de elemento**
   - ¿Qué tipos de elemento arquitectónico se están
     categorizando? (máquinas servidor individuales vs.
     entorno de servicio)
 * - **Audiencia**
   - ¿A qué clase(s) de stakeholder va dirigida la vista?
     ¿Enfocada en uno o en un grupo amplio con intereses
     y experiencia variable?
 * - **Expertise de la audiencia**
   - ¿Cuánto conocimiento técnico tienen los stakeholders?
     (adquirentes y usuarios vs. desarrolladores o soporte)
 * - **Scope de concerns**
   - ¿Qué preocupaciones de stakeholders pretende abordar
     la vista? ¿Cuánto conocen del contexto arquitectónico?
 * - **Nivel de detalle**
   - ¿Cuánto necesitan saber estos stakeholders sobre este
     aspecto de la arquitectura?

.. admonition:: Estrategia

 Solo incluir en una vista la información que hace avanzar
 los objetivos de la descripción arquitectónica: información
 que ayuda a explicar la arquitectura a los stakeholders o
 demuestra que los objetivos del sistema se están cumpliendo.

----

Viewpoints
===========

Un viewpoint es el mecanismo que evita tener que partir de cero
cada vez que se crea una vista. Kruchten definió cuatro vistas
estándar: Logical, Process, Physical y Development. La norma IEEE
generalizó esta idea proponiendo el concepto de viewpoint.

.. admonition:: Definición

 Un **viewpoint** es una colección de patrones, plantillas y
 convenciones para construir un tipo de vista. Define los
 stakeholders cuyas preocupaciones se reflejan en el viewpoint
 y las directrices, principios y modelos de plantilla para
 construir sus vistas.

La relación entre viewpoints y vistas es análoga a la relación
entre clases y objetos en desarrollo orientado a objetos:

- Una definición de clase provee una plantilla para la
  construcción de un objeto.
- Un viewpoint provee una plantilla para la construcción de
  una vista.

Los viewpoints son una forma importante de aportar estructura y
consistencia a lo que anteriormente era una actividad bastante
desestructurada. Al definir un enfoque estándar, un lenguaje
estándar e incluso un metamodelo estándar para describir
diferentes aspectos de un sistema, los stakeholders pueden
entender cualquier descripción arquitectónica que se ajuste a
esos estándares una vez que los conocen.

.. admonition:: Estrategia

 Al desarrollar una vista, ya sea usando o no un viewpoint
 formalmente definido, tener claro qué tipos de concerns está
 abordando la vista, qué tipos de elementos arquitectónicos
 presenta y a quién va dirigido el viewpoint. Asegurarse de
 que los stakeholders también lo entiendan.

----

Relaciones entre los conceptos clave
======================================

.. uml::
 :caption: Figura 3-1 — Vistas y Viewpoints en contexto

 @startuml uml14-rozanski-modelo-conceptual

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

 @enduml

Relaciones añadidas al modelo conceptual base:

- Un **viewpoint** define los objetivos, la audiencia y el
  contenido de una clase de vistas, y define los *concerns*
  que abordarán las vistas de esa clase.
- Una **vista** se ajusta a (*conforms to*) un viewpoint y
  comunica la resolución de varios *concerns* (y la resolución
  de un *concern* puede comunicarse en varias vistas).
- Una **descripción arquitectónica (AD)** comprende varias
  vistas.

----

Beneficios de usar viewpoints y vistas
========================================

.. list-table::
 :header-rows: 1
 :widths: 28 72

 * - Beneficio
   - Descripción
 * - **Separación de concerns**
   - Describir muchos aspectos del sistema mediante una sola
     representación puede oscurecer la comunicación y hacer
     que aspectos independientes queden entrelazados en el
     modelo. Separar las descripciones permite enfocarse en
     cada aspecto por separado.
 * - **Comunicación con grupos de stakeholders**
   - Los concerns de cada grupo son típicamente muy diferentes
     (usuarios finales, auditores de seguridad, staff de
     helpdesk). El enfoque orientado a viewpoints facilita
     dirigir rápidamente a cada grupo a la parte del AD
     relevante para sus concerns, usando lenguaje y notación
     apropiados a su conocimiento y experiencia.
 * - **Gestión de la complejidad**
   - Tratar simultáneamente todos los aspectos de un sistema
     grande genera una complejidad abrumadora. Tratando cada
     aspecto significativo por separado, el arquitecto puede
     enfocarse en cada uno por turno y ayudar a vencer la
     complejidad resultante de su combinación.
 * - **Mejora del foco del desarrollador**
   - Separando en vistas distintas los aspectos del sistema
     más importantes para el equipo de desarrollo, se ayuda
     a garantizar que se construye el sistema correcto.

----

Riesgos y pitfalls
====================

.. list-table::
 :header-rows: 1
 :widths: 25 75

 * - Riesgo
   - Descripción y mitigación
 * - **Inconsistencia**
   - Usar varias vistas genera inevitablemente problemas de
     consistencia entre ellas. No existen lenguajes de
     descripción arquitectónica verificables automáticamente
     de uso generalizado. Alcanzar consistencia cross-view
     es un proceso inherentemente manual.
 * - **Selección incorrecta de vistas**
   - No siempre es obvio qué conjunto de vistas es adecuado.
     Depende de la naturaleza y complejidad de la arquitectura,
     las habilidades de los stakeholders, el tiempo disponible
     y otros factores. La experiencia del arquitecto y el
     análisis de los concerns más importantes son la mejor
     guía.
 * - **Fragmentación**
   - Tener varias vistas puede dificultar la comprensión del
     AD. Cada vista implica un esfuerzo significativo de
     creación y mantenimiento. Eliminar vistas que no aborden
     concerns significativos. En algunos casos considerar
     vistas híbridas, aunque con cuidado de que no se vuelvan
     difíciles de entender por abordar demasiados concerns
     combinados.

----

Catálogo de viewpoints (Rozanski & Woods)
==========================================

La Parte III del libro presenta el catálogo de siete viewpoints
core para arquitecturas de sistemas de información: Context,
Functional, Information, Concurrency, Development, Deployment y
Operational. Aunque los viewpoints son en gran medida disjuntos,
es conveniente agruparlos como se muestra en Figura 3-2.

.. list-table:: Tabla 3-1 — Catálogo de viewpoints (Rozanski & Woods)
 :header-rows: 1
 :widths: 18 82

 * - Viewpoint
   - Definición
 * - **Context**
   - Describe las relaciones, dependencias e interacciones entre
     el sistema y su entorno: las personas, sistemas y entidades
     externas con las que interactúa. La vista Context será de
     interés para muchos stakeholders y juega un papel importante
     en ayudarles a entender las responsabilidades del sistema y
     cómo se relaciona con su organización.
 * - **Functional**
   - Describe los elementos funcionales *runtime* del sistema,
     sus responsabilidades, interfaces e interacciones primarias.
     Una vista Functional es la piedra angular de la mayoría de
     las ADs y suele ser la primera que los stakeholders leen.
     Impulsa la forma de otras estructuras del sistema (información,
     concurrencia, despliegue) y tiene un impacto significativo
     en propiedades de calidad como la capacidad de cambio, la
     seguridad y el rendimiento en tiempo de ejecución.
 * - **Information**
   - Describe cómo el sistema almacena, manipula, gestiona y
     distribuye información. El objetivo de casi cualquier sistema
     informático es manipular información de alguna forma, y este
     viewpoint desarrolla una vista completa pero de alto nivel de
     la estructura estática de los datos y el flujo de información.
     El objetivo del análisis es responder las grandes preguntas
     sobre contenido, estructura, propiedad, latencia, referencias
     y migración de datos.
 * - **Concurrency**
   - Describe la estructura de concurrencia del sistema y mapea
     los elementos funcionales a unidades de concurrencia para
     identificar claramente qué partes del sistema pueden ejecutarse
     concurrentemente y cómo se coordina y controla esto. Conlleva
     la creación de modelos que muestren las estructuras de proceso
     e hilo que el sistema usará y los mecanismos de comunicación
     entre procesos para coordinar su operación.
 * - **Development**
   - Describe la arquitectura que soporta el proceso de desarrollo
     de software. Las vistas Development comunican los aspectos de
     la arquitectura de interés para los stakeholders involucrados
     en construir, probar, mantener y mejorar el sistema.
 * - **Deployment**
   - Describe el entorno en el que el sistema se desplegará y las
     dependencias que el sistema tiene sobre él. Esta vista captura
     el entorno hardware que el sistema necesita (nodos de
     procesamiento, interconexiones de red e instalaciones de
     almacenamiento), los requisitos del entorno técnico para cada
     elemento y el mapeo de los elementos software al entorno de
     ejecución que los ejecutará.
 * - **Operational**
   - Describe cómo el sistema será operado, administrado y soportado
     cuando esté en ejecución en su entorno de producción. Para
     todos los sistemas salvo los más simples, instalar, gestionar
     y operar el sistema es una tarea significativa que debe
     considerarse y planificarse en tiempo de diseño. El objetivo
     es identificar estrategias a nivel de sistema para abordar los
     concerns operacionales de los stakeholders e identificar
     soluciones que los aborden.

Agrupación de viewpoints
--------------------------

.. uml::
 :caption: Figura 3-2 — Agrupación de viewpoints

 @startuml uml14-rozanski-viewpoints-agrupacion

 skinparam rectangleBorderColor #555555
 skinparam rectangleBackgroundColor #F9F9F9
 skinparam rectangleFontSize 13
 skinparam ArrowColor #555555
 skinparam shadowing false

 rectangle "Context\n(overarching)" as ContextVP #E8F4FD

 rectangle "Organización fundamental" {
   rectangle "Functional" as FunctionalVP #D5E8D4
   rectangle "Information" as InformationVP #D5E8D4
   rectangle "Concurrency" as ConcurrencyVP #D5E8D4
 }

 rectangle "Construcción" {
   rectangle "Development" as DevelopmentVP #FFF2CC
 }

 rectangle "Entorno de producción" {
   rectangle "Deployment" as DeploymentVP #FFE6CC
   rectangle "Operational" as OperationalVP #FFE6CC
 }

 ContextVP -[hidden]-> FunctionalVP
 FunctionalVP -[hidden]-> DevelopmentVP
 DevelopmentVP -[hidden]-> DeploymentVP

 @enduml

- **Context** está en la cima: informa el scope y contenido
  de todos los demás viewpoints.
- **Functional, Information, Concurrency** definen juntos cómo
  el sistema provee su funcionalidad.
- **Development** define estándares y modelos para la
  construcción de los elementos funcionales, de información y
  de concurrencia.
- **Deployment y Operational** definen el entorno de producción
  del sistema.

.. note::

 El catálogo de Rozanski & Woods tiene **7 viewpoints**
 (incluyendo Context). El estudio empírico referenciado en
 :doc:`contexto-empirico` usó **6** (excluyendo Context),
 que son los presentes en la :doc:`framework-rozanski`.

----

Selección de viewpoints
========================

No todos los viewpoints aplican a toda arquitectura, y algunos
serán más importantes que otros. La selección adecuada depende de:

- La naturaleza y complejidad de la arquitectura
- Las habilidades y experiencia de los stakeholders (y del
  arquitecto)
- El tiempo disponible y otras restricciones

Aunque es difícil generalizar, la siguiente tabla lista la
importancia relativa que cada vista tiene para algunos tipos
típicos de sistemas de información. Se recomienda usar esta tabla
como punto de partida al elegir las vistas a incluir en la AD:

.. list-table:: Tabla 3-2 — Vistas más importantes para tipos típicos de sistema
 :header-rows: 2
 :stub-columns: 1
 :widths: 18 14 14 14 14 14 12

 * - Tipo de sistema
   - OLTP\ [#t1]_
   - Cálculo/MW\ [#t2]_
   - DSS/MIS\ [#t3]_
   - Web vol. alto\ [#t4]_
   - Pkg. empresa\ [#t5]_
   -
 * - Viewpoint
   -
   -
   -
   -
   -
   -
 * - **Context**
   - Alta
   - Baja
   - Alta
   - Media
   - Media
   -
 * - **Functional**
   - Alta
   - Alta
   - Baja
   - Alta
   - Alta
   -
 * - **Information**
   - Media
   - Baja
   - Alta
   - Media
   - Media
   -
 * - **Concurrency**
   - Baja
   - Alta
   - Baja
   - Media
   - Variable
   -
 * - **Development**
   - Alta
   - Alta
   - Baja
   - Alta
   - Alta
   -
 * - **Deployment**
   - Alta
   - Alta
   - Alta
   - Alta
   - Alta
   -
 * - **Operational**
   - Variable
   - Baja
   - Media
   - Media
   - Alta
   -

.. rubric:: Notas de tabla

.. [#t1] OLTP: Sistema de información transaccional en línea
.. [#t2] Cálculo/MW: Servicio de cálculo o middleware
.. [#t3] DSS/MIS: Sistema de soporte de decisiones / información gerencial
.. [#t4] Web vol. alto: Sitio web de alto volumen de usuarios
.. [#t5] Pkg. empresa: Paquete de software empresarial (ERP, etc.)

La selección correcta de vistas para un contexto específico
requiere experiencia y análisis de los concerns más importantes
que afectan a la arquitectura concreta. Ver análisis IACT en
:doc:`contexto-empirico`.

----

Resumen
========

Capturar la esencia y el detalle de toda la arquitectura en un
único modelo no es posible para ningún sistema que no sea
trivial. El intento produce un monstruo de modelo que es
inmanejable y no representa adecuadamente el sistema para
ningún stakeholder.

La mejor forma de gestionar esta complejidad es producir
diferentes representaciones de toda o parte de la arquitectura,
cada una enfocada en ciertos aspectos del sistema y mostrando
cómo aborda algunos de los concerns de los stakeholders.
Estas representaciones son las **vistas**.

Para decidir qué vistas producir y qué debe incluir cada una,
se usan los **viewpoints**: definiciones estandarizadas de
conceptos, contenido y actividades de una clase de vista.

El uso de vistas y viewpoints aporta beneficios importantes
(separación de concerns, comunicación con stakeholders, gestión
de la complejidad), pero tiene pitfalls que deben gestionarse
(inconsistencia, selección incorrecta, fragmentación).

----

Referencias cruzadas
=====================

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **Contexto empírico del estudio**
   - :doc:`contexto-empirico`
 * - **Meta-modelo (Figura 1)**
   - :doc:`metamodelo-descripcion`
 * - **Framework Rozanski — Tabla 1**
   - :doc:`framework-rozanski`
 * - **Comparación de frameworks — Tabla 2**
   - :doc:`frameworks-comparacion`
 * - **Vistas arquitectónicas IACT**
   - :doc:`/arquitectura-tecnica/vistas-kruchten`
