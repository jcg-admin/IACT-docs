.. _uc-inc-rpt-01-parte-10:

==========================
Parte 10 — Patrones
==========================

10.1 Patrones aplicados
=======================

.. list-table::
 :widths: 18 32 50
 :header-rows: 1

 * - Patron
   - Nombre
   - Aplicacion
 * - **P-15**
   - RBAC granular
   - Acceso controlado por DIDs asignados
     al usuario via grupos de funciones
 * - **P-20**
   - Include UC
   - Logica reutilizable invocada por
     UC_RPT_01..17 sin duplicar codigo
 * - **P-31**
   - Cache by session
   - El segmento resuelto se cachea para
     evitar consultas RBAC repetidas
 * - **P-42**
   - Fail-fast
   - EX-02 y EX-03 detienen el flujo
     inmediatamente — ningun reporte debe
     mostrar datos sin segmento validado

10.2 Anti-patrones evitados
============================

- **Sin filtro global**: nunca retornar todos
  los datos y filtrar en el cliente. El filtro
  por segmento se aplica en la capa de servicio.
- **Sin hardcodeo de segmentos**: el mapeo
  DID→segmento vive en tabla configurable,
  no en codigo fuente.
