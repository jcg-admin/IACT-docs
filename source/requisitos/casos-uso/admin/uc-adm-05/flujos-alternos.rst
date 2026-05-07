.. meta::
 :artefacto: UC_ADM_05_ALT
 :tipo: Caso de Uso (seccion)
 :dominio: requisitos
 :subdominio: casos_uso/admin
 :estado: Borrador
 :version: 1.0.0

=========================
4. Flujos Alternos
=========================

4.1 FA-01: ACTIVE → DEPRECATED (deprecar)
=========================================

::

   PASO 1   Invoker selecciona "Marcar como Deprecado"  (Interfaz de Usuario)
   PASO 2   Confirma                                     (Interfaz de Usuario)
   PASO 3   POST .../deprecate/                          (Interfaz de Usuario → Servicio de Aplicacion)
   PASO 4-7 Identicos al flujo principal salvo
            target=DEPRECATED                            (Servicio de Aplicacion)
   PASO 8   UPDATE status='DEPRECATED', deprecated_at=now() (Servicio de Aplicacion → Almacen de Datos)
   PASO 9-12 Audit + COMMIT + invalidacion + 200 OK     (resto del flujo)

**Postcondiciones especiales:**

- Item visible en endpoint con flag
  ``status="DEPRECATED"``.
- Frontend muestra etiqueta "(legacy)".
- Cuenta del Planificador de Tareas para auto-archive
  empieza desde ``deprecated_at``.

4.2 FA-02: DEPRECATED → ACTIVE (reactivar desde deprecated)
===========================================================

::

   POST .../reactivate/

**UPDATE en PASO 8:**

::

   UPDATE menu_items SET
       status='ACTIVE',
       deprecated_at=NULL,
       block_auto_archive=False,
       block_reason='',
       block_set_by=NULL,
       block_set_at=NULL
   WHERE id=?

**Audit event:** ``LIFECYCLE_TRANSITION`` con
``before_status=DEPRECATED``, ``after_status=ACTIVE``,
``flag_block_cleared=True`` (si aplicaba).

4.3 FA-03: DEPRECATED → ARCHIVED (archivado manual)
===================================================

::

   POST .../archive/

**Pre-validacion:** invoker debe confirmar con dialog
"¿Archivar item? Quedara fuera del menu de los users".

**UPDATE en PASO 8:**

::

   UPDATE menu_items SET
       status='ARCHIVED',
       archived_at=now(),
       block_auto_archive=False,
       block_reason='',
       block_set_by=NULL,
       block_set_at=NULL
   WHERE id=?

(``deprecated_at`` se preserva — auditabilidad de cuanto
estuvo en DEPRECATED.)

**Postcondiciones especiales:**

- Item invisible en endpoint
  ``GET /api/v1/menu/`` (incluso para users con la
  capability — CNST-032 v2.0.0 §1.1 BR-MENU-04).
- Capability subyacente sigue accesible via URL directa
  (defense-in-depth en endpoint).

4.4 FA-04: Auto-archive del Planificador de Tareas
==================================================

Ejecutado por la identidad de sistema (no invoker
humano).

::

   PASO 1   Planificador de Tareas dispara job diario   (Planificador)
   PASO 2   Query items DEPRECATED con
            deprecated_at < now() - 90d AND
            block_auto_archive=False                    (Planificador → Almacen de Datos)
   PASO 3   Por cada item: ejecutar transicion
            DEPRECATED → ARCHIVED (FA-03 con
            actor='system')                             (Servicio de Aplicacion)
   PASO 4   Audit event LIFECYCLE_AUTO_ARCHIVED         (Servicio de Aplicacion → Almacen de Datos)
   PASO 5   Notificacion al system_admin con resumen    (Servicio de Notificacion)

**Concurrencia:** la transicion usa lock optimista. Si un
admin reactiva el item entre el query y el UPDATE, el
auto-archive falla silenciosamente con log (caso raro).

**Pre-archive notification a 80d:**

::

   PASO 1   Job diario detecta items con
            deprecated_at < now() - 80d AND
            deprecated_at >= now() - 90d AND
            block_auto_archive=False                    (Planificador → Almacen de Datos)
   PASO 2   Notificacion a system_admin:
            "auto-archive en 10 dias salvo
             que active block_auto_archive"             (Servicio de Notificacion)
   PASO 3   Sin cambios en DB                            (no hay UPDATE en este job)

4.5 FA-05: Activar block_auto_archive
=====================================

::

   POST .../{id}/block-archive/
   { "block_reason": "Auditoria pendiente Q3" }

**Validaciones:**

- ``status == DEPRECATED`` (no aplica en otros estados).
- ``block_reason`` ≥ 20 caracteres.

**UPDATE en PASO 8:**

::

   UPDATE menu_items SET
       block_auto_archive=True,
       block_reason='Auditoria pendiente Q3...',
       block_set_by=invoker.id,
       block_set_at=now()
   WHERE id=? AND status='DEPRECATED'

**Audit event:** ``MENU_ITEM_BLOCK_FLAG_SET`` con
``actor_id``, ``block_reason``, ``timestamp``.

4.6 FA-06: Desactivar block_auto_archive
========================================

::

   DELETE .../{id}/block-archive/

**Validacion:** ``block_auto_archive == True``.

**UPDATE:**

::

   UPDATE menu_items SET
       block_auto_archive=False,
       block_reason='',
       block_set_by=NULL,
       block_set_at=NULL
   WHERE id=?

**Audit event:** ``MENU_ITEM_BLOCK_FLAG_CLEARED``.

**Notas:** desactivar el flag NO archiva inmediatamente.
El item queda en DEPRECATED sujeto al auto-archive
normal cuando ``deprecated_at < now() - 90d``.

4.7 FA-07: Reactivar desde ARCHIVED
===================================

::

   POST .../{id}/reactivate/

**Pre-validacion:** invoker confirma con dialog
"¿Reactivar item archivado? Volvera a ser visible".

**UPDATE:** identico a FA-02 pero limpia tambien
``archived_at=NULL``.

**Audit event:** ``LIFECYCLE_TRANSITION`` con
``before_status=ARCHIVED``, ``after_status=ACTIVE``.

**Notas:** el item recupera su ``display_order`` y
``parent`` previos (nunca fueron borrados — solo
ocultos).
