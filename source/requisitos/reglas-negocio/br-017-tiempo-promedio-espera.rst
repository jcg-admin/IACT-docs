.. meta::
 :artefacto: BR_017
 :tipo: Regla de Negocio
 :dominio: requisitos
 :subdominio: reglas_negocio
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-01-07
 :ultimo_cambio: 2026-01-07
 :autor: Equipo IACT
 :clasificacion: Interno

.. _br-017:

=================================
BR_017: Tiempo Promedio de Espera
=================================


Resumen Ejecutivo
-----------------

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **ID**
   - BR_017
 * - **Nombre**
   - Tiempo Promedio de Espera
 * - **Tipo**
   - Cálculo
 * - **Categoría**
   - KPI / Métricas Operacionales
 * - **Criticidad**
   - Alta
 * - **Estado**
   - Vigente

----

1. Definición Formal
--------------------

1.1 Enunciado de la Regla
^^^^^^^^^^^^^^^^^^^^^^^^^

.. note:: **Regla de Negocio BR_017**

 El Tiempo Promedio de Espera (TPE) se calcula como el promedio de segundos
 que los clientes esperan en cola antes de ser atendidos por un agente,
 en un período determinado.

1.2 Fórmula de Cálculo
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

 TPE = Σ(Tiempo_Espera_Individual) / Total_Llamadas_Atendidas

 Donde:
 - Tiempo_Espera_Individual: Segundos desde entrada a cola hasta atención
 - Total_Llamadas_Atendidas: Llamadas que fueron efectivamente atendidas

 Unidad: Segundos (con 2 decimales)

1.3 Formulación SBVR
^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

 VOCABULARIO:
 - tiempo_espera: Duración en segundos desde entrada a cola hasta atención
 - llamada_atendida: Llamada que fue contestada por un agente
 - tpe: Tiempo Promedio de Espera calculado
 - periodo: Rango de tiempo para el cálculo

 REGLA DE CÁLCULO:
 tpe ES IGUAL A 
 PROMEDIO(tiempo_espera) DE llamadas_atendidas EN periodo
 
 El resultado DEBE expresarse en segundos con 2 decimales.
 
 Llamadas abandonadas NO SE INCLUYEN en el cálculo de TPE.

1.4 Justificación
^^^^^^^^^^^^^^^^^

El TPE es un KPI crítico porque:

- **Experiencia del cliente**: Mide frustración por espera
- **Eficiencia operacional**: Indica capacidad del call center
- **Dimensionamiento**: Ayuda a planificar turnos de agentes
- **SLA contractual**: Métrica común en acuerdos de servicio

----

2. Clasificación
----------------

2.1 Tipo de Regla
^^^^^^^^^^^^^^^^^

.. list-table::
 :widths: 20 80
 :header-rows: 0

 * - **Tipo**
   - **Cálculo**
 * - 
   - [X] **Cálculo**: Define fórmula matemática para derivar valor

2.2 Naturaleza
^^^^^^^^^^^^^^

- **Estática/Dinámica**: Estática - fórmula fija
- **Automatizable**: Sí - calculada por ETL
- **Alcance**: MOD_Reports, MOD_Alerts

----

3. Aplicación en Sistema
------------------------

3.1 Donde Aplica
^^^^^^^^^^^^^^^^

.. list-table::
 :widths: 30 70
 :header-rows: 1

 * - Componente
   - Descripción de Aplicación
 * - Dashboard Principal
   - KPI destacado junto a tasa de abandono
 * - Gráfico por Hora
   - Tendencia de TPE durante el día
 * - Reportes
   - Comparativo por centro y período
 * - Alertas
   - Umbral de alerta si > 120 segundos

3.2 Umbrales de Referencia
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
 :widths: 20 30 50
 :header-rows: 1

 * - Rango
   - Clasificación
   - Acción
 * - 0 - 30 seg
   - Excelente
   - Ninguna
 * - 30 - 60 seg
   - Bueno
   - Monitorear
 * - 60 - 120 seg
   - Aceptable
   - Revisar capacidad
 * - > 120 seg
   - Crítico
   - Alerta BR_014

----

4. Implementación Técnica
-------------------------

4.1 SQL de Cálculo
^^^^^^^^^^^^^^^^^^

.. note::

 Los detalles de implementacion de esta regla estan delegados
 al documento tecnico de la capa de persistencia y servicio.
 Esta especificacion describe el QUE y el POR QUE, no el COMO.

4.2 Modelo de datos
^^^^^^^^^^^^^^^^^^^

.. note::

 Los detalles de implementacion de esta regla estan delegados
 al documento tecnico de la capa de persistencia y servicio.
 Esta especificacion describe el QUE y el POR QUE, no el COMO.

----

5. Trazabilidad
---------------

- **Origen**: BReq_RPT_Reporteria
- **UC Relacionados**: UC_RPT_01, UC_RPT_04, UC_RPT_07
- **BR Relacionada**: BR_014 (alerta si excede umbral)

----

6. Historial de Cambios
-----------------------

.. list-table::
 :widths: 15 15 70
 :header-rows: 1

 * - Versión
   - Fecha
   - Descripción del Cambio
 * - 1.0.0
   - 2026-01-07
   - Versión inicial

----

*Documento versión 1.0.0 - Proyecto IACT Dashboard Analytics*
