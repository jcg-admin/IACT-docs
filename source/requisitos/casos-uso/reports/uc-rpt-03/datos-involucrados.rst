.. _uc-rpt-03-parte-07:

================================
Parte 7 — Datos involucrados
================================

7.1 Entidades leidas
====================

- **Base Analitica IVR** — datos historicos de llamadas,
  centros de transferencia y menus IVR por trimestre,
  consultados via Servicio de Reportes.
- **SegmentoUsuario** — filtro de segmento aplicado por
  ``<<include>>`` UC_INC_RPT_01.

7.2 Datos del reporte historico
================================

El reporte historico cruza informacion de multiples Servicios
de Reportes. Los datos disponibles son los generados por
el ETL en la Base Analitica IVR:

::

   ReporteHistorico:
     trimestre            : codigo del trimestre
     segmento             : codigo de segmento
     total_llamadas       : total de llamadas del trimestre
     tasa_abandono        : calculada con los tres tipos de abandono
     centros_principales  : distribucion por centro de transferencia
     menus_frecuentes     : distribucion por menu IVR

Comparacion entre trimestres disponible cuando existan multiples
tablas fuente ``tbl_historico_tN_YYYY`` (estado futuro; actualmente
solo existe Q3 2025 — ver D-ETL-009).

7.3 Cache
=========

- key incluye ``trimestre`` + ``segments_hash``.
- TTL: 300s (datos historicos son inmutables post-ETL).
- No requiere invalidacion (datos de trimestres pasados
  no cambian tras el ETL).

7.4 Datos NO involucrados
==========================

- BD operativa (repositorio operacional — tablas de usuarios, RBAC).
- PII: numeros de telefono individuales.
- Audio / transcripciones.
- Datos de agentes o colas de call center.
