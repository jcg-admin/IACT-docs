.. _uc-rpt-13-parte-07:

================================
Parte 7 — Datos involucrados
================================

7.1 Entidades leidas
====================

- **Base Analitica IVR** — datos de llamadas abandonadas
  por segmento, generados por el ETL y consultados via
  Servicio de Reportes.

7.2 Datos retornados por el Servicio de Reportes
=================================================

El Servicio de Reportes (``sp_rpt_llamadas_abandonadas``)
retorna para el trimestre indicado:

::

   ReporteAbandono:
     segmento         : codigo de segmento (nacional_A, etc.)
     total_llamadas   : total de llamadas recibidas
     abandonadas_vacio          : llamadas con menu='VACIO'
     abandonadas_cliente_colgo  : llamadas con menu='cliente_colgo'
     abandonadas_sin_opcion     : menu='SinOpcion_Cabecera'
     total_abandonadas          : suma de los tres tipos
     tasa_abandono              : (total_abandonadas / total_llamadas) * 100

Ver BR_016 para la definicion completa de tipos de abandono
y umbrales operativos.

7.3 Datos NO involucrados
==========================

- PII del caller.
- Audio / transcripciones.
- Datos de agentes individuales (el IVR no tiene agentes).

7.4 Filtros aplicables
=======================

- Por segmento (``nacional_A``, ``nacional_B``, ``Puebla``).
- Por trimestre (``Q3_25``, etc.).
- El filtro de segmento aplica CNST-008: el usuario solo
  ve los segmentos de su perfil (``<<include>>`` UC_INC_RPT_01).
