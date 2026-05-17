.. meta::
 :artefacto: CNST_033
 :tipo: Restriccion Normativa
 :dominio: normativa
 :subdominio: restricciones
 :estado: Aprobado
 :version: 2.0.0
 :fecha_creacion: 2026-01-13
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Critico

.. _cnst-033:

================================================================
CNST-033 — Vocabulario Unificado RBAC IACT
================================================================

.. note::

 **Restriccion normativa vigente.**

 Define el vocabulario canonico del sistema RBAC IACT. Todo
 codigo, documento y artefacto del sistema debe seguir las
 convenciones aqui definidas sin excepcion.

 La version 1.0.0 de este documento fue generada como
 resultado del analisis de errores documentado en
 :doc:`/gestion/evidencia/rbac-historia/analisis-errores-modelo-rbac-v5-2-0`.

 La version 2.0.0 incorpora las convenciones de nomenclatura
 de modulos y clases Python derivadas del analisis documentado
 en :doc:`/gestion/evidencia/rbac-arquitectura/cia-rbac-002-arquitectura-permisos-drf`.

 Para el modelo de datos vigente ver
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`.

----

1. Proposito
============

Este documento establece el vocabulario canonico del sistema
RBAC IACT. Su proposito es garantizar consistencia absoluta en
la nomenclatura de todos los artefactos del sistema — codigo,
base de datos, documentacion y tests — eliminando la ambiguedad
que produjo los 87+ errores documentados en
``MODELO_RBAC_IACT_v5.2.0``.

El incumplimiento de cualquier regla de este documento
constituye un error de nivel CRITICO en revision de codigo.

----

2. Regla Fundamental
====================

::

   CODIGO:         Ingles     (clases, metodos, variables, codenames,
                               nombres de funciones, campos SQL)
   DOCUMENTACION:  Espanol    (docstrings, help_text, description,
                               comments, mensajes de error)

**No hay excepciones.** El argumento de que un concepto es "de
dominio" y por tanto debe estar en espanol fue la causa raiz de
los 87+ errores de ``MODELO_RBAC_IACT_v5.2.0``. Ese argumento
queda formalmente invalidado por este documento.

----

3. Convenciones por Capa
========================

3.1 Codenames de Funciones
--------------------------

Los codenames son los valores del campo ``name`` en el modelo
``Function``. Son el identificador de autorizacion en runtime.

**Formato:** ``snake_case`` en ingles.

**Patron de construccion:** ``{verbo}_{objeto}``

.. list-table::
 :header-rows: 1
 :widths: 30 30 40

 * - Correcto
   - Incorrecto
   - Razon
 * - ``view_reports``
   - ``ve_reportes``
   - Ingles obligatorio
 * - ``view_reports``
   - ``view-reports``
   - ``snake_case`` obligatorio
 * - ``view_reports``
   - ``ViewReports``
   - ``snake_case`` obligatorio
 * - ``view_reports``
   - ``viewReports``
   - ``snake_case`` obligatorio
 * - ``export_csv``
   - ``exporta_csv``
   - Ingles obligatorio
 * - ``manage_sessions``
   - ``gestiona_sesiones``
   - Ingles obligatorio
 * - ``view_audit_log``
   - ``ve_auditoria``
   - Ingles + ``log`` explicito
 * - ``view_charts``
   - ``ve_graficos``
   - ``charts``, no ``graphics``
 * - ``view_pipeline_status``
   - ``ve_estado_etl``
   - Ingles + sin acronimos

**Regla sobre acronimos:** los acronimos tecnicos (``ETL``,
``IVR``, abreviaturas de dominio como separation of duties)
se expanden a terminos descriptivos en ingles cuando forman
parte de un codename. ``ETL`` → ``pipeline``,
separation of duties → ``separation``.

3.2 Identificadores de Funciones
---------------------------------

Los ``function_id`` son codigos de catalogo para trazabilidad
documental. No son identificadores de autorizacion en runtime.

**Formato:** ``{MODULO}-{NNN}`` (uso interno de BD — no aparece en codigo de autorizacion)

Los modulos validos son:

.. list-table::
 :header-rows: 1
 :widths: 20 80

 * - Prefijo
   - Modulo
 * - ``AUTH``
   - Autenticacion y sesiones
 * - ``USR``
   - Usuarios
 * - ``ACC``
   - Acceso y asignaciones
 * - ``PIP``
   - Pipeline de datos
 * - ``RPT``
   - Reportes
 * - ``ALR``
   - Alertas
 * - ``AUD``
   - Auditoria
 * - ``LOG``
   - Logs tecnicos

3.3 Nombres de Grupos de Funciones
-----------------------------------

Los nombres son los valores del campo ``name`` en el modelo
``FunctionGroup``.

**Formato:** ``{rol}_{scope}_group`` o ``{rol}_group``

**Reglas:**

- Ingles obligatorio.
- Sin prefijo ``agr_`` (redundante con ``group_id``).
- Terminar siempre con ``_group``.

.. list-table::
 :header-rows: 1
 :widths: 30 30 40

 * - Correcto
   - Incorrecto
   - Razon
 * - ``basic_operator_group``
   - ``agr_operador_basico``
   - Ingles + sin prefijo redundante
 * - ``report_viewer_group``
   - ``agr_visualizador_reportes``
   - Ingles + sin prefijo
 * - ``system_admin_group``
   - ``agr_admin_sistema``
   - Ingles + sin prefijo
 * - ``auditor_group``
   - ``agr_auditor``
   - Ingles + sin prefijo

3.4 Nombres de Reglas de Separacion
-------------------------------------

Los nombres son los valores del campo ``name`` en el modelo
``SeparationRule``.

**Formato:** ``{dominio_a}_{dominio_b}_separation``

**Reglas:**

- Ingles obligatorio.
- Sin prefijo ``sod_`` (redundante con ``rule_id``).
- Terminar siempre con ``_separation``.
- Descriptivo: debe indicar los dos dominios que se separan.

.. list-table::
 :header-rows: 1
 :widths: 32 32 36

 * - Correcto
   - Incorrecto
   - Razon
 * - ``pipeline_audit_separation``
   - ``sod_admin_auditoria``
   - Ingles + descriptivo + sin prefijo
 * - ``user_audit_separation``
   - ``sod_usuarios_auditoria``
   - Ingles + descriptivo + sin prefijo
 * - ``access_audit_separation``
   - ``sod_acceso_auditoria``
   - Ingles + descriptivo + sin prefijo

3.5 Campos SQL
--------------

**Formato:** ``snake_case`` en ingles.

**Convencion de fechas y tiempos:**

- ``*_at`` para campos ``datetime`` (``assigned_at``,
  ``created_at``, ``updated_at``).
- ``*_date`` para campos ``date`` exclusivamente.

.. list-table::
 :header-rows: 1
 :widths: 35 30 35

 * - Correcto
   - Incorrecto
   - Razon
 * - ``rule_group``
   - ``separation_group``
   - Mas conciso y claro
 * - ``assigned_at``
   - ``assigned_date``
   - Convencion ``*_at`` para datetime
 * - ``created_at``
   - ``creation_date``
   - Convencion ``*_at`` para datetime

----

4. Convenciones Python
======================

4.1 Modulos
-----------

**Regla:** el nombre del modulo debe expresar el concepto de
dominio que contiene, no el patron de implementacion ni el
acronimo tecnologico.

.. list-table::
 :header-rows: 1
 :widths: 28 28 44

 * - Correcto
   - Incorrecto
   - Razon
 * - ``permissions/``
   - ``rbac/``
   - ``rbac`` es el patron; ``permissions`` es el dominio
 * - ``catalog.py``
   - ``permissions_registry.py``
   - ``registry`` es patron; ``catalog`` es dominio
 * - ``enforcement.py``
   - ``drf_permissions.py``
   - ``drf_`` es ruido tecnico; ``enforcement`` expresa proposito
 * - ``backends.py``
   - ``rbac_backends.py``
   - El prefijo repite el contexto del modulo

4.2 Clases
----------

**Regla:** el nombre de la clase debe expresar que hace en
lenguaje del dominio, no como lo hace ni donde vive.

.. list-table::
 :header-rows: 1
 :widths: 28 28 44

 * - Correcto
   - Incorrecto
   - Razon
 * - ``FunctionAuthorization``
   - ``RBACBackend``
   - ``RBAC`` repite contexto; ``Backend`` describe mecanismo
 * - ``FunctionCatalog``
   - ``Perm``
   - ``Perm`` es abreviacion no pronunciable
 * - ``FunctionCatalog``
   - ``Permissions``
   - ``Permissions`` es plural de infraestructura, no dominio
 * - ``FunctionAccessPolicy``
   - ``HasFunction``
   - ``Has`` es patron getter, no expresa el rol de la clase
 * - ``FunctionAccessPolicy``
   - ``RBACPermission``
   - ``RBAC`` repite contexto del modulo

4.3 Metodos y funciones
------------------------

**Formato:** ``snake_case`` en ingles.

**Regla:** el nombre debe expresar que retorna o que hace, no
como lo hace.

.. list-table::
 :header-rows: 1
 :widths: 40 35 25

 * - Correcto
   - Incorrecto
   - Razon
 * - ``calculate_effective_functions``
   - ``get_rbac_perms``
   - Descriptivo + sin acronimos
 * - ``has_perm``
   - ``check_rbac``
   - Estandar Django; no se reemplaza

4.4 Docstrings y comentarios
-----------------------------

**Idioma:** espanol.

**Regla:** los docstrings documentan el proposito y el contrato.
Los ejemplos en docstrings usan codenames en ingles (codigo),
no ``function_id``.

INCORRECTO:

.. code-block:: python

   def calculate_effective_functions(user: User) -> Set[str]:
       """
       Returns:
           Set de codenames: {'view_reports', 'view_dashboard', ...}
       """

CORRECTO:

.. code-block:: python

   def calculate_effective_functions(user: User) -> Set[str]:
       """
       Calcula las funciones efectivas del usuario considerando
       asignaciones directas y grupos.

       Returns:
           Set of function names: {'view_reports', 'export_csv', ...}
       """

4.5 ``help_text`` y ``description``
-------------------------------------

**Idioma:** espanol.

**Regla:** los ejemplos dentro de ``help_text`` y ``description``
usan codenames en ingles.

INCORRECTO:

.. code-block:: python

   name = models.CharField(
       help_text="Nombre descriptivo (ve_reportes, exporta_csv)"
   )

CORRECTO:

.. code-block:: python

   name = models.CharField(
       help_text="Nombre descriptivo (view_reports, export_csv)"
   )

----

5. Catalogo Canonico de Codenames
==================================

Catalogo completo de valores ``name`` del modelo ``Function``
en ``MODELO_RBAC_IACT_v5.2.1``. Estos son los identificadores
de autorizacion en runtime.

5.1 MOD_Auth
------------

.. list-table::
 :header-rows: 1
 :widths: 35 65

 * - Codename
   - Descripcion
 * - ``manage_sessions``
   - Gestiona sesiones activas
 * - ``close_user_session``
   - Cierra la sesion de un usuario especifico
 * - ``reset_password``
   - Resetea la contrasena de un usuario
 * - ``view_active_sessions``
   - Visualiza las sesiones activas del sistema

5.2 MOD_Users
-------------

.. list-table::
 :header-rows: 1
 :widths: 35 65

 * - Codename
   - Descripcion
 * - ``create_users``
   - Crea nuevos usuarios en el sistema
 * - ``update_users``
   - Modifica datos de usuarios existentes
 * - ``delete_users``
   - Elimina usuarios del sistema
 * - ``list_users``
   - Lista el catalogo de usuarios
 * - ``search_users``
   - Busca usuarios por criterios
 * - ``block_users``
   - Bloquea el acceso de un usuario
 * - ``unblock_users``
   - Desbloquea el acceso de un usuario
 * - ``reactivate_users``
   - Reactiva un usuario inactivo
 * - ``view_users``
   - Visualiza el detalle de un usuario

5.3 MOD_Access
--------------

.. list-table::
 :header-rows: 1
 :widths: 35 65

 * - Codename
   - Descripcion
 * - ``assign_functions``
   - Asigna funciones directas a un usuario
 * - ``revoke_functions``
   - Revoca funciones directas de un usuario
 * - ``view_assignments``
   - Visualiza las asignaciones de funciones
 * - ``assign_function_groups``
   - Asigna grupos de funciones a un usuario
 * - ``manage_separation_rules``
   - Gestiona las reglas de separacion de funciones

5.4 MOD_Pipeline
----------------

.. list-table::
 :header-rows: 1
 :widths: 35 65

 * - Codename
   - Descripcion
 * - ``view_pipeline_status``
   - Visualiza el estado del pipeline de datos
 * - ``view_pipeline_errors``
   - Visualiza los errores del pipeline de datos
 * - ``view_data_availability``
   - Visualiza la disponibilidad de datos
 * - ``request_pipeline_retry``
   - Solicita reintento de ejecucion del pipeline

5.5 MOD_Reports
---------------

.. list-table::
 :header-rows: 1
 :widths: 35 65

 * - Codename
   - Descripcion
 * - ``view_reports``
   - Visualiza el listado de reportes
 * - ``view_dashboard``
   - Visualiza el dashboard principal
 * - ``filter_reports``
   - Aplica filtros sobre reportes
 * - ``export_csv``
   - Exporta datos en formato CSV
 * - ``export_excel``
   - Exporta datos en formato Excel
 * - ``export_pdf``
   - Exporta datos en formato PDF
 * - ``view_kpis``
   - Visualiza indicadores clave de desempeno
 * - ``view_charts``
   - Visualiza graficos del sistema

5.6 MOD_Alerts
--------------

.. list-table::
 :header-rows: 1
 :widths: 35 65

 * - Codename
   - Descripcion
 * - ``view_alerts``
   - Visualiza las alertas del sistema
 * - ``configure_alerts``
   - Configura alertas propias
 * - ``configure_team_alerts``
   - Configura alertas del equipo
 * - ``pause_alerts``
   - Pausa alertas activas
 * - ``delete_alerts``
   - Elimina alertas del sistema
 * - ``view_alert_history``
   - Visualiza el historial de alertas

5.7 MOD_Audit
-------------

.. list-table::
 :header-rows: 1
 :widths: 35 65

 * - Codename
   - Descripcion
 * - ``view_audit_log``
   - Visualiza el log de auditoria
 * - ``search_audit_log``
   - Busca registros en el log de auditoria
 * - ``export_audit_log``
   - Exporta el log de auditoria
 * - ``generate_compliance_report``
   - Genera reportes de cumplimiento normativo

5.8 MOD_Logs
------------

.. list-table::
 :header-rows: 1
 :widths: 35 65

 * - Codename
   - Descripcion
 * - ``view_technical_logs``
   - Visualiza logs tecnicos del sistema
 * - ``export_logs``
   - Exporta logs tecnicos del sistema

----

6. Catalogo Canonico de Grupos
================================

Catalogo completo de valores ``name`` del modelo
``FunctionGroup``.

.. list-table::
 :header-rows: 1
 :widths: 15 32 53

 * - ID
   - Nombre
   - Descripcion
 * - ``basic_operator_group``
   - Visualizacion basica del sistema
   -
 * - ``report_viewer_group``
   - Visualizacion completa de reportes
   -
 * - ``quality_supervisor_group``
   - Supervision de calidad de datos
   -
 * - ``data_exporter_group``
   - Exportacion de datos del sistema
   -
 * - ``alert_manager_group``
   - Gestion de alertas del sistema
   -
 * - ``user_admin_group``
   - Administracion de usuarios
   -
 * - ``permission_admin_group``
   - Administracion de permisos y asignaciones
   -
 * - ``auditor_group``
   - Acceso completo de auditoria
   -
 * - ``pipeline_admin_group``
   - Administracion del pipeline de datos
   -
 * - ``system_admin_group``
   - Administracion completa del sistema
   -

----

7. Catalogo Canonico de Reglas de Separacion
==============================================

Catalogo completo de valores ``name`` del modelo
``SeparationRule``.

.. list-table::
 :header-rows: 1
 :widths: 15 35 50

 * - ID
   - Nombre
   - Descripcion
 * - ``pipeline_audit_separation``
   - Separa administracion de pipeline de funciones de auditoria
   -
 * - ``user_audit_separation``
   - Separa administracion de usuarios de funciones de auditoria
   -
 * - ``access_audit_separation``
   - Separa administracion de accesos de funciones de auditoria
   -

----

8. Tabla de Transformaciones
==============================

Referencia rapida de patrones de traduccion espanol → ingles
aplicados en la correccion de ``MODELO_RBAC_IACT_v5.2.0``.

8.1 Verbos
----------

::

   gestiona_*          →  manage_*
   ve_*                →  view_*
   crea_*              →  create_*
   modifica_*          →  update_*
   elimina_*           →  delete_*
   busca_*             →  search_*
   bloquea_*           →  block_*
   desbloquea_*        →  unblock_*
   reactiva_*          →  reactivate_*
   asigna_*            →  assign_*
   revoca_*            →  revoke_*
   configura_*         →  configure_*
   pausa_*             →  pause_*
   solicita_*          →  request_*
   exporta_*           →  export_*
   filtra_*            →  filter_*
   genera_*            →  generate_*
   cierra_*            →  close_*
   resetea_*           →  reset_*
   lista_*             →  list_*

8.2 Sustantivos especificos
----------------------------

::

   graficos            →  charts        (NO graphics)
   auditoria           →  audit_log     (log explicito)
   etl / estado_etl    →  pipeline      (sin acronimo)
   separation of       →  separation    (forma corta inglesa)
   duties (legacy)
   agrupador           →  function_group

----

9. Reglas de Revision
======================

Todo artefacto del sistema — codigo, migracion, test, documento
— debe verificarse contra este vocabulario antes de ser
integrado. Las siguientes condiciones constituyen errores de
nivel CRITICO:

- Codename en espanol.
- Codename en kebab-case o camelCase.
- Uso de ``function_id`` como identificador de autorizacion
  en runtime.
- Prefijo redundante en nombre de grupo (``agr_``) o regla
  de separacion (``separation_``).
- Prefijo de acronimo en nombre de modulo Python (``rbac_``).
- Nombre de clase que describe mecanismo en lugar de dominio
  (``RBACBackend``, ``HasFunction``).
- Nombre abreviado no pronunciable (``Perm``).
- String literal de permiso fuera de ``FunctionCatalog``.
- ``app_label`` hardcodeado fuera de ``permissions/catalog.py``
  y ``permissions/backends.py``.

----

10. Historial de Versiones
============================

.. list-table::
 :header-rows: 1
 :widths: 12 15 73

 * - Version
   - Fecha
   - Cambios
 * - 1.0.0
   - 2026-01-13
   - Version inicial. Canoniza la regla fundamental
     (codigo en ingles, docs en espanol) y los catalogos
     de codenames, grupos y reglas de separacion corregidos en
     ``MODELO_RBAC_IACT_v5.2.1``.
 * - 2.0.0
   - 2026-05-04
   - Incorpora convenciones de nomenclatura para modulos
     y clases Python derivadas de CIA-RBAC-002. Agrega
     seccion 4 (Convenciones Python), seccion 8 (Tabla de
     Transformaciones) y seccion 9 (Reglas de Revision).
     Corrige metadata (clasificacion Alto → Critico).

----

11. Trazabilidad
================

.. list-table::
 :header-rows: 1
 :widths: 35 65

 * - Referencia
   - Path
 * - Analisis de errores que origino v1.0.0
   - :doc:`/gestion/evidencia/rbac-historia/analisis-errores-modelo-rbac-v5-2-0`
 * - CIA que origino v2.0.0
   - :doc:`/gestion/evidencia/rbac-arquitectura/cia-rbac-002-arquitectura-permisos-drf`
 * - ADR de autorizacion DRF
   - :doc:`/normativa/gobernanza/adr-gob-010-rbac-autorizacion-drf-backend`
 * - ADR de coexistencia ACC+PERM
   - :doc:`/normativa/gobernanza/adr-gob-008-rbac-coexistencia-acc-perm`
 * - Modelo de datos vigente
   - :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index` (v5.2.1)
