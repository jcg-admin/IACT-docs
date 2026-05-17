.. meta::
 :artefacto: UML_14_PERSPECTIVAS
 :tipo: Referencia — Perspectivas Arquitectonicas
 :dominio: base_cognitiva
 :subdominio: _uml
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uml-14-perspectivas:

=======================================================
Perspectivas Arquitectónicas
=======================================================

Fuente: Rozanski & Woods, *Software Systems Architecture* — Cap. 4.

----

Viewpoints y calidad del sistema
==================================

Los viewpoints (Functional, Information, Concurrency, etc.) son una
excelente forma de particionar la arquitectura en un conjunto de
modelos interrelacionados. Sin embargo, típicamente se evalúan para
completitud y corrección solo contra requisitos funcionales, no contra
otras cualidades del sistema como rendimiento, seguridad o disponibilidad.

Esto puede resultar en un sistema funcionalmente correcto pero con
tiempo de respuesta pobre, inseguro o poco confiable.

Los concerns que impulsan estas propiedades de calidad son comunes a
muchas o todas las vistas. La seguridad, por ejemplo, afecta aspectos
de la arquitectura abordados por la mayoría de los viewpoints:

- **Desde el viewpoint Functional:** el sistema necesita identificar y
  autenticar a sus usuarios. Los procesos de seguridad deben ser
  efectivos pero no intrusivos.
- **Desde el viewpoint Information:** el sistema debe controlar
  diferentes clases de acceso a la información (lectura, inserción,
  actualización, borrado) a distintos niveles de granularidad.
- **Desde el viewpoint Operational:** el sistema debe mantener y
  distribuir información secreta (claves, contraseñas) y estar
  actualizado con los últimos parches de seguridad.
- **Desde los viewpoints Development, Concurrency y Deployment:** se
  encontrarán también aspectos afectados por requisitos de seguridad.

El criterio "el sistema debe ser seguro" se descompone en criterios
más específicos a través de los viewpoints. Por eso, intentar abordar
estas propiedades de calidad mediante un viewpoint adicional no
funciona bien: no tiene sentido crear una vista de seguridad aislada
porque la seguridad tiene implicaciones en todas las demás vistas.

.. admonition:: Problema

 Las propiedades de calidad son *cross-cutting*: afectan múltiples
 vistas simultáneamente. No pueden encapsularse en un viewpoint
 adicional sin duplicar análisis o perder coherencia.

----

Concepto de Perspectiva Arquitectónica
========================================

Se necesita algo en el modelo conceptual que sea "ortogonal" a los
viewpoints. Este concepto se denomina **perspectiva arquitectónica**.

.. admonition:: Definición

 Una **perspectiva arquitectónica** es una colección de actividades
 arquitectónicas, tácticas y directrices que se usan para asegurar
 que un sistema exhibe un conjunto particular de propiedades de
 calidad relacionadas, que requieren consideración a través de un
 número de vistas arquitectónicas del sistema.

.. admonition:: Definición

 Una **táctica arquitectónica** es un enfoque establecido y probado
 que se puede usar para ayudar a lograr una propiedad de calidad
 particular.

Las perspectivas sistematizan lo que un buen arquitecto hace de todas
formas: entender las propiedades de calidad requeridas; evaluar y
revisar los modelos arquitectónicos para asegurar que la arquitectura
exhibe las propiedades requeridas; identificar, prototipar, probar y
seleccionar tácticas arquitectónicas para abordar los casos en que la
arquitectura es deficiente.

.. note::

 No confundir tácticas con patrones de diseño. Una táctica es más
 general y menos restrictiva: no impone una estructura software
 particular sino que provee orientación general sobre cómo diseñar
 un aspecto del sistema.

----

Aplicar perspectivas a vistas
================================

Una perspectiva no se trabaja en aislamiento: se aplica a cada vista
de la arquitectura para analizar y validar sus cualidades y para
impulsar la toma de decisiones arquitectónicas adicionales. Esto se
describe como *aplicar la perspectiva a la vista*.

La relación entre perspectivas y vistas es muchos-a-muchos: aunque
cada perspectiva puede aplicarse a cada vista, en la práctica
(por restricciones de tiempo y riesgos a abordar) solo se aplican
algunas perspectivas a algunas vistas.

El resultado de aplicar una perspectiva a una vista puede ser:

