.. meta::
 :artefacto: INDEX_UC_SUPERVISION
 :tipo: Indice
 :dominio: requisitos
 :subdominio: casos_uso/supervision
 :estado: Reservado
 :version: 1.1.0
 :fecha_creacion: 2026-05-01
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy

==========================================================
MOD_Supervision — Supervision Live (Supervisor User View)
==========================================================

.. warning:: Modulo reservado (out-of-scope para v5.6.0)

 MOD_Supervision es un **extension point open-closed** del modelo
 RBAC v5.6.0: declarado en el catalogo (3 funciones,
 ``supervision:monitor``, ``supervision:barge_in``,
 ``supervision:broadcast``) pero **out-of-scope para esta
 release**. La documentacion de UC_SUP_01..03 se preserva como
 base para activacion futura, NO como especificacion
 implementable en v5.6.0.

 SUP-001 (monitor_live_calls) y SUP-002 (barge_in_calls) requieren
 ademas tono de supervision por compliance — diseño de la senal
 audible queda dentro de la especificacion del extension point.

 Modelo activo de v5.6.0: 9 modulos / 64 funciones (ver
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`).
 Catalogo total declarado: 77 funciones (64 activas + 13
 reservadas en MOD_Operator y MOD_Supervision).

Casos de Uso
------------

.. toctree::
 :maxdepth: 1

 uc-sup-01/index
 uc-sup-02/index
 uc-sup-03/index
