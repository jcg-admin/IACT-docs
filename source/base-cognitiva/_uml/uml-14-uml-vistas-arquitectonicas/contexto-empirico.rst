.. meta::
 :artefacto: UML_14_CONTEXTO
 :tipo: Referencia — Investigacion Empirica
 :dominio: base_cognitiva
 :subdominio: _uml
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uml-14-contexto:

=======================================================
Contexto empírico: UML y viewpoints arquitectónicos
=======================================================

Motivación del estudio
=======================

Dado el enorme soporte comunitario de UML (incluyendo fabricantes
de herramientas y desarrolladores del lenguaje) y su popularidad
entre los practitioners, cabría esperar entender en qué medida
los practitioners usan UML y sus distintos tipos de diagramas
para modelar arquitecturas de software desde diferentes viewpoints.

Sin embargo, los estudios empíricos existentes sobre UML no
ayudan a comprender la perspectiva de los practitioners sobre el
uso de UML para distintos viewpoints arquitectónicos. Si bien la
literatura existente permite conocer muchos aspectos prácticos de
UML — motivación/desmotivación de practitioners, evaluación de
UML para algunas propiedades de calidad, tasa de uso de UML para
aspectos particulares del desarrollo de software — no es fácil
entender en qué medida los practitioners usan UML para los
diversos viewpoints arquitectónicos que cada uno aborda un
conjunto diferente de preocupaciones (*concerns*) del desarrollo
de software.

Brecha de conocimiento
=======================

En la literatura actual no está claro:

- Qué viewpoints se modelan con UML en la práctica
- Los *concerns* específicos abordados con UML en cada viewpoint
- La elección de los diagramas UML por parte de los practitioners
  para cada *concern*
- Las elecciones de los practitioners respecto a herramientas de
  modelado UML

El framework de Rozanski et al.
=================================

Para determinar el conjunto de viewpoints, se considera el enfoque
de Rozanski et al. para el framework de viewpoints arquitectónicos,
que se enfoca en las necesidades de los practitioners que trabajan
con cualquier tipo de sistema de información y al mismo tiempo
soporta los conceptos de viewpoint, view y model type que
encajan bien con la definición del meta-modelo.

El objetivo de la investigación es encuestar a los practitioners
para entender en qué medida usan UML para describir arquitecturas
de software desde los diferentes viewpoints que Rozanski et al.
ofrecen en su framework.

Los siete viewpoints de Rozanski et al.
========================================

El catálogo completo incluye el viewpoint **Context** (transversal)
más seis viewpoints especializados. Las definiciones a continuación
son las del libro original (*Software Systems Architecture*, Rozanski
& Woods, 2ª ed.).

.. list-table::
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
     las ADs y suele ser la primera parte que los stakeholders
     leen. Impulsa la forma de otras estructuras del sistema
     (información, concurrencia, despliegue) y tiene un impacto
     significativo en propiedades de calidad como la capacidad
     de cambio, la seguridad y el rendimiento en tiempo de
     ejecución.
 * - **Information**
   - Describe cómo el sistema almacena, manipula, gestiona y
     distribuye información. El objetivo último de casi cualquier
     sistema informático es manipular información de alguna forma,
     y este viewpoint desarrolla una vista completa pero de alto
     nivel de la estructura estática de los datos y el flujo de
     información. El objetivo del análisis es responder las
     grandes preguntas sobre contenido, estructura, propiedad,
     latencia, referencias y migración de datos.
 * - **Concurrency**
   - Describe la estructura de concurrencia del sistema y mapea
     los elementos funcionales a unidades de concurrencia para
     identificar claramente qué partes del sistema pueden
     ejecutarse concurrentemente y cómo se coordina y controla
     esto. Conlleva la creación de modelos que muestren las
     estructuras de proceso e hilo que el sistema usará y los
     mecanismos de comunicación entre procesos para coordinar
     su operación.
 * - **Development**
   - Describe la arquitectura que soporta el proceso de
     desarrollo de software. Las vistas Development comunican
     los aspectos de la arquitectura de interés para los
     stakeholders involucrados en construir, probar, mantener
     y mejorar el sistema.
 * - **Deployment**
   - Describe el entorno en el que el sistema se desplegará y
     las dependencias que el sistema tiene sobre él. Esta vista
     captura el entorno hardware que el sistema necesita
     (principalmente nodos de procesamiento, interconexiones de
     red e instalaciones de almacenamiento en disco requeridas),
     los requisitos del entorno técnico para cada elemento y el
     mapeo de los elementos software al entorno de ejecución que
     los ejecutará.
 * - **Operational**
   - Describe cómo el sistema será operado, administrado y
     soportado cuando esté en ejecución en su entorno de
     producción. Para todos los sistemas salvo los más simples,
     instalar, gestionar y operar el sistema es una tarea
     significativa que debe considerarse y planificarse en
     tiempo de diseño. El objetivo del viewpoint Operational es
     identificar estrategias a nivel de sistema para abordar
     los concerns operacionales de los stakeholders e
     identificar soluciones que los aborden.

