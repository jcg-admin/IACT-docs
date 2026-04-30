.. meta::
 :artefacto: PLAN_DOC_UC_UML
 :tipo: Plan
 :dominio: gestion
 :subdominio: pm
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-04-30
 :ultimo_cambio: 2026-04-30
 :autor: NestorMonroy
 :clasificacion: Interno

==============================================================
Plan de documentación de UCs con diagramas UML (PlantUML)
==============================================================

.. note::

 Plan de trabajo para documentar los **97 casos de uso** del
 proyecto IACT en **13 documentos temáticos**, cada uno
 incluyendo diagramas UML en **PlantUML** (no Mermaid — política
 del proyecto per
 :doc:`/normativa/estandares/adr-std-007-naming-kebab-correction`
 + :doc:`/base-cognitiva/plantuml-guide/guidelines`).

 Aplica skill ``pm-planning`` (PMBOK Planning).

----

1. Objetivo
===========

Crear **13 documentos** que especifiquen los **97 casos de uso**
del proyecto IACT con diagramas UML completos en PlantUML, usando
los estilos centralizados del proyecto.

Cada documento agrupa los UCs por dominio funcional (acceso,
catálogo, órdenes, pagos, logística, etc.) y aplica la plantilla
canónica
:doc:`/normativa/estandares/plantillas/tpl-uc-spec-con-diagramas-uml`.

----

2. Contexto y origen
====================

Este plan reemplaza la propuesta original "GUÍA DE INTEGRACIÓN
UML v2.0.0 con Mermaid" (interna), adaptándola a la convención
PlantUML del proyecto. Los 97 UCs y la distribución temática se
preservan; cambia únicamente la herramienta de diagramación.

----

3. Tipos de diagramas obligatorios
==================================

Cada UC documentado debe incluir, según aplique, los siguientes
tipos de diagrama (todos en PlantUML):

.. list-table::
 :widths: 25 75
 :header-rows: 1

 * - Tipo de diagrama
   - Cuándo es obligatorio
 * - **Casos de uso**
   - Siempre.
 * - **Estados**
   - Si el UC modifica el estado de una entidad observable.
 * - **Secuencias**
   - Si interactúan ≥ 3 componentes (frontend, backend, BD,
     APIs externas).
 * - **Actividades**
   - Si el flujo principal tiene decisiones, ramas o
     concurrencia.
 * - **Clases**
   - Si el UC introduce o modifica entidades del modelo de
     datos.
 * - **Componentes**
   - En docs consolidados (DOC-26).
 * - **Distribución**
   - En docs consolidados (DOC-26).
 * - **Colaboraciones**
   - Cuando aporta clarificación adicional al diagrama de
     secuencias.

Plantilla canónica:
:doc:`/normativa/estandares/plantillas/tpl-uc-spec-con-diagramas-uml`.

----

4. Distribución de los 13 documentos
====================================

.. list-table::
 :widths: 8 22 12 58
 :header-rows: 1

 * - Doc
   - Dominio (UCs)
   - # UCs
   - Diagramas previstos
 * - **DOC-14**
   - UC_ACC (Acceso / Autenticación)
   - 12
   - UC, Estados, Secuencias, Clases
 * - **DOC-15**
   - UC_CAT (Catálogo)
   - 13
   - UC, Actividades, Secuencias
 * - **DOC-16**
   - UC_CAR (Carrito)
   - 6
   - UC, Estados, Secuencias
 * - **DOC-17**
   - UC_ORD (Órdenes) **[CRÍTICO]**
   - 8
   - UC, Estados, Secuencias [MEGA]
 * - **DOC-18**
   - UC_PAG (Pagos — Stripe)
   - 7
   - UC, Secuencias [Stripe]
 * - **DOC-19**
   - UC_LOG (Logística)
   - 8
   - UC, Colaboraciones, Secuencias
 * - **DOC-20**
   - UC_REP + UC_NOT (Reportes + Notificaciones)
   - 13
   - UC, Actividades, Secuencias
 * - **DOC-21**
   - UC_FAV + UC_REV (Favoritos + Reviews)
   - 10
   - UC, Estados, Clases
 * - **DOC-22**
   - UC_PRO + UC_INV (Promociones + Inventario)
   - 12
   - UC, Actividades, Clases
 * - **DOC-23**
   - UC_ADM (Administración)
   - 8
   - UC, Clases, Actividades
 * - **DOC-24**
   - Clases consolidadas (cross-dominio)
   - —
   - Diagrama de clases COMPLETO integrado
 * - **DOC-25**
   - Secuencias críticas
   - —
   - 5 diagramas de secuencias de UCs críticos
 * - **DOC-26**
   - Componentes + Distribución
   - —
   - Componentes (arquitectura) + Deployment (despliegue)
 * - **TOTAL**
   - 10 dominios + 3 docs cross
   - **97 UCs**
   - 13 documentos