.. list-table::
 :header-rows: 1
 :widths: 20 80

 * - Resultado
   - Descripción
 * - **Insights**
   - Algo — habitualmente algún tipo de modelo — que proporciona
     una visión de la capacidad del sistema para cumplir una
     propiedad de calidad requerida. Demuestra que la arquitectura
     cumple sus requisitos o que es deficiente en algún aspecto.
 * - **Mejoras**
   - Si la perspectiva revela que la arquitectura no cumplirá una
     propiedad de calidad, la arquitectura necesita mejorarse:
     cambiar modelos existentes, crear modelos adicionales, o ambos.
 * - **Artefactos**
   - Modelos y entregables de valor duradero producidos al aplicar
     la perspectiva. Deben preservarse y referenciarse desde la AD.

Actualización del modelo conceptual
--------------------------------------

Aplicar perspectivas añade dos relaciones al modelo conceptual base
(Figura 3-1):

- El contenido de una vista puede ser **moldeado por** varias
  perspectivas, para asegurar la capacidad del sistema de exhibir
  las propiedades de calidad que la perspectiva considera.
- Una perspectiva **aborda** concerns de los stakeholders del sistema.

.. uml::
 :caption: Figura 4-1 — Perspectivas en contexto (extensión del modelo conceptual)

 @startuml uml14-perspectivas-en-contexto

 skinparam classAttributeIconSize 0
 skinparam classBorderColor #333333
 skinparam classBackgroundColor White
 skinparam ArrowColor #444444
 skinparam shadowing false

 class "Architectural\nDescription (AD)" as ArchDescription
 class "View" as ArchView
 class "Viewpoint" as Viewpoint
 class "Concern" as Concern
 class "Stakeholder" as Stakeholder
 class "Perspective" as Perspective

 ArchDescription "comprises 1..n" *-- ArchView
 ArchView --> Viewpoint : conforms to
 Viewpoint --> Concern : addresses
 Stakeholder --> Concern : has
 Perspective --> Concern : addresses
 Perspective --> ArchView : shapes\n{0..n}

 @enduml

----

Beneficios de las perspectivas
================================

.. list-table::
 :header-rows: 1
 :widths: 30 70

 * - Beneficio
   - Descripción
 * - **Guía de decisiones**
   - La perspectiva define concerns que guían la toma de
     decisiones arquitectónicas para asegurar que la arquitectura
     exhibirá las propiedades de calidad consideradas.
 * - **Convenciones compartidas**
   - Provee convenciones comunes, mediciones o incluso una
     notación para describir las cualidades del sistema.
 * - **Validación**
   - Describe cómo validar la arquitectura para demostrar que
     cumple sus requisitos a través de cada vista.
 * - **Soluciones reconocidas**
   - Ofrece soluciones reconocidas a problemas comunes,
     ayudando a compartir conocimiento entre arquitectos.
 * - **Trabajo sistemático**
   - Ayuda a trabajar de forma sistemática para asegurar que
     sus concerns son abordados por el sistema.

Pitfalls al aplicar perspectivas
-----------------------------------

- Cada perspectiva aborda un conjunto relacionado de concerns de
  propiedades de calidad. Habrá a menudo conflictos entre las
  soluciones sugeridas por diferentes perspectivas (p.ej. un sistema
  altamente evolucionable puede ser menos eficiente). Balancear
  estas necesidades en competencia es una parte importante del rol
  del arquitecto.
- Los concerns y prioridades de los stakeholders son diferentes para
  cada sistema. El grado en que debe considerarse cada perspectiva
  varía considerablemente.
- Las perspectivas contienen consejo general establecido. Cada
  situación es diferente — aplicar el consejo con criterio.

----

Catálogo de perspectivas (Rozanski & Woods)
=============================================

El catálogo definido para sistemas de información a gran escala
incluye las siguientes perspectivas principales:

.. list-table::
 :header-rows: 1
 :widths: 22 78

 * - Perspectiva
   - Descripción
 * - **Security**
   - Asegura el acceso controlado a los recursos sensibles del
     sistema. Afecta: Functional (autenticación, autorización),
     Information (control de acceso a datos), Deployment
     (elementos hardware/software de seguridad), Operational
     (gestión de claves y parches).
 * - **Performance & Scalability**
   - Cumplir el perfil de rendimiento requerido y manejar
     cargas de trabajo crecientes satisfactoriamente.
 * - **Availability & Resilience**
   - Asegurar la disponibilidad del sistema cuando se requiere y
     hacer frente a fallos que podrían afectarla.
 * - **Evolution**
   - Asegurar que el sistema puede hacer frente a los cambios
     probables.
 * - **Regulation**
   - Capacidad del sistema para conformarse a leyes locales e
     internacionales, regulaciones cuasi-legales, políticas de
     empresa y otros estándares.

