.. _uc-rpt-01-parte-07:

================================
Parte 7 — Datos involucrados
================================

7.1 Entidades leidas
====================

- **Base Analitica IVR** — datos de llamadas por segmento,
  trimestre y centro de transferencia, generados por el ETL
  y consultados via Servicio de Reportes.
- **SegmentoUsuario** — filtro de segmento aplicado por
  ``<<include>>`` UC_INC_RPT_01.

7.2 Datos del dashboard IVR
============================

El dashboard IVR agrega informacion de los Servicios de
Reportes disponibles. Los KPIs principales son:

::

   DashboardIVR:
     segmentos_activos   : lista de segmentos del usuario
     trimestre_activo    : codigo del trimestre con datos
     total_llamadas      : suma de llamadas recibidas
     total_abandonadas   : suma de los tres tipos de abandono
     tasa_abandono       : (total_abandonadas / total) * 100
     centros_principales : top N centros de transferencia

Todos los valores se calculan sobre la Base Analitica IVR
para el trimestre y segmento activos del usuario.

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