----

5. Ubicación de los documentos generados
========================================

Los 13 documentos viven dentro de
``source/requisitos/casos-uso/<modulo>/`` cada uno como
``uc-<mod>-<NN>-<desc>.rst`` per
:doc:`/normativa/estandares/adr-std-007-naming-kebab-correction`.

Los 3 docs cross (DOC-24..26) se ubican en:

- **DOC-24** (clases consolidadas):
  ``source/arquitectura-tecnica/modelo-clases-consolidado.rst``
- **DOC-25** (secuencias críticas):
  ``source/arquitectura-tecnica/secuencias-criticas.rst``
- **DOC-26** (componentes + deployment):
  ``source/arquitectura-tecnica/componentes-y-distribucion.rst``

Los 10 docs por dominio (DOC-14..23) generan **N archivos UC
individuales** dentro de su submódulo, no un único archivo
monolítico. Por ejemplo, DOC-14 (UC_ACC) produce 12 archivos
``casos-uso/access/uc-acc-NN-*.rst``.

----

6. Política de diagramación
===========================

- **Herramienta:** PlantUML (no Mermaid). Decisión del proyecto.
- **Estilos centralizados:** todos los diagramas inician con
  ``!include ../../_static/plantuml-styles.puml`` (ajustar la
  profundidad relativa según ubicación del archivo).
- **Conversión Mermaid → PlantUML:** cuando se reciba contenido
  fuente en Mermaid, aplicar la tabla de mapeo de
  :doc:`/normativa/estandares/plantillas/tpl-uc-spec-con-diagramas-uml`
  § 4.

----

7. Roadmap de ejecución (por orden recomendado)
===============================================

Orden sugerido por **dependencia y criticidad**:

1. **DOC-14** (UC_ACC) — base de seguridad, todos los demás UC
   dependen de tener auth resuelta.
2. **DOC-23** (UC_ADM) — administración, necesaria para que los
   UC operativos tengan datos.
3. **DOC-15** (UC_CAT) — catálogo, base para carrito/órdenes.
4. **DOC-22** (UC_PRO + UC_INV) — promociones e inventario,
   dependen de catálogo.
5. **DOC-16** (UC_CAR) — carrito, depende de catálogo.
6. **DOC-17** (UC_ORD) — órdenes [CRÍTICO], depende de
   carrito + inventario.
7. **DOC-18** (UC_PAG) — pagos, integra Stripe, depende de
   órdenes.
8. **DOC-19** (UC_LOG) — logística, depende de órdenes.
9. **DOC-20** (UC_REP + UC_NOT) — reportes/notificaciones,
   transversal post-órdenes.
10. **DOC-21** (UC_FAV + UC_REV) — favoritos y reviews,
    independiente de órdenes.
11. **DOC-24** (clases consolidadas) — al cierre, integra
    todos los modelos.
12. **DOC-25** (secuencias críticas) — al cierre, integra
    interacciones cross-dominio.
13. **DOC-26** (componentes + distribución) — al cierre,
    arquitectura física.

----

8. Estimación
=============

.. list-table::
 :widths: 35 25 40
 :header-rows: 1

 * - Bloque
   - UCs
   - Esfuerzo estimado
 * - DOC-14..23 (UC operativos)
   - 97
   - ~1.5–2 h por UC × 97 = **145–195 h**
 * - DOC-24 (clases consolidadas)
   - —
   - ~8–12 h
 * - DOC-25 (secuencias críticas)
   - —
   - ~6–10 h
 * - DOC-26 (componentes + dist.)
   - —
   - ~10–15 h
 * - **Total**
   -
   - **~170–230 horas**

