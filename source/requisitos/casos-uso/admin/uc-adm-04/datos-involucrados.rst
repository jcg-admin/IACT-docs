.. meta::
 :artefacto: UC_ADM_04_DATOS
 :tipo: Caso de Uso (seccion)
 :dominio: requisitos
 :subdominio: casos_uso/admin
 :estado: Borrador
 :version: 1.0.0

==========================
7. Datos Involucrados
==========================

7.1 Entidad principal: MenuItem
===============================

.. list-table::
 :widths: 25 20 55
 :header-rows: 1

 * - Campo
   - Tipo
   - Descripcion
 * - ``id``
   - PK auto
   - Clave primaria
 * - ``function_id``
   - FK Function (1:1)
   - OneToOneField, on_delete=PROTECT (I-1, I-2)
 * - ``display_label``
   - varchar(100)
   - Etiqueta visible al user
 * - ``icon``
   - varchar(100)
   - Identificador de icono frontend
 * - ``display_order``
   - int
   - Orden visual (asc)
 * - ``route_path``
   - varchar(200)
   - Ruta frontend que el item navega
 * - ``parent_id``
   - FK MenuItem (self)
   - Override visual de jerarquia (no permisos)
 * - ``status``
   - choice
   - DRAFT / ACTIVE / DEPRECATED / ARCHIVED
 * - ``deprecated_at``
   - datetime null
   - Marca temporal de transicion a DEPRECATED
 * - ``archived_at``
   - datetime null
   - Marca temporal de transicion a ARCHIVED
 * - ``block_auto_archive``
   - bool
   - Si True, sobrevive auto-archive a 90d
 * - ``block_reason``
   - varchar(500)
   - Justificacion (>= 20 chars si block=True)
 * - ``block_set_by``
   - FK User
   - Quien activo el flag block
 * - ``block_set_at``
   - datetime null
   - Cuando se activo el flag block
 * - ``created_at``
   - datetime
   - auto_now_add
 * - ``updated_at``
   - datetime
   - auto_now
 * - ``created_by``
   - FK User
   - Quien creo el item

7.2 Entidades relacionadas
==========================

- **Function** (UC_ADM_03): catalogo RBAC v5.6.0. UC_ADM_04
  consume registros existentes via FK.
- **AuditEvent**: cada operacion genera entrada (BR-AUDIT-01).
- **AccessGroup** + **FunctionGroupMembership**: lectura
  para identificar users afectados al invalidar cache.

7.3 Origen de los datos
=======================

- ``Function`` proviene del bootstrap RBAC v5.6.0 (data
  migration canonica — ADR-BACK-007 §3.2).
- ``MenuItem`` se crea via UC_ADM_04 o data migration
  inicial.
- ``parent_id`` no existe en bootstrap inicial — todos los
  items son top-level por default.

7.4 Indices
===========

3 indices sobre ``menu_items`` (Phase 5 strategy P3):

- ``status``
- ``(status, display_order)``
- ``deprecated_at``

7.5 Datos NO involucrados
=========================

- **AccessGroup composition** — UC_ADM_04 no modifica AGRs
  (eso es UC_PERM_06).
- **User assignments** — UC_ADM_04 no asigna users a AGRs
  (eso es UC_PERM_05).
- **Function.is_critical** — UC_ADM_04 no modifica el flag
  (solo via data migration — ADR-BACK-010).