.. note::

 El viewpoint **Operational** es crítico desde el punto de vista
 de esfuerzo: los problemas operacionales deben resolverse
 temprano para minimizar el esfuerzo requerido, ya que este
 puede crecer significativamente si se abordan cuando el sistema
 ya está en producción. Este viewpoint **no tiene equivalente**
 en Kruchten 4+1, Soni, Clements ni Garland — es una
 contribución original de Rozanski & Woods.

----

Importancia de los viewpoints por tipo de sistema
===================================================

No todos los viewpoints tienen la misma relevancia para cada tipo
de sistema de información. La siguiente tabla resume la importancia
relativa de cada viewpoint para cinco tipos de sistema
representativos (Rozanski & Woods, Cap. 3):

.. list-table:: Importancia de viewpoints por tipo de sistema
 :header-rows: 2
 :stub-columns: 1
 :widths: 18 14 14 14 14 14 12

 * - Tipo de sistema
   - OLTP\ [#f1]_
   - Cálculo/MW\ [#f2]_
   - DSS/MIS\ [#f3]_
   - Web vol.\ alto\ [#f4]_
   - Pkg. Empresa\ [#f5]_
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

.. rubric:: Notas

.. [#f1] OLTP: Sistema de información transaccional en línea
.. [#f2] Cálculo/MW: Servicio de cálculo o middleware
.. [#f3] DSS/MIS: Sistema de soporte de decisiones / información gerencial
.. [#f4] Web vol. alto: Sitio web de alto volumen
.. [#f5] Pkg. Empresa: Paquete de software empresarial (ERP, etc.)

Relevancia para IACT
----------------------

IACT es un sistema de información con características de OLTP
(registro de acciones ciudadanas), DSS (reportes analíticos) y
alta disponibilidad operacional. Perfil de importancia resultante:

.. list-table::
 :header-rows: 1
 :widths: 20 15 65

 * - Viewpoint
   - Importancia en IACT
   - Justificación
 * - **Functional**
   - Alta
   - Módulos de acción ciudadana, RBAC, pipeline ETL
 * - **Information**
   - Alta
   - Estructura de datos IVR, modelo de dominio, migración
 * - **Deployment**
   - Alta
   - Nodos de procesamiento, red, BD distribuida
 * - **Context**
   - Alta
   - Integración con IVR (fuente de datos externa, solo lectura)
 * - **Development**
   - Media-alta
   - Modularidad, build pipeline, versionado
 * - **Operational**
   - Alta
   - Auditoría, monitorización, soporte en producción
 * - **Concurrency**
   - Media
   - Pipeline ETL concurrente, procesamiento de alertas

Relación con el modelo 5+1 del proyecto IACT
==============================================

.. list-table::
 :header-rows: 1
 :widths: 30 35 35

 * - Rozanski et al.
   - Modelo 5+1 IACT
   - Directorio
 * - Functional
   - Use Case View
   - ``use-case-view/``
 * - Information / Concurrency
   - Process View
   - ``process-view/``
 * - Development
   - Implementation View + Design View
   - ``implementation-view/``, ``design-view/``
 * - Deployment
   - Deployment View (+1)
   - ``deploy-view/``
 * - (Domain) — no en Rozanski
   - Domain Model / Logical View
   - ``domain-model/``
 * - Operational
   - Sin vista dedicada actualmente
   - —

----

Referencias cruzadas
=====================

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **Meta-modelo**
   - :doc:`metamodelo-descripcion`
 * - **Framework Rozanski (Tabla 1)**
   - :doc:`framework-rozanski`
 * - **Vistas arquitectónicas IACT**
   - :doc:`/arquitectura-tecnica/vistas-kruchten`
