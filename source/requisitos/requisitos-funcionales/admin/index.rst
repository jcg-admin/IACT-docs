Requisitos Funcionales - Admin
==============================

Casos de uso del modulo Admin — catalogos canonicos (CRUD/listado)
de entidades RBAC y MenuItems administradas por roles
administrativos. Distinto a las operaciones de **asignacion** que
viven en ``access/`` y ``permissions/``.

.. admonition:: Origen — spec-from-code
   :class: note

   Estos UCs fueron documentados retroactivamente (2026-05-20)
   por la iniciativa ``documentar-uc-adm-01-05``. La spec deriva
   del comportamiento real implementado en IACT-api +
   IACT-ui, no de un documento de requisitos previo. La
   nomenclatura ``UC_ADM_NN`` se conserva tal cual aparece en
   markers de codigo para facilitar trazabilidad inversa.

   Cuando exista solape con un UC del dominio ``access/`` o
   ``permissions/``, esta carpeta lo indica explicitamente en
   el ``index.rst`` del UC.

.. toctree::
 :hidden:
 :maxdepth: 1

 uc-086-catalogo-reglas-separacion-funciones/index
 uc-087-catalogo-funciones-rbac/index
 uc-088-catalogo-grupos-acceso/index
 uc-089-catalogo-menu-items/index
 uc-090-ciclo-vida-menu-items/index
