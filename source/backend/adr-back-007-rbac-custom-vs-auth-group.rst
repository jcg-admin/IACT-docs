.. meta::
 :artefacto: ADR-BACK-007
 :tipo: ADR
 :dominio: backend
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-06
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Interno

.. _adr-back-007:

============================================================================
ADR-BACK-007: RBAC con AccessGroup custom vs ``django.contrib.auth.Group``
============================================================================

Estado y metadata
=================

- **Estado:** Aprobada.
- **Fecha:** 2026-05-06.
- **Decisores:** NestorMonroy (ejecutor) + investigación
  documentada en WP
  ``2026-05-06-19-27-21-agr-django-permission-groups-research``.
- **Contexto tecnico:** Backend — modelo de datos RBAC v5.6.0.
- **Relacionados:**

  - :doc:`/backend/adr-back-001-grupos-funcionales-sin-jerarquia`
    — modelo flat sin herencia (compatible).
  - :doc:`/backend/adr-back-005-middleware-decoradores-permisos`
    — capa middleware/decoradores (ortogonal).
  - :doc:`/backend/adr-back-006-rbac-estrategia-implementacion`
    — estrategia de implementación.
  - :doc:`/normativa/restricciones/cnst-029-rbac-modelo-plano`.
  - :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`.

- **Refs research (WP-5):** ``research/raw/Q1`` (auth.Group y
  auth.Permission), ``Q2`` (data migration bootstrap), ``Q5``
  (custom vs extender), ``Q7`` (separation of duties).

----

1. Contexto y Problema
======================

Django provee un modelo nativo
``django.contrib.auth.models.Group`` listo para usar:

   *"Groups are a generic way of categorizing users so you can
   apply permissions, or some other label, to those users. A
   user can belong to any number of groups, and a user in a
   group automatically has the permissions granted to that
   group."*
   — `django.contrib.auth | Django documentation
   <https://docs.djangoproject.com/en/6.0/ref/contrib/auth/>`_.

El proyecto IACT requiere:

1. **12 grupos predefinidos** (AGR-001..AGR-012) con códigos
   estables como natural keys (mejor que solo ``name`` para
   referencia multi-entorno).
2. **Distinción entre grupos del sistema (predefinidos) y
   custom** creables por administradores en runtime
   (UC_PERM_05). El proyecto la modela con
   ``AccessGroup.is_system: BOOLEAN``.
3. **Separation of Duties** mediante 3 reglas
   declarativas que restringen pares de funciones mutuamente
   exclusivas (BR-007, ``FunctionSeparationRule``).
4. **Metadata adicional por grupo**: descripción profesional
   ("profile_description"), categoría de permisos, audit
   trail de cambios.
5. **Permisos temporales excepcionales** con vencimiento (CNST-031).

**Pregunta arquitectónica:**

¿Conviene usar ``django.contrib.auth.models.Group`` directamente
(con custom permissions) o crear un modelo ``AccessGroup``
independiente?

----

2. Factores de Decisión
=======================

- **Idiomática Django:** alineamiento con la documentación
  oficial.
- **Compatibilidad con tooling tercero:** ``django-guardian``,
  ``django-admin``, packages que asumen ``auth.Group``.
- **Capacidad de extender el modelo:** agregar campos como
  ``is_system``, ``profile_description``, audit fields.
- **Costo de implementación y mantenimiento.**
- **Riesgo de regresión** si se cambia el modelo después.
- **Auditabilidad y trazabilidad.**

----

3. Decisión
===========

Se mantiene un modelo ``AccessGroup`` **custom independiente**
de ``django.contrib.auth.models.Group``, junto con un modelo
``Function`` independiente de ``django.contrib.auth.models.Permission``.

Esta decisión documenta formalmente la elección que el catálogo
RBAC v5.6.0 ya implementa (``catalogo-funciones.rst``,
``grupos-funciones.rst``, ``modelo-datos.rst``).

3.1 Por qué NO ``auth.Group``
-----------------------------

Hay tres consideraciones documentadas en la comunidad Django:

(a) **El modelo ``auth.Group`` no es customizable nativamente.**

   *"Django's contrib.auth Group model is not customizable,
   forcing users to work around Django to customize it, and
   customization is necessary in any bigger project."*
   — `Custom Group model — Django Internals — Django Forum
   <https://forum.djangoproject.com/t/custom-group-model/30070>`_.

   El ticket oficial `#29748 — Add AUTH_GROUP_MODEL setting
   <https://code.djangoproject.com/ticket/29748>`_ propone
   permitir swappear el modelo Group (paralelo a
   ``AUTH_USER_MODEL``), pero **sigue abierto desde 2018**.

(b) **Necesidad de campos custom**: ``is_system``, audit fields, código AGR estable como natural key.

   ``auth.Group`` solo tiene ``id`` (autoincrement) y ``name``.
   El proyecto requiere:

   - Código estable AGR-001..AGR-012 (natural key).
   - Flag ``is_system`` para enforcement de inmutabilidad.
   - Descripción profesional larga.
   - Categoría operativa.

