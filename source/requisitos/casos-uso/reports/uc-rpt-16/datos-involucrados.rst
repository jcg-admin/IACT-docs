.. _uc-rpt-16-parte-07:

================================
Parte 7 — Datos involucrados
================================

7.1 Entidades leidas
====================

- **BD_IVR (Base Analitica IVR legacy)** — esquema con
  ``base_ivr_detalle`` poblado por el ETL. Se accede via
  ``cursor.callproc(...)`` a TRES SPs (uno por sub-vista).

7.2 Datos retornados por los SPs
================================

UC_RPT_16 invoca uno de tres SPs segun la ``vista``
solicitada:

**Menus redirigidos** (``sp_rpt_menu_redirigidos``):

::

   ReporteMenuRedirigidos:
     menu             : valor del campo menu (cMenu normalizado)
     total_llamadas   : llamadas que llegaron a este menu
     trimestre        : codigo del trimestre

**Menu por centro** (``sp_rpt_menu_centro``):

::

   ReporteMenuCentro:
     menu             : menu IVR
     centro           : centro de transferencia destino
     total            : llamadas en ese cruce menu x centro

**Errores de menu** (``sp_rpt_cMENU_ERROR``):

::

   ReporteMenuError:
     menu             : valor del campo menu con estado error
     segmento         : codigo de segmento
     total            : ocurrencias del error
     trimestre        : codigo del trimestre

7.3 Datos NO involucrados
==========================

- PII del caller (cTelefono_Origen no se expone en reportes).
- Audio / DTMF raw.

7.4 Centinelas de menu
=======================

El campo ``menu`` en la Base Analitica IVR contiene:

- Nombre literal del menu (valor de cMenu del IVR).
- ``'VACIO'`` — llamada que no llego a ningun menu
  (cMenu era NULL o vacio en la fuente).

Ver :doc:`/requisitos/reglas-negocio/br-016-tasa-abandono`
para los tres tipos de abandono relacionados con este campo.
