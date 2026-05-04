.. meta::
 :artefacto: CIA_RBAC_002
 :tipo: CIA
 :dominio: gestion
 :subdominio: evidencia/rbac-arquitectura
 :estado: Propuesto
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Critico

.. _cia-rbac-002:

================================================================
CIA-RBAC-002 — Arquitectura de Permisos IACT con Django REST
================================================================

**Estado:** Propuesto.

**Fecha:** 2026-05-04.

**Tipo:** Change Impact Assessment.

**Relacionados:**

- :doc:`/normativa/gobernanza/adr-gob-008-rbac-coexistencia-acc-perm`
- :doc:`/normativa/gobernanza/adr-gob-010-rbac-autorizacion-drf-backend`
- :doc:`/gestion/evidencia/rbac-historia/analisis-errores-modelo-rbac-v5-2-0`

----

Contexto
========

El sistema RBAC de IACT resuelve permisos mediante la funcion
``calculate_effective_functions()`` que retorna el conjunto de
funciones activas para un usuario dado. Los decoradores y clases
de permiso en DRF deben integrarse con este mecanismo de forma
correcta y consistente.

El problema detectado: ``@require_function('RPT-001')`` pasa el
``function_id`` (e.g. ``RPT-001``) como argumento, pero la funcion
de resolucion trabaja con el ``name`` (codename en snake_case,
e.g. ``view_reports``). Esta discrepancia produce autorizaciones
incorrectas o fallas silenciosas.

----

Decisiones
==========

.. _cia-rbac-002-dec-001:

DEC-001 — ``calculate_effective_functions()`` retorna codenames
---------------------------------------------------------------

**Impacto:** Alto. Afecta toda integracion entre el sistema RBAC
y DRF.

``calculate_effective_functions()`` DEBE retornar ``Set[str]`` de
``name`` (codename), NO de ``function_id``.

.. code-block:: python

   def calculate_effective_functions(user) -> Set[str]:
       """
       Retorna el conjunto de codenames activos para el usuario.
       Ejemplo de retorno: {'view_reports', 'export_reports', 'view_ivr'}
       NO retorna function_ids como 'RPT-001'.
       """
       ...

**Razon:** El codename (``name`` en el modelo ``Function``) es el
identificador semantico estable. El ``function_id`` (``RPT-001``) es
un codigo de catalogo — util para trazabilidad documental, NO como
clave de autorizacion en runtime.

.. _cia-rbac-002-dec-002:

DEC-002 — Codenames exclusivamente en ``snake_case``
----------------------------------------------------

**Impacto:** Medio. Afecta consistencia del catalogo.

Todos los codenames DEBEN seguir ``snake_case``:

- Correcto: ``view_reports``, ``export_ivr_data``, ``manage_users``
- Incorrecto: ``view-reports``, ``ViewReports``, ``view reports``

**Razon:** Consistencia con la convencion Django de permisos nativos
y con ``auth.Permission.codename``.

.. _cia-rbac-002-dec-003:

DEC-003 — Backend custom ``FunctionAuthorization``
--------------------------------------------------

**Impacto:** Alto. Reemplaza el bridge a ``auth_permission``.

Un backend custom intercepta ``has_perm()`` sin depender de
``auth_permission``:

.. code-block:: python

   class FunctionAuthorization:
       """
       Backend de autorizacion que resuelve permisos contra
       la tabla 'functions' del modelo RBAC IACT.
       """

       def authenticate(self, request, **kwargs):
           return None  # solo autoriza, no autentica

       def has_perm(self, user_obj, perm, obj=None):
           """
           perm llega en formato 'app_label.codename'
           (e.g. 'permissions.view_reports').
           """
           if not user_obj.is_active:
               return False
           app_label, codename = perm.split('.', 1)
           effective = calculate_effective_functions(user_obj)
           return codename in effective

**Razon:** La tabla ``functions`` es la unica fuente de verdad para
el modelo RBAC de IACT. No debe existir un puente a
``auth.Permission`` que duplique la logica y genere inconsistencias.

