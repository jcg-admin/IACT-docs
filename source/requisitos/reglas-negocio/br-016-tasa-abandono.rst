.. meta::
 :artefacto: BR_016
 :tipo: Regla de Negocio
 :dominio: requisitos
 :subdominio: reglas_negocio
 :estado: Vigente
 :version: 2.0.0
 :fecha_creacion: 2026-04-29
 :ultimo_cambio: 2026-05-02
 :autor: NestorMonroy
 :clasificacion: Alto

.. _br-016:

========================
BR_016: Tasa de Abandono
========================

1. Definicion
-------------

La **Tasa de Abandono** mide el porcentaje de llamadas que el cliente
abandona antes de ser atendidas por un agente. Es uno de los KPI
principales del sistema IVR.

**Formula:**

.. code-block:: text

 tasa_abandono = (llamadas_abandonadas / llamadas_recibidas) * 100

Donde:

- ``llamadas_abandonadas``: llamadas en las que el cliente colgó
  antes de recibir atencion (ver seccion 5 para implementacion
  concreta en el sistema IVR IACT).
- ``llamadas_recibidas``: total de llamadas que entraron al IVR
  durante la ventana de medicion.

2. Tipo de regla
----------------

**Tipo:** Regla de Calculo (categorizada en
:doc:`/base-cognitiva/_fundamentos-conceptuales/fnd-05-jerarquia-4-niveles`).

Es una de las 3 BRs de tipo "Calculo" del catalogo IACT (junto con
BR_017 Tiempo Promedio Espera y BR_018 Indice Eficiencia).

3. Parametros
-------------

.. list-table::
 :header-rows: 1
 :widths: 30 70

 * - Parametro
   - Valor
 * - Ventana de medicion default
   - 24 horas (rolling)
 * - Ventana minima permitida
   - 1 hora
 * - Ventana maxima permitida
   - 2 anos (CNST_018 Rango Maximo de Consulta)
 * - Granularidad temporal
   - Hora, dia, semana, mes, trimestre
 * - Granularidad por dimension
   - Total, por segmento, por centro de transferencia

4. Umbrales operativos
----------------------

Los umbrales estan calibrados para el perfil de trafico real del
IVR IACT, donde un porcentaje estructural de llamadas abandona en
el menu IVR antes de transferirse a un agente.

.. list-table::
 :header-rows: 1
 :widths: 25 25 50

 * - Estado
   - Rango
   - Significado
 * - Optimo
   - < 20 %
   - Performance dentro del SLA del IVR IACT
 * - Aceptable
   - 20 % - 30 %
   - Monitoreo recomendado; revisar causas
 * - Critico
   - > 30 %
   - Requiere intervencion inmediata (alerta automatica)

.. note::

 Los umbrales 5%/10% son valores tipicos de call centers con alta
 tasa de resolucion en el menu IVR self-service. El IVR de IACT
 tiene un perfil distinto: el ~70-80% de llamadas navega
 exitosamente al menu y se transfiere; el porcentaje de abandono
 estructural observable es del orden del 20-30%. Los umbrales se
 definieron con los datos reales de Q3 2025.

Los umbrales son configurables via ``UC_ALR_01 Configurar Umbrales``.

5. Implementacion en el sistema IVR IACT
-----------------------------------------

El campo ``cMenu`` de la tabla fuente registra el ultimo menu al
que llego la llamada antes de finalizar. El SP de ETL normaliza
los valores vacios a ``'VACIO'``.

**Tres tipos de abandono reconocidos:**

.. list-table::
 :header-rows: 1
 :widths: 30 70

 * - Valor de ``menu``
   - Significado operativo
 * - ``'VACIO'``
   - La llamada nunca alcanzo un menu (``cMenu`` era NULL o vacio
     en la tabla fuente). El cliente colgó en la bienvenida o
     antes de llegar al arbol de opciones.
 * - ``'cliente_colgo'``
   - La llamada llego a un menu y el cliente colgó explicitamente
     sin elegir opcion de transferencia.
 * - ``'SinOpcion_Cabecera'``
   - La llamada llego al menu pero no se seleccionó ninguna opcion
     dentro del tiempo de espera de la cabecera.

**Filtro SQL de implementacion:**

.. note::

 Los detalles de implementacion de esta operacion estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.
**Volumenes de referencia (Q3 2025, Nacional A):**

- ``VACIO``: ~8-9% del total de llamadas.
- ``cliente_colgo``: ~18-19% del total de llamadas.
- ``SinOpcion_Cabecera``: ~1% del total de llamadas.
- **Total abandono**: ~27-28% del total de llamadas.

6. UCs relacionados
-------------------

- :doc:`/requisitos/casos-uso/reports/uc-rpt-02/index`
- :doc:`/requisitos/casos-uso/reports/uc-rpt-13/index`
- :doc:`/requisitos/casos-uso/alerts/uc-alr-01/index`

7. CNSTs aplicables
-------------------

- :doc:`/normativa/restricciones/cnst-017-sla-de-tiempos-de-respuesta`
  — calculo en runtime debe responder en SLA p95 <= 2 s.
- :doc:`/normativa/restricciones/cnst-018-rango-maximo-de-consulta-de-2-anos`
  — limite de ventana de medicion historica.

8. BRs relacionadas
-------------------

- BR_017 Tiempo Promedio Espera (otra metrica de calidad de servicio).
- BR_018 Indice Eficiencia (metrica complementaria).

9. Origen
---------

- **Fuente:** SLA de negocio del sistema IVR; datos reales Q3 2025.
- **Documento:** referenciado en
  :doc:`/base-cognitiva/_fundamentos-conceptuales/fnd-05-jerarquia-4-niveles`
  como ejemplo canonico de regla de calculo.
- **Fecha:** 2026-04-29 (creacion); 2026-05-02 (implementacion
  concreta y recalibracion de umbrales con datos reales Q3 2025).
