.. meta::
 :artefacto: INDEX_UC_ADMIN
 :tipo: Indice
 :dominio: requisitos
 :subdominio: casos_uso/admin
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

====================================================
MOD_Admin — Administracion del Modelo RBAC (UCs)
====================================================

.. note:: Modulo NUEVO en RBAC v5.6.0

 MOD_Admin es uno de los **9 modulos in-scope** del modelo RBAC
 v5.6.0 (3 funciones: ``create_separation_rule``,
 ``manage_function_catalog``, ``assign_functions_to_group``).
 Formaliza el plano de configuracion RBAC que en versiones
 anteriores estaba implicito en MOD_Access y MOD_Permissions.
 Ver :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`.

Plano de configuracion del modelo RBAC: gestiona QUE funciones, grupos
del sistema y reglas SoD EXISTEN. Actor principal: ``system_admin``
(AGR-010 — ``system_admin_group``).
Ver :doc:`/arquitectura-tecnica/use-case-view/admin/index`.

Casos de Uso
------------

.. toctree::
 :maxdepth: 2

 uc-adm-01/index
 uc-adm-02/index
 uc-adm-03/index