.. _cia-rbac-002-dec-004:

DEC-004 — Clase ``Perm`` centraliza constantes
----------------------------------------------

**Impacto:** Medio. Elimina strings literales dispersos.

.. code-block:: python

   from django.apps import apps

   def _perm(codename: str) -> str:
       app_label = apps.get_app_config('permissions').label
       return f'{app_label}.{codename}'

   class Perm:
       """Catalogo centralizado de permisos IACT."""
       VIEW_REPORTS    = _perm('view_reports')
       EXPORT_REPORTS  = _perm('export_reports')
       VIEW_IVR        = _perm('view_ivr')
       MANAGE_USERS    = _perm('manage_users')
       # ... resto del catalogo

**Uso en vistas:**

.. code-block:: python

   from permissions.constants import Perm

   @permission_required(Perm.VIEW_REPORTS)
   def list_reports(request):
       ...

**Razon:** Strings literales dispersos son fragiles ante renombrados
y dificultan el grep. La clase ``Perm`` es el punto unico de verdad
para codenames en codigo Python.

.. _cia-rbac-002-dec-005:

DEC-005 — ``FunctionPermission`` para DRF
-----------------------------------------

**Impacto:** Alto. Reemplaza el uso de ``IsAuthenticated`` sin
control RBAC en endpoints DRF.

.. code-block:: python

   from rest_framework.permissions import BasePermission

   class FunctionPermission(BasePermission):
       """
       Permission class DRF que delega en FunctionAuthorization.

       Uso:
           permission_classes = [FunctionPermission('view_reports')]
       """

       def __init__(self, codename: str):
           self.codename = codename

       def has_permission(self, request, view):
           perm = f'{APP_LABEL}.{self.codename}'
           return request.user.has_perm(perm)

**Integracion en viewsets DRF:**

.. code-block:: python

   class ReportViewSet(ModelViewSet):
       permission_classes = [FunctionPermission('view_reports')]

**Razon:** DRF usa ``has_perm()`` internamente. Delegando en
``FunctionAuthorization`` (DEC-003), ``FunctionPermission`` se
integra de forma natural con el pipeline de autorizacion DRF.

.. _cia-rbac-002-dec-006:

DEC-006 — ``app_label`` resuelto dinamicamente
-----------------------------------------------

**Impacto:** Bajo. Elimina hardcodeo del app_label.

.. code-block:: python

   from django.apps import apps

   APP_LABEL = apps.get_app_config('permissions').label

**Razon:** Hardcodear ``'permissions'`` en strings de permisos crea
una dependencia fragil al nombre del modulo. Resolverlo via
``AppConfig`` permite renombrar el modulo sin grep masivo.

----

Impacto en documentos existentes
=================================

Los siguientes documentos contienen notacion incorrecta (uso de
``function_id`` donde se requiere codename) y deben actualizarse:

.. list-table::
 :widths: 55 45
 :header-rows: 1

 * - Archivo
   - Correccion requerida
 * - ``rbac-historia/analisis-errores-modelo-rbac-v5-2-0.rst``
   - Seccion "CORRECTO": ``'RPT-001'`` → ``'view_reports'``
 * - ``arquitectura-tecnica/matriz-dependencias-uc-iact.rst``
   - Placeholder ``'FUNC-NNN'`` → ``'<codename>'``
 * - ``requisitos/casos-uso/permissions/uc-perm-07/informacion-general.rst``
   - Placeholder ``'F_CODE'`` → ``'<codename>'``

----

Trazabilidad
============

.. list-table::
 :widths: 20 80
 :header-rows: 1

 * - Ref
   - Descripcion
 * - ADR-GOB-008
   - Coexistencia ACC+PERM — contexto de la decision
 * - ADR-GOB-010
   - Decision de adoptar FunctionAuthorization (Option B)
 * - CNST-033
   - Vocabulario unificado RBAC (snake_case codenames)
