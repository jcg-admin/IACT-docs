.. _uc-inc-rpt-01-parte-06:

==========================================
Parte 6 — Requisitos no funcionales
==========================================

6.1 Performance
===============

.. list-table::
 :widths: 30 30 40
 :header-rows: 1

 * - Metrica
   - Target
   - Notas
 * - Latencia (cache hit)
   - ≤ 5 ms
   - Segmento cacheado por sesion
 * - Latencia (cache miss)
   - ≤ 50 ms
   - Consulta RBAC + mapeo DID
 * - Cache hit ratio
   - ≥ 90%
   - Se invalida solo en cambio de permisos

6.2 Seguridad
=============

- El resultado de la resolucion de segmento NUNCA
  se expone directamente al cliente. Se usa solo
  como filtro interno en el UC invocador.
- El log de auditoria registra cada resolucion de
  segmento (usuario, segmentos resueltos, timestamp).

6.3 Disponibilidad
==================

Este UC es una dependencia critica de todos los
reportes IVR. Su disponibilidad objetivo es ≥ 99.9%,
alineada con CNST-017 (SLA de reportes).

6.4 Escalabilidad
=================

El resultado de la resolucion debe ser cacheado por
sesion para evitar consultas repetidas al servicio
RBAC en cada solicitud de reporte del mismo usuario.
