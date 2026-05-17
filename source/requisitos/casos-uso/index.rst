.. meta::
 :artefacto: INDEX_CASOS_USO
 :tipo: Indice
 :dominio: requisitos
 :subdominio: casos_uso
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-04-29
 :ultimo_cambio: 2026-04-29
 :autor: NestorMonroy
 :clasificacion: Interno

============
Casos de Uso
============

Catalogo de Casos de Uso del sistema IACT v4.0.0 organizado en 13 modulos
funcionales. La decision arquitectonica de coexistencia ACC ↔ PERM
(Hipotesis 1 aprobada) se materializa en los modulos MOD_Access (vista
funcional) y MOD_Permissions (vista tecnica granular). MOD_Admin (nuevo
v5.6.0) cubre el plano de configuracion del modelo RBAC.

Modulos
-------

.. toctree::
 :maxdepth: 2

 auth/index
 users/index
 access/index
 permissions/index
 admin/index
 reports/index
 alerts/index
 pipeline/index
 audit/index
 logs/index
 operator/index
 supervision/index
 caller/index
