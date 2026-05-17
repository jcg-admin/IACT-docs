.. meta::
 :artefacto: INDEX_UC_SUPERVISION
 :tipo: Indice
 :dominio: requisitos
 :subdominio: casos_uso/supervision
 :estado: Fuera del scope
 :version: 1.2.0
 :fecha_creacion: 2026-05-01
 :ultimo_cambio: 2026-05-07
 :autor: NestorMonroy

==========================================================
MOD_Supervision — Supervision Live (Supervisor User View)
==========================================================

.. warning:: **Cluster fuera del scope del proyecto IACT**

 MOD_Supervision es un **extension point open-closed** del modelo
 RBAC v5.6.0: declarado en el catalogo (3 funciones,
 ``supervision:monitor``, ``supervision:barge_in``,
 ``supervision:broadcast``) pero **fuera del scope del proyecto**.
 La documentacion de UC_SUP_01..03 se preserva como base para
 activacion futura, NO como especificacion implementable. Sus
 diagramas NO estan sujetos al ciclo de normalizacion STD-012
 v1.1.0 (WP ``2026-05-07-04-50-49-std-012-prefix-normalization``).

 SUP-001 (monitor_live_calls) y SUP-002 (barge_in_calls) requieren
 ademas tono de supervision por compliance — diseño de la senal
 audible queda dentro de la especificacion del extension point.

 Modelo activo de v5.6.x: 67 funciones in-scope (catalogo
 declara 80 con 13 reservadas en MOD_Operator y
 MOD_Supervision). Ver
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`.

Casos de Uso
------------

.. toctree::
 :maxdepth: 1

 uc-sup-01/index
 uc-sup-02/index
 uc-sup-03/index
