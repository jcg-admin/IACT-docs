.. _uc-rpt-17-parte-07:

================================
Parte 7 — Datos involucrados
================================

7.1 Entidades leidas
====================

- **Base Analitica IVR** — dimension de clientes IVR,
  generada por el ETL desde ``tbl_historico_*`` y consultada
  via Servicio de Reportes.

7.2 Datos retornados por el Servicio de Reportes
=================================================

**Clientes IVR** (``sp_rpt_clientes``):

::

   ReporteClientes:
     telefono_hashed  : identificador anonimizado del caller
                        (derivado de cTelefono_Origen via hash)
     segmento         : codigo de segmento
     total_llamadas   : veces que este caller contacto el IVR
     primera_llamada  : fecha de la primera llamada del trimestre
     ultima_llamada   : fecha de la ultima llamada del trimestre
     trimestre        : codigo del trimestre

7.3 Privacidad de datos
========================

El campo ``cTelefono_Origen`` de la tabla fuente contiene el
numero de telefono del llamante (PII). El ETL no almacena el
numero en claro en ``base_ivr_clientes`` — aplica un hash
unidireccional para anonimizar el identificador del cliente.

El reporte expone solo ``telefono_hashed``. El numero raw
NUNCA se expone en ninguna vista o API (CNST-007 + CNST-001).

7.4 Datos NO involucrados
==========================

- Numero de telefono raw (PII).
- Datos de identidad del caller.
- Audio / transcripciones.

7.5 Filtros aplicables
=======================

- Por segmento (filtro de perfil de usuario via UC_INC_RPT_01).
- Por trimestre.
