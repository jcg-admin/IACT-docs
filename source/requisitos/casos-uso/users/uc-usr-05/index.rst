.. meta::
 :artefacto: UC_USR_05
 :tipo: Caso de Uso (stub Reservado)
 :dominio: requisitos
 :subdominio: casos_uso/users
 :estado: Reservado
 :version: 0.1.0
 :fecha_creacion: 2026-05-07
 :ultimo_cambio: 2026-05-07
 :autor: NestorMonroy
 :clasificacion: Interno
 :origen: incierto — referenciado en uc-auth-03/04/05
          sin decision arquitectonica formal documentada

.. _uc-usr-05:

==============================================
UC_USR_05 — Bloquear Usuario (RESERVADO)
==============================================

.. warning:: **UC en estado Reservado — sin spec completa**

   Este UC esta declarado como **planificado** pero no
   tiene spec formal. Aparece referenciado en:

   - ``auth/uc-auth-03/flujos-alternos.rst:14`` — "el User
     existe pero ``state='BLOCKED'`` (UC_USR_05 lo bloqueo)".
   - ``auth/uc-auth-04/flujos-alternos.rst:97`` — "(UC_USR_06)
     el User ya tenga contrasena".
   - ``auth/uc-auth-05/informacion-general.rst:75,109`` —
     "UC_USR_05 (bloquear usuario)".

   La investigacion del WP
   ``2026-05-07-04-08-13-use-case-view-analysis`` confirma
   que **nunca existio commit de creacion** de este UC. Las
   referencias asumen su existencia pero la decision
   arquitectonica formal sobre su scope, capability RBAC y
   relacion con BR-015 (Bloqueo Intentos Fallidos) no esta
   documentada.

   Estado **Reservado** hasta que el ejecutor confirme:

   - El alcance del UC (¿bloqueo administrativo manual?
     ¿bloqueo automatico por intentos fallidos? ¿ambos?).
   - La capability RBAC asociada (sugerencia: ``block_users``
     o ``deactivate_users``).
   - El AGR titular (sugerencia: AGR-002 user_admin).
   - Si la funcionalidad actualmente vive en BR-015 +
     ``deactivate_users`` y este UC es redundante.

Resumen propuesto
=================

UC_USR_05 administraria el bloqueo manual de usuarios por
parte de un admin (distinto del bloqueo automatico de
BR-015 por intentos fallidos). El bloqueo es una transicion
``state: ACTIVE -> BLOCKED`` que impide login pero preserva
la cuenta para auditoria y posible reactivacion (UC_USR_06).

Trazabilidad
============

.. list-table::
 :widths: 30 70
 :header-rows: 0

 * - **ID**
   - UC_USR_05
 * - **Nombre propuesto**
   - Bloquear Usuario
 * - **Modulo**
   - MOD_Users
 * - **Capability propuesta**
   - ``block_users`` (no existe en catalogo) o
     ``deactivate_users`` (existe — soft delete BR-009)
 * - **Estado**
   - **Reservado** (origen incierto)
 * - **BR relacionada**
   - BR-015 (Bloqueo Intentos Fallidos) — semantica
     diferente, automatica por sistema vs manual por admin
 * - **UCs que lo referencian**
   - UC_AUTH_03, UC_AUTH_04, UC_AUTH_05, UC_PERM_07,
     UC_PERM_09

Decision pendiente
==================

Antes de promover este UC a Borrador / Vigente, requiere
ADR explicito que defina:

1. ¿Es necesario un UC separado o la funcionalidad ya
   esta cubierta por ``deactivate_users`` (UC_USR_03)?
2. Si separado, ¿cual es la capability RBAC (nueva o
   existente)?
3. ¿Que relacion tiene con BR-015 (bloqueo automatico)?

Mientras el ADR no exista, las referencias en otros UCs
deben tratarse como **referencias a funcionalidad
planificada** (no a UC documentado).
