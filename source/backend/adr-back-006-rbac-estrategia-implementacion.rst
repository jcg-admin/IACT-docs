.. meta::
 :artefacto: ADR-BACK-006
 :tipo: ADR
 :dominio: backend
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-04-29
 :ultimo_cambio: 2026-04-29
 :autor: NestorMonroy
 :clasificacion: Critico

.. _adr-back-006:

================================================================
ADR-BACK-006: RBAC Estrategia de Implementacion (Supersede 003)
================================================================

**Estado:** Aprobado.

**Fecha:** 2026-04-29.

**Decisores:** NestorMonroy.

**Supersede:**

- :doc:`/backend/adr-back-003-orm-sql-hybrid-permissions`

**Relacionados (no superseded):**

- :doc:`/normativa/gobernanza/adr-gob-009-rbac-modelo-conceptual`
  (modelo conceptual canonico)
- :doc:`/normativa/gobernanza/adr-gob-008-rbac-coexistencia-acc-perm`
  (coexistencia ACC + PERM)
- :doc:`/normativa/restricciones/cnst-032-menu-dinamico-obligatorio`
  (funcion SQL ``obtener_menu_usuario`` obligatoria)
- :doc:`/normativa/restricciones/cnst-033-vocabulario-unificado-rbac`
- :doc:`/normativa/restricciones/cnst-010-permission-class-explicita-en-vistas-drf`
- :doc:`/backend/adr-back-005-middleware-decoradores-permisos`
  (middleware/decoradores, complementario)

----

1. Contexto
===========

ADR-BACK-003 (legacy, noviembre 2025) definio la estrategia
hibrida ORM Django + SQL nativo PostgreSQL para implementar el
sistema de permisos. La estrategia tecnica era correcta pero
quedo desalineada con el corpus normativo vigente:

- Vocabulario "Capacidad" / ``Capacidad`` que CNST-033 vigente
  PROHIBE.
- Cifras "100-1000 req/s" / "8 tablas" inconsistentes con la
  recalibracion v5.2.1.
- Nota in-text "VALIDAR ESTA ESTRATEGIA" inadecuada para un
  ADR aceptado (ver Resolucion).
- Funcion SQL ``obtener_menu_usuario()`` no documentada como
  parte del enforcement obligatorio (CNST-032 vigente lo exige).

Este ADR consolida la estrategia tecnica de implementacion
**alineada al corpus vigente** + resuelve la nota in-text con la
seccion "Single source of truth for enforcement".

----

2. Decision
===========

2.1 Estrategia hibrida ORM + SQL (preservada del legacy)
--------------------------------------------------------

- **Django ORM**: para CRUD, desarrollo, testing, admin.
- **Vistas SQL** (PostgreSQL): para queries frecuentes de
  lectura.
- **Funciones SQL nativas** (PL/pgSQL): para verificaciones
  ultra-rapidas de autorizacion + enforcement.

Esta estrategia equilibra:

- Mantenibilidad (ORM para desarrollo).
- Performance (SQL para autorizacion).
- Testabilidad (ORM en fixtures/factories).

2.2 Single source of truth for enforcement (NUEVA)
--------------------------------------------------

**La verificacion final de "usuario X tiene Funcion Y?" SIEMPRE
debe pasar por la funcion SQL canonica.**

::

   usuario_tiene_funcion(p_usuario_id INTEGER,
                         p_funcion_codigo VARCHAR)
   RETURNS BOOLEAN

Reglas inviolables:

1. **El ORM Django NO implementa logica propia de evaluacion**
   de autorizacion. Solo gestiona CRUD sobre las tablas.
2. **Las vistas SQL son optimizaciones de lectura**; no son
   fuente de verdad para autorizacion.
3. **La funcion SQL es la unica fuente de verdad** para "tiene
   permiso?".
4. **Auditoria de todos los accesos** via ``verificar_funcion_y_auditar()``
   (variante atomica con write a tabla audit).

Esto resuelve la nota in-text del ADR-BACK-003 legacy:

   "VALIDAR ESTA ESTRATEGIA YA QUE ES REDUDANTE QUE SE
   CONSIDERE DEVELOP Y TEST, SE TIENE QUE CREAR UNA ESTRATEGIA
   SOLO PARA PRODUCCION PARA QUE SE MANTEGA UNA SOLA
   TRAZABILIDAD DE PERMISOS."

La inquietud era trazabilidad unica — resuelta por el principio
"single source of truth via SQL function". Develop/Test/Prod usan
la misma funcion SQL; la diferencia es solo el nivel de mocking
en tests unitarios (donde se mockea la funcion entera).

2.3 Funciones SQL canonicas (vocabulario CNST-033)
--------------------------------------------------

Renombradas del legacy para cumplir vocabulario:

