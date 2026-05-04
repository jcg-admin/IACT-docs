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


8.8 Datos Iniciales - 74 Funciones (v5.5.0)
-------------------------------------------



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

8.10 Datos Iniciales - 3 Reglas SoD
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

9.5 Management Command
----------------------



.. code-block:: bash

 # Inicializar RBAC v5.2.1
 python manage.py initialize_permissions
 
 # O paso a paso:
 python manage.py initialize_functions # 74 funciones
 python manage.py initialize_function_groups # 12 grupos
 python manage.py initialize_separation_rules # 3 reglas SoD