(c) **Separacion de funciones requiere modelo de relación adicional.**

   Django no provee separacion de funciones nativa (Q7 del WP-5):

   *"In RBAC, permissions are associated with roles... RBAC
   uses mutual exclusion constraints to implementar políticas de separacion."*
   — `On Mutually-Exclusive Roles and Separation of Duty
   (Purdue) <https://www.cs.purdue.edu/homes/ninghui/papers/sod-j.pdf>`_.

   El modelo ``FunctionSeparationRule`` requiere referencias
   directas al modelo de grupos. Tener ``AccessGroup`` propio
   facilita estas FK.

3.2 Bootstrap canónico via data migration
-----------------------------------------

Per `Migration Operations — Django documentation
<https://docs.djangoproject.com/en/5.0/ref/migration-operations/>`_:

   *"RunPython is generally the operation you would use to
   create data migrations, run custom data updates and
   alterations, and anything else you need access to an ORM
   and/or Python code for."*

Y `How to provide initial data for models
<https://docs.djangoproject.com/en/6.0/howto/initial-data/>`_:

   *"Since Django 1.7, automatic loading of fixtures is
   deprecated when applications use migrations, and if you
   want to load initial data for an app, consider doing it in
   a migration."*

**Decisión:** los 12 grupos AGR-001..012, las 64 funciones
activas y las 3 reglas de separacion se **bootstrap via data migrations
con** ``RunPython``, no via fixtures ni management commands.

El management command ``manage.py initialize_permissions`` se
preserva como **convenience wrapper** para re-bootstrap manual
(reset RBAC durante development), pero no es la fuente
canónica del estado inicial — la data migration sí lo es.

----

4. Consecuencias
================

4.1 Positivas
-------------

- **Control total** sobre el modelo: campos como ``is_system``,
  audit fields, código estable AGR.
- **Separacion de funciones nativa** del modelo IACT — relación FK directa entre
  ``FunctionSeparationRule`` y ``AccessGroup``.
- **Natural keys estables** (AGR-001..012) que sobreviven
  migraciones de DB.
- **Bootstrap canónico Django** via ``RunPython`` data
  migration (alineado con docs).
- **Separación clara** entre infraestructura del sistema
  (``is_system=True``) y configuración runtime (``is_system=False``).

4.2 Negativas (aceptadas)
-------------------------

- **Pérdida de compatibilidad con tooling tercero** que asume
  ``auth.Group``:

   *"The design limitation restricts other app development, as
   many Django permission packages only support group
   permissions based on django.contrib.auth.models.Group, like
   django-guardian."*
   — Django Forum, op. cit.

   Mitigación: si en el futuro se adopta ``django-guardian``,
   se puede agregar adapter o wrapper sin reemplazar
   ``AccessGroup``.

- **No reutiliza Django admin nativo** para gestión de Group.
  Mitigación: se puede registrar ``AccessGroup`` en admin con
  ``ModelAdmin`` custom; el costo es bajo.

- **Más código a mantener** vs solución nativa.
  Mitigación: la complejidad va con el dominio (RBAC con separacion de funciones
  no es trivial en ningún caso).

4.3 Neutrales
-------------

- **Permission backend custom requerido** — DRF
  ``DjangoModelPermissions`` no funciona out-of-the-box con
  ``Function``/``AccessGroup``. ADR-BACK-005 documenta la
  capa middleware/decoradores que enforce ``Function`` codes
  via ``user.has_perm()`` extendido.

----

5. Alternativas Consideradas
============================

5.1 Alternativa B — Migrar a ``auth.Group`` con custom permissions
------------------------------------------------------------------

Reemplazar ``AccessGroup`` con ``auth.Group`` y ``Function``
con ``auth.Permission`` (custom codenames vía ``Meta.permissions``).

- **Pros:** alineación máxima con Django; compatibilidad con
  ``django-guardian``, admin nativo, packages tercero.
- **Contras:** refactor masivo del backend Y del corpus IACT-docs
  (ya estabilizado en sesiones 2026-05-06). ``is_system``
  requeriría proxy model o admin-level enforcement. Riesgo alto
  de regresión.
- **Veredicto:** descartada por costo desproporcionado vs
  beneficio en el estado actual del proyecto.

5.2 Alternativa C — Wrapper ``OneToOneField`` (Role → Group)
------------------------------------------------------------

Crear modelo ``Role`` con ``OneToOneField`` a
``auth.Group``, agregando campos custom:

::

   class Role(models.Model):
       group = models.OneToOneField(Group, on_delete=models.CASCADE)
       agr_code = models.CharField(max_length=10, unique=True)
       is_system = models.BooleanField(default=False)
       profile_description = models.TextField()

- **Pros:** mantiene compatibilidad con tooling Django; agrega
  flexibilidad sin replicar el modelo.
- **Contras:** introduce dos capas (Role + Group) que el
  desarrollador debe entender; refactor moderado pero no
  trivial; corpus IACT-docs ya documenta ``AccessGroup``
  directo en ~80 archivos.
- **Veredicto:** considerar como **migración futura** si el
  proyecto adopta ``django-guardian`` u otros paquetes
  dependientes de ``auth.Group``. Documentado como TD-RBAC-02
  para evaluación posterior.