.. list-table::
 :header-rows: 1
 :widths: 40 30 30

 * - Funcion legacy (vocabulario "Capacidad")
   - Funcion canonica vigente
   - Proposito
 * - ``usuario_tiene_permiso(p_usuario_id, p_capacidad_codigo)``
   - ``usuario_tiene_funcion(p_usuario_id, p_funcion_codigo)``
   - Verificacion booleana O(log n)
 * - ``obtener_capacidades_usuario(p_usuario_id)``
   - ``obtener_funciones_usuario(p_usuario_id)``
   - Array de funciones efectivas
 * - ``obtener_grupos_usuario(p_usuario_id)``
   - ``obtener_grupos_usuario(p_usuario_id)``
   - Sin cambio (vocabulario "Grupo" sigue valido)
 * - ``verificar_permiso_y_auditar(p_usuario_id, p_capacidad)``
   - ``verificar_funcion_y_auditar(p_usuario_id, p_funcion)``
   - Atomico: check + write audit
 * - ``obtener_menu_usuario(p_usuario_id)``
   - ``obtener_menu_usuario(p_usuario_id)``
   - Sin cambio (CNST-032 vigente)

2.4 Modelos Django (vocabulario CNST-033)
-----------------------------------------

Los modelos Django se nombran con vocabulario canonico:

- ``Function`` (era ``Capacidad``).
- ``FunctionGroup`` (era ``GrupoPermiso``).
- ``FunctionGroupMembership`` (era ``CapacidadGrupo``).
- ``UserFunctionAssignment`` (era ``UsuarioFuncion`` directo).
- ``UserFunctionGroupAssignment`` (era ``UsuarioGrupo``).
- ``ExceptionalFunctionGrant`` (era ``PermisoExcepcional``).
- ``FunctionAuditLog`` (era ``AuditoriaPermiso``).
- ``FunctionSeparationRule`` (era ``ReglaSoD``).

----

3. Consecuencias
================

3.1 Positivas
-------------

- Trazabilidad unica del enforcement (resuelve nota in-text
  legacy).
- Vocabulario alineado con CNST-033.
- Performance preservada (SQL para hot-path).
- Mantenibilidad preservada (ORM para CRUD/admin).
- Auditoria atomica con la verificacion (no race condition).
- ``obtener_menu_usuario()`` parte del enforcement obligatorio
  (CNST-032).

3.2 Negativas mitigadas
-----------------------

- Lock-in PostgreSQL (aceptado, no hay planes de cambio).
- Migraciones complejas para evolucionar funciones SQL —
  mitigado con Django Migrations.
- Curva de aprendizaje SQL (PL/pgSQL) para desarrolladores
  acostumbrados solo a ORM.

----

4. Plan de implementacion (cuando se materialice)
=================================================

1. **Fase 1: Schema + Modelos Django** (vocabulario canonico).
2. **Fase 2: Vistas SQL + indices optimizados**.
3. **Fase 3: Funciones SQL nativas** (5 funciones canonicas).
4. **Fase 4: Service layer Python** (wrapper sobre funciones
   SQL).
5. **Fase 5: Middleware/decoradores DRF** (per ADR-BACK-005
   middleware vigente).
6. **Fase 6: Tests + benchmarks** (overhead < 5ms p95).

----

5. Validacion y metricas
========================

Criterios de exito:

- Verificacion ``usuario_tiene_funcion()``: < 10ms (p95).
- Generacion de menu ``obtener_menu_usuario()``: < 50ms (p95).
- Cobertura de tests: > 90%.
- 100% de endpoints con ``permission_classes`` explicito
  (CNST-010 vigente).
- 100% de accesos auditados (CNST-025 vigente).

----

6. Estrategia tecnica complementaria
====================================

ADR-BACK-005 (middleware/decoradores) preservado como referencia
tecnica de la **integracion Django/DRF** con el sistema de
permisos. Cuando el codigo se materialice:

- Decoradores ``@verificar_permiso`` -> ``@verificar_funcion``
  (vocabulario CNST-033).
- ``GranularPermission`` DRF class -> usar la funcion SQL
  ``usuario_tiene_funcion()`` internamente.

Ver :doc:`/backend/adr-back-005-middleware-decoradores-permisos`
para detalles tecnicos.

----

7. Trazabilidad historica
=========================

- :doc:`/backend/adr-back-003-orm-sql-hybrid-permissions`
  (legacy supersedido por este ADR).
- :doc:`/gestion/evidencia/rbac-historia/diseno-referencia-implementacion-permisos-legacy`
  (codigo Python legacy referencia).
- :doc:`/gestion/evidencia/rbac-historia/gap-analysis-sistema-permisos-nov-2025`
  (estado nov 2025: 75% completado).
- :doc:`/normativa/gobernanza/adr-gob-009-rbac-modelo-conceptual`
  (modelo conceptual que esta estrategia implementa).
