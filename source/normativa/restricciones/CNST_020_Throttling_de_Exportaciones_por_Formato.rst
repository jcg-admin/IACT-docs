.. meta::
 :artefacto: CNST_020
 :tipo: Restriccion
 :dominio: normativa
 :subdominio: restricciones
 :estado: Vigente
 :version: 2.0.0
 :fecha_creacion: 2025-12-17
 :ultimo_cambio: 2026-04-28
 :autor: NestorMonroy
 :clasificacion: Alto

.. _cnst-020:

=================================================
CNST-020: Throttling de Exportaciones por Formato
=================================================

Resumen Ejecutivo
-----------------

.. list-table::
 :widths: 30 70
 :header-rows: 0

 * - **ID**
   - CNST_020
 * - **Categoria**
   - Performance
 * - **Tipo (TXM_01)**
   - Tecnica
 * - **Criticidad**
   - Alto
 * - **Negociable**
   - No
 * - **Estado**
   - Vigente

1. Definicion
-------------

1.1 Enunciado
^^^^^^^^^^^^^


Las exportaciones DEBEN respetar limites cuantitativos por formato:
maximo de registros, cantidad maxima diaria por usuario y timeout de
procesamiento.

1.2 Justificacion
^^^^^^^^^^^^^^^^^


Previene scraping, controla uso de recursos y mantiene UX usable
(archivos mas grandes son inmanejables del lado cliente).

1.3 Origen
^^^^^^^^^^

- **Fuente:** Performance + control de uso de recursos
- **Documento:** RESTRICCIONES_COMPLETAS_DEL_SISTEMA_IACT.md:621-640
- **Fecha:** 2025-01-01

2. Especificacion Tecnica
-------------------------

2.1 Descripcion Detallada
^^^^^^^^^^^^^^^^^^^^^^^^^

(detalle en parametros)

2.2 Parametros
^^^^^^^^^^^^^^


.. list-table::
 :header-rows: 1
 :widths: 15 25 25 20 15

 * - Formato
   - Max registros
   - Max/dia/usuario
   - Timeout
   - Tamano aprox
 * - CSV
   - 100 000
   - 10
   - 60 s
   - 15-20 MB
 * - Excel
   - 50 000
   - 5
   - 90 s
   - 10-15 MB
 * - PDF
   - 10 000
   - 3
   - 120 s
   - 5-10 MB

2.3 Tecnologias Involucradas
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- DRF ScopedRateThrottle
- Limites por formato y por rol

3. Impacto en Sistema
---------------------

3.1 Modulos Afectados
^^^^^^^^^^^^^^^^^^^^^

.. list-table::
 :widths: 30 70
 :header-rows: 1

 * - Modulo
   - Impacto
 * - MOD_Reports
   - Aplica limites en export endpoints

3.2 Casos de Uso Afectados
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
 :widths: 30 70
 :header-rows: 1

 * - UC
   - Impacto
 * - UC_022
   - CSV: 100k/10per_dia/60s
 * - UC_023
   - Excel: 50k/5per_dia/90s
 * - UC_024
   - PDF: 10k/3per_dia/120s

3.3 Lo que NO se puede hacer
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Superar el max records por formato
- Exceder limites diarios por rol (BASICO 5, COORD 20)
- Ejecutar export con timeout > el de su formato

4. Business Rules Derivadas
---------------------------

.. list-table::
 :widths: 20 40 40
 :header-rows: 1

 * - BR
   - Nombre
   - Relacion
 * - BR_011 (legacy)
   - Limites de Exportacion
   - FND_00:298 — vinculo historico

5. Implementacion
-----------------

5.1 Codigo de Referencia
^^^^^^^^^^^^^^^^^^^^^^^^


.. code-block:: python

 limits = {"csv": 100_000, "xlsx": 50_000, "pdf": 10_000}
 assert export.records <= limits[export.format]

5.2 Validacion de Cumplimiento
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Ver seccion 5.1 (codigo de referencia es la validacion ejecutable).


6. Excepciones
--------------

6.1 Excepciones Permitidas
^^^^^^^^^^^^^^^^^^^^^^^^^^

- Rol ADMIN_ANALITICA puede tener limites superiores con justificacion

6.2 Proceso de Excepcion
^^^^^^^^^^^^^^^^^^^^^^^^

Limites por rol se configuran en settings, cambios requieren ADR.

El protocolo formal de waiver de CNSTs esta pendiente de elaborar en
el WP de gobernanza (`PROC_Excepciones_CNST` — ver
(referencia interna) § W-4).

7. Verificacion
---------------

7.1 Criterios de Cumplimiento
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

El cumplimiento se verifica via los snippets de la seccion 5.

7.2 Metodo de Verificacion
^^^^^^^^^^^^^^^^^^^^^^^^^^

- **Tipo:** Automatico
- **Frecuencia:** Continuo
- **Herramienta:** Tests que verifican respuesta 429 al exceder limites

8. Trazabilidad
---------------

.. list-table::
 :widths: 30 70
 :header-rows: 0

 * - **CNSTs relacionadas**
   - :doc:`CNST_019_Exportaciones_Asincronas_Sobre_10k_Registros`, :doc:`CNST_011_Throttling_Obligatorio_en_Endpoints_Publicos`
 * - **BR derivadas**
   - BR_011 (legacy)
 * - **UCs afectados**
   - UC_022, UC_023, UC_024
 * - **MODs afectados**
   - MOD_Reports
 * - **ADRs relacionados**
   - Pendiente WP arquitectura tecnica

9. Historial de Cambios
-----------------------

.. list-table::
 :widths: 12 15 25 48
 :header-rows: 1

 * - Version
   - Fecha
   - Autor
   - Cambios
 * - 1.0.0
   - 2025-12-17
   - NestorMonroy
   - Version inicial (consolidada del backup canonico)
 * - 2.0.0
   - 2026-04-28
   - NestorMonroy
   - Descomposicion SRP (un concern por archivo) + enriquecimiento estructura completa TPL_CNST (9 secciones)

