.. meta::
 :artefacto: UC_ADM_04_ACTORES
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
   - ``manage_menu_catalog``
 * - **AGR titular**
   - AGR-010 (``system_admin``)
 * - **is_critical**
   - True (cache bypass — ADR-BACK-010)

2.2 Actores secundarios
=======================

- **Servicio de Aplicacion:** valida invariantes,
  persiste cambios.
- **Almacen de Datos:** persiste ``MenuItem``.
- **Servicio de Cache:** invalidacion explicita
  post-COMMIT (afecta ``menu:user:{id}`` de todos los users
  con la capability — ver flujo principal §6).
- **Servicio de Audit Log:** registra cada cambio.

2.3 Precondiciones
==================

(P1) El invoker esta autenticado y su sesion vigente.

(P2) El invoker tiene la capability
``manage_menu_catalog`` (verificada con bypass de cache —
AP-2b).

(P3) Existe la ``Function`` que sera wrapper. Si no existe,
el flujo redirige a UC_ADM_03 (gestion del catalogo de
Function).

(P4) Si se especifica ``parent``, existe el ``MenuItem``
parent y NO esta en estado ARCHIVED.

2.4 Postcondiciones (exito)
===========================

(Q1) El ``MenuItem`` creado / modificado existe en el
catalogo con los campos solicitados.

(Q2) Audit log contiene entrada con
``actor_id``, ``timestamp``, ``operation`` (CREATE / UPDATE),
``before_state``, ``after_state``.

(Q3) Cache de ``menu:user:{id}`` invalidado para todos los
users con la capability subyacente.

(Q4) Si la operacion fue CREATE, el ``MenuItem`` queda en
``status=DRAFT`` (default) — visible solo en preview
admin hasta transicion ACTIVE (UC_ADM_05).

2.5 Postcondiciones (falla)
===========================

- Ningun cambio persistido (transaccion atomica con
  rollback).
- Audit log NO recibe entrada (la transaccion no
  commiteo).
- Cache no invalidado.
