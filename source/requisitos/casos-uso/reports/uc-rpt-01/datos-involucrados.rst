.. _uc-rpt-01-parte-07:

================================
Parte 7 — Datos involucrados
================================

7.1 Entidades leidas
====================

- **BD_IVR (Base Analitica IVR legacy)** — esquema con
  ``base_ivr_detalle`` poblado por el ETL. Se accede
  exclusivamente via ``cursor.callproc('sp_rpt_centros_
  xsegmento', [period, segments])``; el SP entrega filas
  pre-agregadas por segmento, trimestre y centro de
  transferencia.
- **SegmentoUsuario** — filtro de segmento aplicado por
  ``<<include>>`` UC_INC_RPT_01; los segmentos se pasan
  como parametro al SP.

7.2 Datos del dashboard IVR
============================

El dashboard IVR consume las filas pre-agregadas que retorna
``sp_rpt_centros_xsegmento`` desde BD_IVR. Los KPIs
principales (calculados por el SP, no por el backend) son:

::

   DashboardIVR:
     segmentos_activos   : lista de segmentos del usuario
     trimestre_activo    : codigo del trimestre con datos
     total_llamadas      : suma de llamadas recibidas
     total_abandonadas   : suma de los tres tipos de abandono
     tasa_abandono       : (total_abandonadas / total) * 100
     centros_principales : top N centros de transferencia

Todos los valores los calcula el SP en BD_IVR para el
trimestre y segmento activos del usuario; el backend solo
parsea las filas y arma el JSON de respuesta.

7.3 Cache
=========

::

   key = "dashboard:" + user_id + ":"
                      + trimestre + ":"
                      + segments_hash
   ttl: 30s

El cache se invalida al completar una ejecucion ETL exitosa
(``pipeline_runs.estado = 'exitoso'``).

7.4 Datos NO involucrados
==========================

- PII: numeros de telefono de callers individuales.
- Audio / transcripciones.
- Datos de agentes (el IVR no tiene datos de atencion humana
  directa — solo transferencias al centro).