----

6. Implementación
=================

6.1 Bootstrap canónico (data migration)
---------------------------------------

Cada nuevo grupo, función o regla de separacion se introduce en el
sistema vía data migration con ``RunPython``:

::

   # apps/access/migrations/00NN_create_default_groups.py

   from django.db import migrations

   PREDEFINED_GROUPS = [
       ('AGR-001', 'basic_operator_group',  ['view_own_sessions', ...]),
       ('AGR-006', 'user_admin_group',      ['create_users', ...]),
       ('AGR-010', 'system_admin_group',    ['create_separation_rule', ...]),
       # ...12 total
   ]

   def create_default_groups(apps, schema_editor):
       AccessGroup = apps.get_model('access', 'AccessGroup')
       Function = apps.get_model('access', 'Function')

       for code, name, function_codes in PREDEFINED_GROUPS:
           group, _ = AccessGroup.objects.get_or_create(
               agr_code=code,
               defaults={'name': name, 'is_system': True},
           )
           perms = Function.objects.filter(codename__in=function_codes)
           group.functions.set(perms)

   class Migration(migrations.Migration):
       dependencies = [
           ('access', '00NN-1_previous_migration'),
       ]
       operations = [
           migrations.RunPython(create_default_groups,
                                migrations.RunPython.noop),
       ]

Patrón canónico per
`Migration Operations <https://docs.djangoproject.com/en/5.0/ref/migration-operations/>`_:

- ``apps.get_model()`` retorna la versión histórica del modelo
  en el punto de la migración (no la versión actual del código).
- ``get_or_create`` hace la operación idempotente.
- Reverse function ``RunPython.noop`` o función explícita para
  rollback.

6.2 Management command como convenience (no canonico)
-----------------------------------------------------

::

   # apps/access/management/commands/initialize_permissions.py

Sigue existiendo para casos donde un operador quiere re-bootstrap
manual (e.g. tras un reset de DB en development). Internamente
**delega en las funciones de la data migration**, no las duplica.

6.3 Verificación
----------------

- Tras ``python manage.py migrate`` (incluyendo en setup de test
  database) se cargan automáticamente los 12 grupos, 64
  funciones activas, 3 reglas de separacion.
- Test asserting que los AGR-001..012 existen y tienen los
  ``is_system=True`` esperados.

----

7. Trazabilidad
===============

- **Decisión consistente con:** ADR-BACK-001 (modelo flat sin
  jerarquía), ADR-BACK-005 (middleware/decoradores), CNST-029,
  CNST-030, CNST-031.
- **Research soporte:** WP
  ``2026-05-06-19-27-21-agr-django-permission-groups-research``.
  Hallazgos verbatim en ``research/raw/Q1..Q8.md``.
- **Síntesis:** ``analyze/django-rbac-idiomatic-analysis.md``
  del WP-5.
- **Deuda técnica derivada:**

  - **TD-RBAC-01**: migrar el bootstrap real del backend de
    ``manage.py initialize_permissions`` a data migration con
    ``RunPython`` (este ADR documenta el patrón; la migración
    de código real queda en el repo backend).
  - **TD-RBAC-02**: re-evaluar Alternativa C (wrapper
    ``OneToOneField``) si el proyecto adopta paquetes que
    dependen de ``auth.Group``.

----

8. Referencias
==============

8.1 Documentación oficial Django/DRF
------------------------------------

- `django.contrib.auth | Django documentation
  <https://docs.djangoproject.com/en/6.0/ref/contrib/auth/>`_
  — modelo Group y Permission nativos.
- `Using the Django authentication system
  <https://docs.djangoproject.com/en/6.0/topics/auth/default/>`_.
- `Migration Operations
  <https://docs.djangoproject.com/en/5.0/ref/migration-operations/>`_
  — ``RunPython``.
- `How to provide initial data for models
  <https://docs.djangoproject.com/en/6.0/howto/initial-data/>`_.
- `Customizing authentication in Django
  <https://docs.djangoproject.com/en/6.0/topics/auth/customizing/>`_.
- `Permissions — Django REST framework
  <https://www.django-rest-framework.org/api-guide/permissions/>`_.

8.2 Tickets / discusiones de la comunidad
-----------------------------------------

- `Custom Group model — Django Internals — Django Forum
  <https://forum.djangoproject.com/t/custom-group-model/30070>`_.
- `Django Ticket #29748 — Add AUTH_GROUP_MODEL setting
  <https://code.djangoproject.com/ticket/29748>`_.
- `Providing initial data: fixtures vs datamigration
  <https://forum.djangoproject.com/t/providing-initial-data-fixtures-vs-datamigration/2644>`_.

8.3 Fundamento teórico
----------------------

- `On Mutually-Exclusive Roles and Separation of Duty
  (Purdue) <https://www.cs.purdue.edu/homes/ninghui/papers/sod-j.pdf>`_
  — fundamento académico de separacion en RBAC.
- NIST RBAC standard (referenciado en BR-006-rbac-flat-nist).
