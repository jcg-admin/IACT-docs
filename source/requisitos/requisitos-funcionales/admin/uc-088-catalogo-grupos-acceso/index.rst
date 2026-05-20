.. meta::
 :artefacto: UC-088
 :tipo: Caso de Uso (spec-from-code, alias administrativo)
 :dominio: requisitos
 :subdominio: funcionales/admin
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-20
 :ultimo_cambio: 2026-05-20
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc-088:

==========================================
UC-088: Catalogo de Grupos de Acceso (AGR)
==========================================

.. list-table::
 :widths: 25 75

 * - **Marker codigo API**
   - ``UC_ADM_03``
 * - **Marker codigo UI**
   - ``UC_ADM_03``
 * - **Actor**
   - Administrador de seguridad
 * - **Modulo**
   - MOD_Admin

.. admonition:: Solape funcional con UC-016 / UC_PERM_05
   :class: note

   Este UC describe el **catalogo administrativo** de AGRs
   (listado completo + visualizacion de composicion) que la UI
   admin presenta. La operacion CRUD propia (crear / modificar /
   retirar) esta canonicamente en UC-016 (UC_PERM_05). El marker
   ``UC_ADM_03`` aparece en codigo donde el componente UI consume
   el catalogo en el modulo admin (``AGRCatalog.jsx``,
   ``AGRComposition.test.jsx``). Las dos entradas se mantienen
   por trazabilidad de markers; las reglas de negocio son las
   de UC-016.

FR derivados
============

.. toctree::
 :hidden:
 :maxdepth: 1

 fr-088-01-listar-catalogo-agr