.. admonition:: Estrategia

 Aplicar solo las perspectivas más relevantes a las vistas.
 Basar la selección en las necesidades de los stakeholders, la
 importancia relativa de las diferentes propiedades de calidad
 para ellos, y la propia experiencia y criterio del arquitecto.

----

Perspectivas aplicadas al proyecto IACT
==========================================

IACT es un sistema de información con RBAC, pipeline ETL, auditoría
regulatoria e integración con IVR. Las perspectivas más relevantes:

.. list-table::
 :header-rows: 1
 :widths: 22 78

 * - Perspectiva
   - Relevancia en IACT
 * - **Security**
   - Crítica. RBAC multi-nivel (AGR_ADMIN, AGR_OPERADOR,
     AGR_AUDITOR), JWT, acceso de solo lectura a IVR (CNST-007),
     control granular por función.
     ✓ Implementado: :doc:`/arquitectura-tecnica/perspectivas/perspectiva-security`
 * - **Regulation**
   - Alta. Auditoría de acceso regulatoria, trazabilidad de
     acciones ciudadanas, cumplimiento normativo institucional.
     ✓ Implementado: :doc:`/arquitectura-tecnica/perspectivas/perspectiva-regulation`
 * - **Availability & Resilience**
   - Alta. Sistema de acción ciudadana territorial — la
     indisponibilidad tiene impacto directo en operaciones de campo.
     ✓ Implementado: :doc:`/arquitectura-tecnica/perspectivas/perspectiva-availability`
 * - **Performance & Scalability**
   - Media-alta. Pipeline ETL sobre datos IVR de alto volumen,
     dashboards con consultas agregadas, alertas en tiempo real.
     Parcialmente cubierto en process-view/ e implementation-view/.
 * - **Evolution**
   - Media-alta. Arquitectura modular planificada para crecimiento
     incremental de módulos funcionales.
     Parcialmente cubierto en implementation-view/ y design-view/.

Grid de aplicación perspectiva × vista para IACT
--------------------------------------------------

.. list-table::
 :header-rows: 2
 :stub-columns: 1
 :widths: 22 13 13 13 13 13 13

 * - Vista
   - Security
   - Regulation
   - Availability
   - Performance
   - Evolution
   -
 * -
   - *(acceso y autenticación)*
   - *(auditoría y cumplimiento)*
   - *(disponibilidad)*
   - *(rendimiento y escala)*
   - *(evolucionabilidad)*
   -
 * - **Domain Model**
   - Media
   - Media
   - Baja
   - Baja
   - Alta
   -
 * - **Use Case View**
   - Alta
   - Alta
   - Baja
   - Media
   - Alta
   -
 * - **Process View**
   - Media
   - Media
   - Alta
   - Alta
   - Media
   -
 * - **Design View**
   - Alta
   - Media
   - Media
   - Media
   - Alta
   -
 * - **Implementation View**
   - Media
   - Baja
   - Baja
   - Baja
   - Alta
   -
 * - **Deployment View (+1)**
   - Alta
   - Baja
   - Alta
   - Alta
   - Media
   -

----

Perspectivas vs. Viewpoints — comparación
===========================================

.. list-table::
 :header-rows: 1
 :widths: 20 40 40

 * - Concepto
   - Viewpoint
   - Perspective
 * - **Qué produce**
   - Una vista (modelos que describen la arquitectura)
   - Cambios a vistas existentes (insights, mejoras, artefactos)
 * - **Enfoque**
   - Guiar la producción de modelos que describen la arquitectura
   - Proveer actividades y tácticas para asegurar que el sistema
     exhibe propiedades de calidad requeridas
 * - **Resultado**
   - Nuevas estructuras (vistas)
   - Modificaciones a estructuras existentes
 * - **Concerns**
   - Funcionales / estructurales
   - Propiedades de calidad (*cross-cutting*)
 * - **Relación con ISO 42010**
   - Formalizado en el estándar como concept central
   - No está en ISO 42010 — es contribución original de
     Rozanski & Woods, compatible mediante "modelos compartidos
     entre vistas"

----

Referencias cruzadas
=====================

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **Vistas y Viewpoints (Cap. 3)**
   - :doc:`vistas-y-viewpoints`
 * - **Framework Rozanski (Tabla 1)**
   - :doc:`framework-rozanski`
 * - **Comparación de frameworks**
   - :doc:`frameworks-comparacion`
 * - **Vistas arquitectónicas IACT**
   - :doc:`/arquitectura-tecnica/vistas-kruchten`
