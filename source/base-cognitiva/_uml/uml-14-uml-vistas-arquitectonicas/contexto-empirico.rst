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

Los seis viewpoints de Rozanski et al.
=======================================

.. list-table::
 :header-rows: 1
 :widths: 20 80

 * - Viewpoint
   - Descripción
 * - **Functional**
   - Concierne a los elementos funcionales que componen los
     sistemas de software y sus interacciones.
 * - **Information**
   - Concierne a cómo los datos del sistema son definidos,
     almacenados, accedidos y transmitidos.
 * - **Concurrency**
   - Concierne al mapeo de los elementos funcionales en
     elementos concurrentes y sus interacciones concurrentes.
 * - **Development**
   - Concierne al modelado de los planes y decisiones tomadas
     sobre el proceso de desarrollo de software, como la
     estructuración del código y la planificación de los
     procesos de build y release.
 * - **Deployment**
   - Concierne a la estructura física de los sistemas que
     representa los elementos hardware en los que se ejecutarán
     los elementos funcionales y sus relaciones físicas.
 * - **Operational**
   - Concierne a los aspectos operacionales que ocurren mientras
     el sistema está en producción: monitorización,
     administración, restauración y soporte. Se enfoca en la
     gestión y control del sistema en ejecución, no en los
     requisitos de diseño.

.. note::

 El viewpoint **Operational** es crítico desde el punto de vista
 de esfuerzo: los problemas operacionales deben resolverse
 temprano para minimizar el esfuerzo requerido, ya que este
 puede crecer significativamente si se abordan cuando el sistema
 ya está en producción.

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
