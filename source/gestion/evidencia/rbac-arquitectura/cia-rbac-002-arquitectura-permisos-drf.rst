.. meta::
 :artefacto: CIA_RBAC_002
 :tipo: CIA
 :dominio: gestion
 :subdominio: evidencia/rbac-arquitectura
 :estado: Propuesto
 :version: 2.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Critico

.. _cia-rbac-002:

================================================================
CIA-RBAC-002 — Arquitectura de Permisos IACT con Django REST
================================================================

.. note::

 **Change Impact Assessment — Pendiente de implementacion.**

 Documenta las decisiones arquitectonicas derivadas del analisis
 de integracion entre el modelo RBAC IACT v5.2.1 y Django REST
 Framework. Ninguna de las decisiones aqui descritas ha sido
 implementada. Este documento es el insumo para la generacion
 de tickets de implementacion y el ADR correspondiente.

 Para el modelo de datos vigente ver
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`.

 Para el vocabulario canonico ver
 :doc:`/normativa/restricciones/cnst-033-vocabulario-unificado-rbac`.

----

1. Contexto
===========

**Fecha del analisis:** 2026-05-04.

**Modelo de referencia:** ``MODELO_RBAC_IACT_v5.2.1`` (vigente).

**Disparador:** revision del metodo ``calculate_effective_functions``
y su integracion con el sistema de permisos de Django y DRF.

El sistema RBAC de IACT resuelve permisos mediante
``calculate_effective_functions()``, que retorna el conjunto de
funciones activas para un usuario dado. Los decoradores y clases
de permiso en DRF deben integrarse con este mecanismo de forma
correcta y consistente.

**Problema detectado:** ``@require_function('RPT-001')`` pasa el
``function_id`` (``RPT-001``) como argumento, pero la funcion de
resolucion trabaja con el ``name`` (codename en ``snake_case``,
``view_reports``). Esta discrepancia produce autorizaciones
incorrectas o fallas silenciosas.

**Estado:** ninguna decision ha sido implementada. Este documento
registra formalmente las decisiones tomadas durante el analisis
para guiar la implementacion.

**Relacionados:**

- :doc:`/normativa/gobernanza/adr-gob-008-rbac-coexistencia-acc-perm`
- :doc:`/normativa/gobernanza/adr-gob-010-rbac-autorizacion-drf-backend`
- :doc:`/gestion/evidencia/rbac-historia/analisis-errores-modelo-rbac-v5-2-0`

----

2. Resumen de Decisiones
========================

.. list-table::
 :header-rows: 1
 :widths: 12 52 18 18

 * - ID
   - Decision
   - Impacto
   - Estado
 * - DEC-001
   - ``calculate_effective_functions`` retorna ``name`` (codename), no ``function_id``
   - Alto
   - Pendiente
 * - DEC-002
   - Codenames en ``snake_case`` exclusivamente
   - Medio
   - Pendiente
 * - DEC-003
   - Custom backend ``FunctionAuthorization`` para interceptar ``has_perm()``
   - Alto
   - Pendiente
 * - DEC-004
   - Catalogo centralizado ``FunctionCatalog`` — elimina strings literales
   - Medio
   - Pendiente
 * - DEC-005
   - Clase ``FunctionPermission`` para integracion con DRF
   - Alto
   - Pendiente
 * - DEC-006
   - ``app_label`` resuelto dinamicamente via ``AppConfig``
   - Bajo
   - Pendiente

----

.. _cia-rbac-002-dec-001:

3. DEC-001 — Identificador en ``calculate_effective_functions``
===============================================================

3.1 Problema identificado
--------------------------

El metodo ``calculate_effective_functions`` retornaba un
``Set[str]`` de valores ``function_id`` (``AUTH-001``,
``RPT-004``). Esto es inconsistente con el contrato del
ecosistema Django, donde el identificador canonico de un
permiso es el ``codename`` — campo de texto semantico — y no
un codigo opaco.

INCORRECTO (estado previo al analisis):

.. code-block:: python

   def calculate_effective_functions(user: User) -> Set[str]:
       """
       Returns:
           Set of function_id: {'RPT-001', 'RPT-002', ...}
       """

CORRECTO (decision adoptada):

.. code-block:: python

   def calculate_effective_functions(user: User) -> Set[str]:
       """
       Retorna el conjunto de codenames activos para el usuario,
       considerando asignaciones directas y grupos.

       Returns:
           Set of function names: {'view_reports', 'export_csv', ...}
       """

3.2 Razon tecnica
-----------------

El ``codename`` (``name`` en el modelo ``Function``) es el
identificador semantico estable para operaciones de autorizacion.
El ``function_id`` (``RPT-001``) es un codigo de catalogo — util
para trazabilidad documental, no como clave de autorizacion en
runtime.

3.3 Constraint requerida
------------------------

El campo ``name`` debe tener ``unique=True`` en el modelo
``Function``. Esta constraint garantiza que el ``Set[str]``
retornado sea un identificador sin ambiguedad.

.. code-block:: python

   class Function(models.Model):
       function_id = models.CharField(max_length=10, primary_key=True)
       name        = models.CharField(max_length=100, unique=True)
       description = models.CharField(max_length=255)
       category    = models.CharField(max_length=50)

3.4 Impacto en el modelo de datos
----------------------------------

No requiere cambio en los valores existentes de ``name``.
Requiere una migracion para agregar la constraint ``unique=True``
si no esta presente.

----

.. _cia-rbac-002-dec-002:

4. DEC-002 — Formato de Codenames: ``snake_case``
==================================================

4.1 Decision
------------

El formato canonico es ``snake_case`` sin excepcion::

   Correcto:   view_reports, export_csv, manage_sessions
   Incorrecto: view-reports, ViewReports, view reports

4.2 Razones
-----------

El formato Django estandar para codenames es ``snake_case``.
Los permisos generados automaticamente siguen este formato:
``add_post``, ``change_post``, ``delete_post``, ``view_post``.

Kebab-case (``view-reports``) no puede usarse como identificador
de variable en Python porque el guion es interpretado como
operador de resta. CNST-033 ya canonizo todos los nombres en
``snake_case``: ``manage_sessions``, ``view_reports``,
``export_csv``. Kebab-case violaria CNST-033.

4.3 Catalogo de codenames vigente
----------------------------------

El catalogo completo de ``name`` en el modelo ``Function`` es
el definido en ``MODELO_RBAC_IACT_v5.2.1``. No se introducen
nombres nuevos. Solo se formaliza que estos valores son el
identificador de autorizacion en el sistema DRF.

----

.. _cia-rbac-002-dec-003:

5. DEC-003 — Custom Backend ``FunctionAuthorization``
======================================================

5.1 Problema identificado
--------------------------

Django requiere el formato ``app_label.codename`` en
``has_perm()``. El backend estandar ``ModelBackend`` resuelve
ese contrato contra la tabla ``auth_permission``.

``auth_permission`` es infraestructura Django con ciclo de vida
acoplado a migraciones. ``functions`` es dominio IACT con ciclo
de vida acoplado al catalogo de funciones del negocio.
Introducir entradas IACT en ``auth_permission`` acopla ambos
dominios y genera una dependencia recurrente: cada cambio en
el catalogo requiere una migracion Django adicional.

5.2 Decision
------------

Se implementa un backend custom que intercepta ``has_perm()``
del dominio ``permissions`` y lo resuelve directamente contra
``calculate_effective_functions()``, sin consultar
``auth_permission``. Las llamadas de otros dominios (``auth``,
``admin``) se dejan pasar al siguiente backend en
``AUTHENTICATION_BACKENDS``.

El nombre ``FunctionAuthorization`` expresa el proposito de
dominio: autoriza por funciones. No menciona la tecnologia
(``Backend``) ni repite el contexto del modulo (``permissions``).

.. code-block:: python

   # permissions/backends.py

   from django.apps import apps
   from permissions.services import calculate_effective_functions


   class FunctionAuthorization:
       """
       Autoriza usuarios verificando sus funciones efectivas.

       Intercepta has_perm() del dominio 'permissions' y lo resuelve
       contra calculate_effective_functions(). Llamadas de otros
       dominios se dejan pasar a ModelBackend.
       """

       APP_LABEL = apps.get_app_config('permissions').label

       def authenticate(self, request, **kwargs):
           return None

       def has_perm(self, user_obj, perm, obj=None) -> bool:
           if not user_obj.is_active:
               return False

           if '.' not in perm:
               return False

           app_label, codename = perm.split('.', 1)

           if app_label != self.APP_LABEL:
               return False

           effective = calculate_effective_functions(user_obj)
           return codename in effective

.. code-block:: python

   # config/settings.py

   AUTHENTICATION_BACKENDS = [
       'permissions.backends.FunctionAuthorization',
       'django.contrib.auth.backends.ModelBackend',
   ]

5.3 Comportamiento del sistema con dos backends
------------------------------------------------

.. list-table::
 :header-rows: 1
 :widths: 40 32 28

 * - Llamada
   - Backend que responde
   - Fuente de datos
 * - ``has_perm('permissions.view_reports')``
   - ``FunctionAuthorization``
   - Tabla ``functions`` (IACT)
 * - ``has_perm('permissions.export_csv')``
   - ``FunctionAuthorization``
   - Tabla ``functions`` (IACT)
 * - ``has_perm('auth.add_user')``
   - ``ModelBackend``
   - Tabla ``auth_permission``
 * - ``has_perm('admin.view_logentry')``
   - ``ModelBackend``
   - Tabla ``auth_permission``

5.4 Por que el filtro ``app_label`` es obligatorio
---------------------------------------------------

Sin el filtro ``if app_label != self.APP_LABEL: return False``,
el backend intercepta **todas** las llamadas a ``has_perm()``,
incluyendo ``auth.add_user`` y ``admin.view_logentry``. Esas
llamadas se resolveran contra ``calculate_effective_functions()``
en lugar de ``ModelBackend``. Si algun codename IACT coincide
con uno nativo Django (p.ej. ``add_user``), el resultado sera
un falso positivo que rompe el sistema de autorizacion de forma
silenciosa.

----

.. _cia-rbac-002-dec-004:

6. DEC-004 — Catalogo Centralizado ``FunctionCatalog``
=======================================================

6.1 Problema identificado
--------------------------

Strings de permisos dispersos en vistas, servicios y tests son
una categoria de bug silencioso. Django no lanza error si el
permiso no existe — retorna ``False``. Un typo es indetectable
en tests superficiales.

El nombre ``Perm`` viola Clean Code: es una abreviacion — no es
pronunciable ni descriptivo. El nombre correcto expresa el
proposito de dominio: ``FunctionCatalog`` es el catalogo de
funciones del sistema IACT.

6.2 Decision
------------

.. code-block:: python

   # permissions/catalog.py

   from django.apps import apps


   def _perm(codename: str) -> str:
       """
       Construye el string de permiso resolviendo app_label
       dinamicamente desde AppConfig. Ver DEC-006.
       """
       app_label = apps.get_app_config('permissions').label
       return f'{app_label}.{codename}'


   class FunctionCatalog:
       """
       Catalogo de funciones del sistema IACT.

       Uso:
           user.has_perm(FunctionCatalog.VIEW_REPORTS)
           permission_classes = [
               FunctionPermission(FunctionCatalog.VIEW_REPORTS)
           ]
       """

       # MOD_Auth
       MANAGE_SESSIONS       = _perm('manage_sessions')
       CLOSE_USER_SESSION    = _perm('close_user_session')
       RESET_PASSWORD        = _perm('reset_password')
       VIEW_ACTIVE_SESSIONS  = _perm('view_active_sessions')

       # MOD_Users
       CREATE_USERS          = _perm('create_users')
       UPDATE_USERS          = _perm('update_users')
       DELETE_USERS          = _perm('delete_users')
       LIST_USERS            = _perm('list_users')
       SEARCH_USERS          = _perm('search_users')
       BLOCK_USERS           = _perm('block_users')
       UNBLOCK_USERS         = _perm('unblock_users')
       REACTIVATE_USERS      = _perm('reactivate_users')
       VIEW_USERS            = _perm('view_users')

       # MOD_Access
       ASSIGN_FUNCTIONS         = _perm('assign_functions')
       REVOKE_FUNCTIONS         = _perm('revoke_functions')
       VIEW_ASSIGNMENTS         = _perm('view_assignments')
       ASSIGN_FUNCTION_GROUPS   = _perm('assign_function_groups')
       MANAGE_SEPARATION_RULES  = _perm('manage_separation_rules')

       # MOD_Pipeline
       VIEW_PIPELINE_STATUS    = _perm('view_pipeline_status')
       VIEW_PIPELINE_ERRORS    = _perm('view_pipeline_errors')
       VIEW_DATA_AVAILABILITY  = _perm('view_data_availability')
       REQUEST_PIPELINE_RETRY  = _perm('request_pipeline_retry')

       # MOD_Reports
       VIEW_REPORTS   = _perm('view_reports')
       VIEW_DASHBOARD = _perm('view_dashboard')
       FILTER_REPORTS = _perm('filter_reports')
       EXPORT_CSV     = _perm('export_csv')
       EXPORT_EXCEL   = _perm('export_excel')
       EXPORT_PDF     = _perm('export_pdf')
       VIEW_KPIS      = _perm('view_kpis')
       VIEW_CHARTS    = _perm('view_charts')

       # MOD_Alerts
       VIEW_ALERTS           = _perm('view_alerts')
       CONFIGURE_ALERTS      = _perm('configure_alerts')
       CONFIGURE_TEAM_ALERTS = _perm('configure_team_alerts')
       PAUSE_ALERTS          = _perm('pause_alerts')
       DELETE_ALERTS         = _perm('delete_alerts')
       VIEW_ALERT_HISTORY    = _perm('view_alert_history')

       # MOD_Audit
       VIEW_AUDIT_LOG             = _perm('view_audit_log')
       SEARCH_AUDIT_LOG           = _perm('search_audit_log')
       EXPORT_AUDIT_LOG           = _perm('export_audit_log')
       GENERATE_COMPLIANCE_REPORT = _perm('generate_compliance_report')

       # MOD_Logs
       VIEW_TECHNICAL_LOGS = _perm('view_technical_logs')
       EXPORT_LOGS         = _perm('export_logs')

6.3 Impacto en el codigo existente
------------------------------------

Toda ocurrencia de strings literales de permisos debe ser
reemplazada por la constante correspondiente de
``FunctionCatalog``.

INCORRECTO:

.. code-block:: python

   user.has_perm('permissions.view_reports')
   permission_classes = [FunctionPermission('view_reports')]

CORRECTO:

.. code-block:: python

   from permissions.catalog import FunctionCatalog

   user.has_perm(FunctionCatalog.VIEW_REPORTS)
   permission_classes = [FunctionPermission(FunctionCatalog.VIEW_REPORTS)]

----

.. _cia-rbac-002-dec-005:

7. DEC-005 — Clase ``FunctionPermission`` para DRF
===================================================

7.1 Problema identificado
--------------------------

El modelo IACT es un sistema de control por vista, no por
instancia. Colocar logica IACT en ``has_object_permission``
produce comportamiento incorrecto en list views sin lanzar
errores — una categoria de bug silencioso que no aparece en
tests superficiales.

El nombre ``HasFunction`` viola Clean Code: ``Has`` es un patron
getter, no expresa el proposito de la clase. El archivo
``drf_permissions.py`` agrega ruido tecnico que el path ya
provee.

Nombres corregidos::

   INCORRECTO: drf_permissions.py  →  class HasFunction
   CORRECTO:   enforcement.py      →  class FunctionPermission

7.2 Decision
------------

.. code-block:: python

   # permissions/enforcement.py

   from rest_framework.permissions import BasePermission


   class FunctionPermission(BasePermission):
       """
       Permiso DRF para el modelo RBAC IACT.

       Verifica que el usuario autenticado tenga la funcion
       requerida en su conjunto efectivo, delegando en
       FunctionAuthorization via user.has_perm().

       Uso:
           permission_classes = [
               FunctionPermission(FunctionCatalog.VIEW_REPORTS)
           ]

       Uso con multiples funciones requeridas:
           permission_classes = [
               FunctionPermission(FunctionCatalog.VIEW_REPORTS),
               FunctionPermission(FunctionCatalog.EXPORT_CSV),
           ]
       """

       def __init__(self, function: str):
           self.function = function

       def has_permission(self, request, view) -> bool:
           if not request.user or not request.user.is_authenticated:
               return False
           return request.user.has_perm(self.function)

       def has_object_permission(self, request, view, obj) -> bool:
           """
           El modelo IACT es un sistema de control por vista, no por
           instancia. Si has_permission paso, el objeto es accesible.

           Excepcion: verificaciones SoD sobre objetos especificos
           se implementan en subclases dedicadas sobreescribiendo
           este metodo.
           """
           return True

7.3 Integracion en vistas
--------------------------

.. code-block:: python

   from permissions.catalog import FunctionCatalog
   from permissions.enforcement import FunctionPermission


   class ReportListView(APIView):
       permission_classes = [
           FunctionPermission(FunctionCatalog.VIEW_REPORTS)
       ]


   class ReportExportView(APIView):
       permission_classes = [
           FunctionPermission(FunctionCatalog.VIEW_REPORTS),
           FunctionPermission(FunctionCatalog.EXPORT_CSV),
       ]

7.4 Separacion de responsabilidades
-------------------------------------

.. list-table::
 :header-rows: 1
 :widths: 28 36 36

 * - Metodo
   - Responsabilidad
   - Logica IACT aplicable
 * - ``has_permission``
   - Control de acceso a la vista
   - Verificacion de funciones efectivas del usuario
 * - ``has_object_permission``
   - Control de acceso al objeto especifico
   - Verificacion SoD (casos excepcionales unicamente)

----

.. _cia-rbac-002-dec-006:

8. DEC-006 — ``app_label`` Resuelto Dinamicamente
==================================================

8.1 Problema identificado
--------------------------

Hardcodear el string ``'permissions'`` en llamadas a
``has_perm()`` crea acoplamiento al nombre de la app. Si el
``app_label`` cambia en ``AppConfig``, todas las verificaciones
de permisos se rompen silenciosamente — Django retorna ``False``
sin lanzar excepcion.

8.2 Decision
------------

El ``app_label`` nunca aparece como string literal fuera de
``permissions/catalog.py`` y ``permissions/backends.py``. La
funcion ``_perm()`` y el atributo ``APP_LABEL`` lo resuelven
desde ``AppConfig`` al momento de inicializacion del modulo.

.. code-block:: python

   # permissions/apps.py

   from django.apps import AppConfig


   class PermissionsConfig(AppConfig):
       name  = 'permissions'
       label = 'permissions'

8.3 Efecto ante renombre de la app
------------------------------------

.. code-block:: python

   # Si label cambia:
   class PermissionsConfig(AppConfig):
       name  = 'permissions'
       label = 'access_control'

   # FunctionCatalog.VIEW_REPORTS pasa de:
   #   'permissions.view_reports'
   # a:
   #   'access_control.view_reports'
   #
   # Sin modificar ninguna vista, servicio ni test.

----

9. Estructura de Archivos
=========================

9.1 Modulo resultante
---------------------

::

   permissions/
       apps.py          →  class PermissionsConfig
       backends.py      →  class FunctionAuthorization
       catalog.py       →  class FunctionCatalog
       enforcement.py   →  class FunctionPermission
       models.py        →  class Function  (unique=True en name)
       services.py      →  def calculate_effective_functions()
       migrations/
           XXXX_add_unique_name.py

9.2 Regla de nomenclatura aplicada
------------------------------------

.. list-table::
 :header-rows: 1
 :widths: 30 28 42

 * - Anterior
   - Correcto
   - Razon
 * - ``rbac/``
   - ``permissions/``
   - ``rbac`` es el patron de implementacion; ``permissions`` es el concepto de dominio
 * - ``RBACBackend``
   - ``FunctionAuthorization``
   - ``RBAC`` repite contexto; ``Backend`` describe mecanismo, no dominio
 * - ``permissions_registry.py``
   - ``catalog.py``
   - ``registry`` describe patron de implementacion; ``catalog`` describe dominio
 * - ``drf_permissions.py``
   - ``enforcement.py``
   - ``drf_`` es ruido tecnico; ``enforcement`` expresa el proposito
 * - ``HasFunction``
   - ``FunctionPermission``
   - ``Has`` es patron getter; ``Permission`` expresa el rol de la clase
 * - ``Perm``
   - ``FunctionCatalog``
   - ``Perm`` es abreviacion no pronunciable; ``FunctionCatalog`` es descriptivo

----

10. Mapa de Archivos Afectados
================================

.. list-table::
 :header-rows: 1
 :widths: 48 14 38

 * - Archivo
   - Accion
   - Descripcion
 * - ``permissions/models.py``
   - Modificar
   - Agregar ``unique=True`` al campo ``name`` de ``Function``
 * - ``permissions/apps.py``
   - Crear
   - ``PermissionsConfig`` con ``name`` y ``label``
 * - ``permissions/backends.py``
   - Crear
   - ``FunctionAuthorization`` — custom backend para ``has_perm()``
 * - ``permissions/catalog.py``
   - Crear
   - ``FunctionCatalog`` con catalogo canonico de constantes
 * - ``permissions/enforcement.py``
   - Crear
   - ``FunctionPermission`` para integracion DRF
 * - ``permissions/services.py``
   - Modificar
   - ``calculate_effective_functions`` retorna ``Set[str]`` de ``name``
 * - ``config/settings.py``
   - Modificar
   - Agregar ``FunctionAuthorization`` a ``AUTHENTICATION_BACKENDS``
 * - ``permissions/migrations/XXXX_add_unique_name.py``
   - Crear
   - Migracion para ``unique=True`` en ``Function.name``

----

11. Impacto en Documentos Existentes
=====================================

Los siguientes documentos contienen notacion incorrecta y deben
actualizarse antes de iniciar la implementacion:

.. list-table::
 :header-rows: 1
 :widths: 60 40

 * - Archivo
   - Correccion requerida
 * - ``rbac-historia/analisis-errores-modelo-rbac-v5-2-0.rst``
   - ``'RPT-001'`` → ``'view_reports'``
 * - ``arquitectura-tecnica/matriz-dependencias-uc-iact.rst``
   - Placeholder ``'FUNC-NNN'`` → ``'<codename>'``
 * - ``requisitos/casos-uso/permissions/uc-perm-07/informacion-general.rst``
   - Placeholder ``'F_CODE'`` → ``'<codename>'``

.. note::

   Las tres correcciones anteriores ya fueron aplicadas en el
   repositorio como parte de este WP (commits previos a este
   documento).

----

12. Riesgos y Mitigaciones
===========================

.. list-table::
 :header-rows: 1
 :widths: 42 16 42

 * - Riesgo
   - Probabilidad
   - Mitigacion
 * - ``Function.name`` no es unico en datos existentes
   - Media
   - Ejecutar query de auditoria antes de la migracion
 * - Codigo existente usa ``function_id`` en verificaciones
   - Alta
   - Busqueda global de strings de permiso antes de implementar
 * - ``FunctionAuthorization`` sin filtro ``app_label``
   - Alta
   - Test de integracion que verifica que ``auth.add_user`` no es interceptado
 * - ``FunctionAuthorization`` no registrado en ``AUTHENTICATION_BACKENDS``
   - Baja
   - Test de integracion que verifica el backend activo
 * - Logica IACT en ``has_object_permission`` en list views
   - Media
   - Revision de todas las vistas que hereden de ``FunctionPermission``

----

13. Dependencias entre Decisiones
==================================

Las decisiones tienen orden de implementacion requerido::

   DEC-002  snake_case                      <- prerequisito de todo
       |
   DEC-001  calculate_effective_functions   <- requiere DEC-002
       |
   DEC-003  FunctionAuthorization           <- requiere DEC-001
       |
   DEC-006  app_label dinamico              <- parte de DEC-003 y DEC-004
       |
   DEC-004  FunctionCatalog                 <- requiere DEC-003 y DEC-006
       |
   DEC-005  FunctionPermission              <- requiere DEC-004

DEC-002 no tiene dependencias tecnicas pero es prerequisito
semantico: todos los codenames deben estar en ``snake_case`` antes
de construir ``FunctionCatalog`` y ``FunctionAuthorization``.

----

14. Lecciones del Analisis
===========================

14.1 Sobre la eleccion del identificador
-----------------------------------------

El campo ``function_id`` (``AUTH-001``) es un identificador de
catalogo, no un identificador de autorizacion. El campo ``name``
(``manage_sessions``) es el identificador semantico que opera en
el plano del codigo. Usarlos indistintamente introduce acoplamiento
entre la capa de datos y la capa de autorizacion.

14.2 Sobre el ``app_label``
----------------------------

El ``app_label`` en ``has_perm()`` es un detalle de
infraestructura Django, no un concepto de dominio. Exponerlo como
string literal en vistas y servicios viola el principio de
separacion de responsabilidades. ``FunctionCatalog`` encapsula
ese detalle en un unico punto.

14.3 Sobre ``has_permission`` vs ``has_object_permission``
-----------------------------------------------------------

El modelo IACT es un sistema de control por funciones atomicas
asignadas a roles. Este modelo es por naturaleza de vista, no de
instancia. Colocar logica IACT en ``has_object_permission``
produce comportamiento incorrecto en list views sin lanzar errores
— una categoria de bug silencioso que no aparece en tests
superficiales.

14.4 Sobre el filtro ``app_label`` en ``FunctionAuthorization``
----------------------------------------------------------------

Un backend custom sin filtro de dominio intercepta la totalidad
de llamadas ``has_perm()`` del sistema. Esto incluye permisos de
``auth``, ``admin`` y cualquier otro modulo Django. El resultado
es la ruptura silenciosa del sistema de autorizacion completo
cuando algun codename IACT colisiona con uno nativo Django.
El filtro ``if app_label != self.APP_LABEL: return False`` es
obligatorio, no opcional.

14.5 Sobre nomenclatura de modulos y clases
--------------------------------------------

Los nombres que repiten el contexto que ya provee el path son
ruido. Los nombres que describen mecanismo de implementacion en
lugar de proposito de dominio violan Clean Code. La regla
aplicada en este documento es unica: el nombre debe expresar
que hace la clase en lenguaje del dominio, no como lo hace ni
donde vive.

----

15. Proximos Pasos
==================

Este documento es el insumo para:

- Apertura de tickets de implementacion por cada decision
  (DEC-001 a DEC-006).
- Revision y aprobacion de
  :doc:`/normativa/gobernanza/adr-gob-010-rbac-autorizacion-drf-backend`
  antes de iniciar la implementacion de DEC-003.
- Actualizacion de los documentos listados en la seccion 11.
- Ejecucion del plan de migracion para ``unique=True`` en
  ``Function.name`` si existen valores duplicados.

----

16. Trazabilidad
================

.. list-table::
 :header-rows: 1
 :widths: 30 70

 * - Referencia
   - Path
 * - Modelo de datos vigente
   - :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index` (v5.2.1)
 * - Restriccion normativa aplicable
   - :doc:`/normativa/restricciones/cnst-033-vocabulario-unificado-rbac`
 * - Analisis historico que origino v5.2.1
   - :doc:`/gestion/evidencia/rbac-historia/analisis-errores-modelo-rbac-v5-2-0`
 * - ADR de decision de backend
   - :doc:`/normativa/gobernanza/adr-gob-010-rbac-autorizacion-drf-backend`
 * - ADR relacionado
   - :doc:`/normativa/gobernanza/adr-gob-008-rbac-coexistencia-acc-perm`