Estimación basada en complejidad media + diagramas previstos.
Ajustar al primer DOC completado para recalibrar.

----

9. Criterios de aceptación por documento
========================================

Cada UC documentado debe cumplir:

1. ✓ Metadata canónica (per STD-007 + plantilla canónica).
2. ✓ Diagrama de casos de uso PlantUML embebido.
3. ✓ Diagramas adicionales según matriz § 3 de este plan.
4. ✓ Secciones completas: precondiciones, flujo principal,
   flujos alternativos, postcondiciones, reglas, excepciones,
   casos de prueba.
5. ✓ Trazabilidad bidireccional: BReq origen, BR aplicables,
   FRs derivados.
6. ✓ Build Sphinx limpio (0 warnings) tras agregar el archivo.
7. ✓ **Análisis OOP completo** per
   :doc:`/normativa/estandares/metodologia-oop-para-ucs` —
   documentar las seis dimensiones (abstracción,
   encapsulamiento, herencia, polimorfismo, envío de mensajes,
   asociaciones) y aprobar el checklist § 6 de la metodología.
8. ✓ **Análisis de dominio completo** per
   :doc:`/normativa/estandares/metodologia-analisis-dominio-ucs`
   — extracción de sustantivos→clases, verbos→operaciones,
   adjetivos→atributos; clases asignadas a un paquete UML;
   restricciones documentadas. Aprobar el checklist § 8 de la
   metodología.

----

10. Riesgos y mitigaciones
==========================

.. list-table::
 :widths: 30 35 35
 :header-rows: 1

 * - Riesgo
   - Impacto
   - Mitigación
 * - Conversión Mermaid → PlantUML genera errores semánticos
   - Diagrama incorrecto, decisiones técnicas mal informadas
   - Validar visualmente cada diagrama tras conversión; usar
     plantilla canónica
 * - 97 UCs es alcance grande; riesgo de inconsistencia entre
     docs
   - Vocabulario divergente, refs rotas
   - Aplicar plantilla canónica estrictamente; revisión
     cruzada cada 10 UCs
 * - Cambios en el modelo de datos durante la documentación
   - Diagramas de clases obsoletos
   - Postergar DOC-24 al final; usar refs
     ``:doc:`` para que actualicen automáticamente
 * - Dependencias inter-UC no detectadas hasta DOC-25
   - Re-trabajo en docs ya cerrados
   - Generar DOC-25 incrementalmente conforme cierren los UCs
     críticos (no esperar al final)

----

11. Trazabilidad
================

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **Skill aplicada**
   - ``pm-planning`` (PMBOK — Planning)
 * - **Origen del plan**
   - Adaptado de "GUÍA DE INTEGRACIÓN UML v2.0.0" (propuesta
     interna en Mermaid), reescrito para PlantUML por política
     del proyecto.
 * - **Ejemplos UML aplicados al dominio IACT**
   - :doc:`ejemplos-uml-aplicados-iact`
 * - **Ejemplos OOP aplicados al dominio IACT**
   - :doc:`ejemplos-oop-aplicados-iact`
 * - **Ejemplos análisis de dominio aplicados al dominio IACT**
   - :doc:`ejemplos-analisis-dominio-aplicados-iact`
 * - **Ejemplos relaciones UML aplicadas al dominio IACT**
   - :doc:`ejemplos-relaciones-uml-aplicados-iact`
 * - **Plantilla aplicable**
   - :doc:`/normativa/estandares/plantillas/tpl-uc-spec-con-diagramas-uml`
 * - **Metodología de análisis de dominio aplicable**
   - :doc:`/normativa/estandares/metodologia-analisis-dominio-ucs`
 * - **Metodología OOP aplicable**
   - :doc:`/normativa/estandares/metodologia-oop-para-ucs`
 * - **Política de diagramación**
   - :doc:`/base-cognitiva/plantuml-guide/guidelines`
 * - **Catálogo PlantUML del proyecto**
   - :doc:`/base-cognitiva/plantuml-guide/diagramas-de-referencia`
 * - **Convención de naming**
   - :doc:`/normativa/estandares/adr-std-007-naming-kebab-correction`
 * - **Catálogo UC actual**
   - :doc:`/requisitos/casos-uso/index`
