.. meta::
 :artefacto: UC_ADM_05_ACTORES
 :tipo: Caso de Uso (seccion)
 :dominio: requisitos
 :subdominio: casos_uso/admin
 :estado: Borrador
 :version: 1.0.0

================================
2. Actores y Precondiciones
================================

2.1 Actor primario
==================

.. list-table::
 :widths: 30 70
 :header-rows: 0

 * - **Codename**
   - ``manage_menu_lifecycle``
 * - **AGR titular**
   - AGR-010 (``system_admin``)
 * - **is_critical**
   - True (cache bypass — ADR-BACK-010)

2.2 Actores secundarios
=======================

- **Servicio de Aplicacion:** valida transiciones, persiste.
- **Almacen de Datos:** persiste cambios de ``status``.
- **Servicio de Cache:** invalidacion explicita post-COMMIT.
- **Servicio de Audit Log:** registra cada transicion.
- **Planificador de Tareas:** actor del flujo de
  auto-archive (FA-04).
- **Servicio de Notificacion (mailbox interno):** entrega
  warnings y critical alerts al system_admin.

2.3 Precondiciones
==================

(P1) Invoker autenticado con sesion vigente (excepto FA-04
que es ejecutado por el Planificador de Tareas con identidad
de sistema).

(P2) Invoker tiene ``manage_menu_lifecycle`` (verificada
con bypass de cache — AP-2b).

(P3) ``MenuItem`` objetivo existe.

(P4) La transicion solicitada es valida segun la maquina
de estados.

2.4 Postcondiciones (exito)
===========================

(Q1) ``MenuItem.status`` actualizado al estado destino.

(Q2) Si la transicion fue ACTIVE → DEPRECATED:
``deprecated_at = now()``.

(Q3) Si la transicion fue DEPRECATED → ARCHIVED:
``archived_at = now()``; ``deprecated_at`` preservado.

(Q4) Si la transicion fue cualquier_estado → ACTIVE:
``deprecated_at`` y ``archived_at`` se limpian a NULL;
``block_auto_archive`` se limpia a False y ``block_reason``
queda vacio.

(Q5) Audit log con evento
``MENU_ITEM_LIFECYCLE_TRANSITION`` con
``before_status``, ``after_status``,
``deprecated_at``, ``archived_at``.

(Q6) Cache de menu invalidado para users afectados.

2.5 Postcondiciones (falla)
===========================

- Sin cambios persistidos (transaccion atomica).
- Sin audit event.
- Sin invalidacion de cache.
