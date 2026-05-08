.. _modelo-rbac-iact-implementacion:

====================================
Modelo RBAC IACT — Implementacion
====================================

8. IMPLEMENTACIÓN SQL
=====================



8.1 Tabla functions
-------------------



.. note::

 Los detalles de implementacion de esta operacion estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.

8.2 Tabla function_groups
-------------------------



.. note::

 Los detalles de implementacion de esta operacion estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.

8.3 Tabla function_group_membership
-----------------------------------



.. note::

 Los detalles de implementacion de esta operacion estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.

8.4 Tabla user_function_assignments
-----------------------------------



.. note::

 Los detalles de implementacion de esta operacion estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.

**CAMBIO v5.2.1:** ``assigned_at`` (NO ``assigned_date``, convención ``*_at`` para datetime)


8.5 Tabla user_function_group_assignments
-----------------------------------------



.. note::

 Los detalles de implementacion de esta operacion estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.

**CAMBIO v5.2.1:** ``assigned_at`` (convención datetime)


8.6 Tabla function_separation_rules
-----------------------------------



.. note::

 Los detalles de implementacion de esta operacion estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.

8.7 Tabla function_separation_rule_details
------------------------------------------



.. note::

 Los detalles de implementacion de esta operacion estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.

**CAMBIO v5.2.1:** ``rule_group`` (NO ``separation_group``, más conciso)


8.8 Datos Iniciales - 64 Funciones Activas (v5.6.0)
---------------------------------------------------



.. note::

 Los detalles de implementacion de esta operacion estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.

8.9 Datos Iniciales - 12 Grupos
-------------------------------



.. note::

 Los detalles de implementacion de esta operacion estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.

8.10 Datos Iniciales - 3 Reglas de Separacion
-----------------------------------



.. note::

 Los detalles de implementacion de esta operacion estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.

----


9. IMPLEMENTACIÓN DJANGO
========================



9.1 Models (appsaccessmodels.py)
--------------------------------



.. note::

 Los detalles de implementacion de este componente estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.

9.2 Service (appsaccessservices.py)
-----------------------------------



.. note::

 Los detalles de implementacion de este componente estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.

9.3 Decorator (appsaccessdecorators.py)
---------------------------------------



.. note::

 Los detalles de implementacion de este componente estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.

9.4 Middleware (appsaccessmiddleware.py)
----------------------------------------



.. note::

 Los detalles de implementacion de este componente estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.

9.5 Bootstrap del catálogo RBAC
-------------------------------

Per ADR-BACK-007, el bootstrap canónico de los 12 grupos
predefinidos AGR-001..012, las 64 funciones activas y las 3
reglas de separacion se hace **via data migration con** ``RunPython``,
no via fixtures ni management command.

Esta es la forma idiomática Django per
:doc:`/backend/adr-back-007-rbac-custom-vs-auth-group` §3.2 y
los docs oficiales:

- `Migration Operations — Django documentation
  <https://docs.djangoproject.com/en/5.0/ref/migration-operations/>`_
- `How to provide initial data for models
  <https://docs.djangoproject.com/en/6.0/howto/initial-data/>`_

9.5.1 Patrón canónico (data migration)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

 # apps/access/migrations/00NN_create_default_groups.py
 from django.db import migrations

 def create_default_groups(apps, schema_editor):
     AccessGroup = apps.get_model('access', 'AccessGroup')
     Function    = apps.get_model('access', 'Function')

     for code, name, function_codenames in PREDEFINED_GROUPS:
         group, _ = AccessGroup.objects.get_or_create(
             agr_code=code,
             defaults={'name': name, 'is_system': True},
         )
         group.functions.set(
             Function.objects.filter(codename__in=function_codenames)
         )

 class Migration(migrations.Migration):
     dependencies = [('access', '00NN-1_previous')]
     operations = [
         migrations.RunPython(create_default_groups,
                              migrations.RunPython.noop),
     ]

**Beneficios:**

- Idempotente (``get_or_create``).
- Se ejecuta automáticamente con ``python manage.py migrate``,
  incluyendo en setup de test database.
- ``apps.get_model()`` retorna la versión histórica del modelo
  en el punto de la migración (no la versión actual del código).

9.5.2 Management command (convenience wrapper, no canónico)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

 # Re-bootstrap manual del RBAC (e.g. tras reset de DB en dev)
 python manage.py initialize_permissions

 # O paso a paso:
 python manage.py initialize_functions          # 64 funciones activas (in-scope)
 python manage.py initialize_function_groups    # 12 grupos
 python manage.py initialize_separation_rules   # 3 reglas de separacion

El management command **delega internamente** en las funciones
de la data migration — no las duplica. Existe como conveniencia
para operadores que necesiten re-bootstrap manual durante
development; **NO es la fuente canónica** del estado inicial.

