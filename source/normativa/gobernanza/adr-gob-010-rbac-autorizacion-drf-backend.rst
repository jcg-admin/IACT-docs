.. meta::
 :artefacto: ADR_GOB_010
 :tipo: ADR
 :dominio: normativa
 :subdominio: gobernanza
 :estado: Propuesto
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Critico

.. _adr-gob-010:

================================================================
ADR-GOB-010: RBAC — Backend de Autorizacion DRF (Option B)
================================================================

**Estado:** Propuesto.

**Fecha:** 2026-05-04.

**Decisores:** NestorMonroy.

**Relacionados:**

- :doc:`adr-gob-008-rbac-coexistencia-acc-perm`
- :doc:`adr-gob-009-rbac-modelo-conceptual`
- :doc:`/gestion/evidencia/rbac-arquitectura/cia-rbac-002-arquitectura-permisos-drf`

----

Contexto
========

El sistema RBAC de IACT define funciones (``Function``) con un
``function_id`` (catalogo, e.g. ``RPT-001``) y un ``name``
(codename en snake_case, e.g. ``view_reports``). Django y DRF
utilizan ``user.has_perm('app_label.codename')`` como mecanismo
de autorizacion.

Se necesita integrar el modelo RBAC de IACT con el pipeline
de autorizacion de Django REST Framework sin duplicar la logica
de resolucion de permisos ni crear dependencias fragiles hacia
``auth.Permission``.

----

Opciones evaluadas
==================

Option A — Bridge ``auth_permission``
--------------------------------------

Sincronizar cada ``Function`` del modelo IACT con una
``auth.Permission`` de Django. El sistema RBAC crea y mantiene
registros en ``auth_permission`` espejando las funciones IACT.

**Ventajas:**

- Compatible con el ecosistema Django/DRF sin customizacion.
- Admin de Django muestra permisos nativamente.

**Desventajas:**

- Duplicacion de datos: ``Function.name`` espejado en
  ``auth.Permission.codename``.
- Sincronizacion fragil: cambios en ``Function`` requieren
  actualizar ``auth.Permission`` atomicamente.
- La tabla ``functions`` deja de ser la unica fuente de verdad.
- ``auth_permission`` introduce un modelo de permisos plano que
  no captura la jerarquia de grupos funcionales (FunctionGroup).

Option B — Backend custom ``FunctionAuthorization``
----------------------------------------------------

Implementar un backend de autorizacion Django que intercepta
``has_perm()`` y resuelve directamente contra
``calculate_effective_functions()``, sin pasar por
``auth.Permission``.

**Ventajas:**

- La tabla ``functions`` es la unica fuente de verdad.
- No hay sincronizacion: el backend resuelve en tiempo real.
- Integra con DRF via ``FunctionPermission(BasePermission)``
  sin modificar el pipeline DRF estandar.
- ``calculate_effective_functions()`` retorna ``Set[str]`` de
  codenames — un solo tipo, sin ambiguedad.

**Desventajas:**

- Requiere implementacion y mantenimiento del backend custom.
- El admin de Django no muestra los permisos IACT nativamente
  (requiere customizacion adicional del admin si se necesita).

----

Decision
========

**Se adopta Option B — FunctionAuthorization custom backend.**

La tabla ``functions`` es y permanece como la unica fuente de
verdad del modelo RBAC IACT. Option A introduce duplicacion
estructural incompatible con ADR-GOB-009 (modelo conceptual)
y con CNST-033 (vocabulario unificado RBAC).

----

Consecuencias
=============

**Positivas:**

1. ``calculate_effective_functions(user)`` retorna ``Set[str]``
   de codenames (``name``). No hay ambiguedad entre
   ``function_id`` y codename.
2. ``@require_function('<codename>')`` pasa el codename, no el
   ``function_id``. Ejemplo correcto:
   ``@require_function('view_reports')``, NO
   ``@require_function('RPT-001')``.
3. ``FunctionPermission('view_reports')`` es la forma canonica
   para DRF — ver
   :ref:`DEC-005 <cia-rbac-002-dec-005>` en CIA-RBAC-002.
4. La clase ``Perm`` centraliza constantes eliminando strings
   literales — ver :ref:`DEC-004 <cia-rbac-002-dec-004>`.

**Negativas / Compromisos:**

1. El admin de Django requiere customizacion si se desea
   visualizar permisos IACT en la interfaz nativa.
2. Tests de integracion DRF deben mockear
   ``FunctionAuthorization``, no ``auth.Permission``.

----

Implementacion de referencia
============================

Ver :doc:`/gestion/evidencia/rbac-arquitectura/cia-rbac-002-arquitectura-permisos-drf`
para el codigo de referencia completo de:

- ``FunctionAuthorization`` (DEC-003)
- Clase ``Perm`` (DEC-004)
- ``FunctionPermission`` (DEC-005)
- Resolucion dinamica de ``app_label`` (DEC-006)
