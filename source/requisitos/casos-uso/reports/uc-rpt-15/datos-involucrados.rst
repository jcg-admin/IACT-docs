.. _uc-rpt-15-parte-07:

================================
Parte 7 — Datos involucrados
================================

7.1 Entidades leidas
====================

- **BD_IVR (Base Analitica IVR legacy)** — esquema con
  ``base_ivr_detalle`` poblado por el ETL. Se accede via
  ``cursor.callproc(...)`` a DOS SPs (uno por dimension).

7.2 Datos retornados por los SPs
================================

UC_RPT_15 invoca dos SPs y combina sus result sets:

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
