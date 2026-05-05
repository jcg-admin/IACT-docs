.. _uc-rpt-15-parte-07:

================================
Parte 7 — Datos involucrados
================================

7.1 Entidades leidas
====================

- **Base Analitica IVR** — datos de llamadas por centro de
  transferencia y segmento, generados por el ETL y consultados
  via Servicio de Reportes.

7.2 Datos retornados por el Servicio de Reportes
=================================================

El Servicio de Reportes provee dos dimensiones de analisis:

**Por centro de transferencia** (``sp_rpt_centros_transferencia``):

::

   ReporteCentros:
     centro_transferencia : valor de cDID_Centro_Transferencia
     segmento             : codigo de segmento
     total_llamadas       : total transferidas al centro
     trimestre            : codigo del trimestre

**Por segmento** (``sp_rpt_centros_xsegmento``):

::

   ReporteCentrosSegmento:
     segmento         : codigo de segmento
     centro           : centro de transferencia
     total            : llamadas en ese cruce

7.3 Datos NO involucrados
==========================

- PII del caller.
- Tiempos de agente (el IVR no tiene datos de atencion).
- Audio / transcripciones.

7.4 Filtros aplicables
=======================

- Por segmento (filtro de perfil de usuario via UC_INC_RPT_01).
- Por trimestre.
- Por centro de transferencia (opcional).
