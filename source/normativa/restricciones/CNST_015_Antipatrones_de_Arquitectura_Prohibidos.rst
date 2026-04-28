.. meta::
   :artefacto: CNST_015
   :tipo: Restriccion
   :dominio: normativa
   :subdominio: restricciones
   :estado: Vigente
   :version: 1.0.0
   :fecha_creacion: 2025-12-17
   :ultimo_cambio: 2026-04-28
   :autor: NestorMonroy
   :clasificacion: Alto

.. _cnst-015:

=================================================
CNST-015: Antipatrones de Arquitectura Prohibidos
=================================================

Enunciado
---------

Los siguientes antipatrones estan PROHIBIDOS en el codebase del
sistema IACT. Su deteccion en code review obliga a refactor antes de
merge a ``main``.

Lista
-----

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Antipatron
     - Razon
   * - Fat Models
     - Modelos con >300 lineas o >15 metodos. Mover logica a service layer.
   * - Fat Views
     - Vistas con logica de negocio. Vistas son orquestadores delgados.
   * - God Object
     - Cualquier clase >500 lineas que abarca multiples dominios.
   * - Hardcoded Configuration
     - Valores de produccion en codigo. Usar ``settings`` o env vars.
   * - SQL Injection via Raw SQL
     - ``cursor.execute(f"...{user_input}...")``. Usar parametros.
   * - Sleep en Vistas
     - ``time.sleep`` en path de request.
   * - N+1 Queries
     - Sin ``select_related``/``prefetch_related`` cuando aplica.
   * - Catch Pokemon
     - ``except Exception: pass`` sin logging ni accion.

Verificacion
------------

- Linter custom + ``ruff`` con reglas activadas.
- Code review obligatorio en PR a ``main``.

Referencias cruzadas
--------------------

- :doc:`CNST_016_Principios_SOLID_Obligatorios`
