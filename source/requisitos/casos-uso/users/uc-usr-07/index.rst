.. meta::
 :artefacto: UC_USR_07
 :tipo: Caso de Uso (stub Reservado)
 :dominio: requisitos
 :subdominio: casos_uso/users
 :estado: Reservado
 :version: 0.1.0
 :fecha_creacion: 2026-05-07
 :ultimo_cambio: 2026-05-07
 :autor: NestorMonroy
 :clasificacion: Interno
 :origen: incierto — referenciado en users/uc-usr-02
          sin decision arquitectonica formal documentada

.. _uc-usr-07:

==============================================
UC_USR_07 — Editar Perfil Propio (RESERVADO)
==============================================

.. warning:: **UC en estado Reservado — sin spec completa**

   Aparece referenciado en:

   - ``users/uc-usr-02/informacion-general.rst:73`` —
     "UC_USR_07 (perfil propio, separado)".

   La referencia distingue entre:

   - UC_USR_02: edicion de usuarios por admin
     (capability ``edit_users``).
   - UC_USR_07: edicion del perfil propio del usuario
     autenticado (capability self-served, sin RBAC
     administrativo).

   La investigacion del WP
   ``2026-05-07-04-08-13-use-case-view-analysis`` confirma
   que nunca existio commit de creacion de este UC.

   Estado **Reservado** hasta que el ejecutor confirme su
   alcance.

Resumen propuesto
=================

UC_USR_07 permitiria al usuario autenticado editar su
**propio perfil** (campos como nombre completo, email
secundario, preferencias de UI, locale) sin requerir
capability administrativa. La capability seria
self-served (auto-otorgada al autenticarse, similar a
``view_own_state``).

**No incluye:**

- Cambio de password (UC_AUTH_03 / UC_AUTH_04).
- Cambio de username (potencial impacto en audit log;
  decision separada).
- Cambio de ``segment_id`` (BR-012 — permanente, no
  switchable).
- Cambio de AGRs / capabilities (UC_PERM_01..06).

Trazabilidad
============

.. list-table::
 :widths: 30 70
 :header-rows: 0

 * - **ID**
   - UC_USR_07
 * - **Nombre propuesto**
   - Editar Perfil Propio
 * - **Modulo**
   - MOD_Users
 * - **Capability propuesta**
   - ``edit_own_profile`` (no existe en catalogo;
     candidata a ser self-served como ``view_own_*``)
 * - **Estado**
   - **Reservado**
 * - **Diferencia con UC_USR_02**
   - UC_USR_02 = admin edita usuarios (RBAC
     ``edit_users``). UC_USR_07 = usuario edita su
     propio perfil (sin RBAC admin).

Decision pendiente
==================

Antes de promover, ADR debe definir:

1. ¿Que campos son editables por el propio usuario vs cuales
   requieren admin?
2. ¿La capability es self-served o requiere asignacion
   explicita?
3. Auditabilidad: ¿toda edicion del perfil propio genera
   audit event?
