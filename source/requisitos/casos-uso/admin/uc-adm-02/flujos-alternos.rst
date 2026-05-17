.. _uc-adm-02-parte-04:

==========================
Parte 4 — Flujos alternos
==========================

FA-01: Codename duplicado: 409 Conflict.
FA-02: Codename con caracteres invalidos
(no snake_case): 400.
FA-03: Module invalido: 400.
FA-04: Desactivar funcion con asignaciones
activas: advertencia en respuesta (202 +
warning list). Funcion se desactiva; asignaciones
existentes preservadas pero no renovables.
FA-05: Listar con filtro module/state:
paginacion + filtros aplicados.

Resumen
=======

.. list-table::
 :widths: 12 38 30 20

 * - FA
   - Disparador
   - Comportamiento
   - Notas
 * - FA-01
   - Codename duplicado
   - 409
   - unicidad
 * - FA-02
   - Formato invalido
   - 400
   - snake_case
 * - FA-03
   - Module invalido
   - 400
   - enum modulos
 * - FA-04
   - Asignaciones activas
   - 202 + warning
   - BR-009
 * - FA-05
   - Listado filtrado
   - 200 paginado
   - manage_function_catalog
