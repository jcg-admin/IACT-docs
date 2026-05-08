.. meta::
 :artefacto: UC_ADM_04_PAT
 :tipo: Caso de Uso (seccion)
 :dominio: requisitos
 :subdominio: casos_uso/admin
 :estado: Borrador
 :version: 1.0.0

==============================
10. Patrones de Diseno
==============================

10.1 Wrapper UX over Authorization Source (AP-1)
================================================

``MenuItem`` envuelve a ``Function`` sin ser fuente de
capability. Una sola direccion: UX depende de auth, auth
nunca depende de UX.

Beneficio: cualquier capability puede tener wrapper UX o
no — la regla de acceso vive siempre en ``Function``.

10.2 Capability bypass para writes criticos (AP-2b)
===================================================

``manage_menu_catalog.is_critical=True``. La verificacion
consulta el Almacen de Datos sin pasar por el servicio de
cache. Strong consistency en cada request administrativo.

Trade-off: latencia adicional por request. Aceptado por la
naturaleza administrativa del UC (baja frecuencia, alto
riesgo).

10.3 Eventual consistency con escape hatch (AP-3)
=================================================

UC continua si el servicio de cache falla durante
invalidacion (degraded mode). El estado del Almacen de
Datos es la fuente de verdad. La telemetria explicita
permite intervencion oportuna.

Frente al patron classic "two-phase commit con cache",
UC_ADM_04 prefiere availability del UC sobre consistency
estricta del cache.

10.4 Audit log append-only
==========================

Cada operacion mutating registra entrada inmutable. Audit
log no permite UPDATE ni DELETE (constraint a nivel de
modelo). Retencion ≥ 7 anos.

Frente al patron classic "soft delete + audit table",
UC_ADM_04 prefiere audit log dedicado y normalizado.

10.5 Bulk operation con UPDATE multi-row
========================================

FA-05 (bulk reorder) usa UPDATE con CASE WHEN para
actualizar N items en una sola query. Patron preferido a
N transacciones individuales.

::

   UPDATE menu_items
      SET display_order = CASE id
            WHEN ? THEN ?
            WHEN ? THEN ?
          END
    WHERE id IN (?, ?);

Beneficio: 1 row-lock vs N row-locks; 1 entrada audit
agregada.

10.6 Verificacion de jerarquia DAG (no ciclos)
==============================================

FA-03 valida que ``parent`` no introduzca ciclos via
traversal. Patron classic "topological check antes de
INSERT/UPDATE".

Implementacion: recorrer ``parent_id`` recursivamente desde
el item modificado, verificar que no llegue al item mismo.

10.7 Pattern reference (relacionados)
=====================================

- UC_PERM_06 (asignar Function a AccessGroup) — mismo
  patron de invalidacion de cache post-COMMIT.
- UC_ADM_03 (gestion de Function) — predecesor logico
  (debe existir Function antes de UC_ADM_04).
- UC_ADM_05 (lifecycle MenuItem) — sucesor logico (despues
  de DRAFT, transicionar a ACTIVE).
