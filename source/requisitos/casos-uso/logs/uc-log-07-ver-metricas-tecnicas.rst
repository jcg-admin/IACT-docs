.. meta::
 :artefacto: UC_LOG_07
 :tipo: Caso de Uso
 :dominio: requisitos
 :subdominio: logs
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-04-30
 :ultimo_cambio: 2026-04-30
 :autor: NestorMonroy
 :clasificacion: Interno
 :normativa: CNST_025

============================================
UC_LOG_07: Ver Métricas Técnicas Agregadas
============================================

.. note::

 Caso de uso nuevo en v5.4.0. Cubre métricas técnicas agregadas
 (CPU, memoria, latencia, throughput). NO es un log de eventos
 ni estado puntual — son agregaciones temporales (ventanas
 móviles). Función dedicada LOG-007 ``view_technical_metrics``.

 Trazabilidad: gap UC_083 declarado en ARQ-MOD-008 sin función
 RBAC backing. Decision D-05 (WP rbac-modelo-conceptual-cleanup).

1. Resumen
----------

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **ID**
   - UC_LOG_07
 * - **Nombre**
   - Ver Métricas Técnicas Agregadas
 * - **Actor Principal**
   - AGR-010: ``system_admin_group`` (sysadmin)
 * - **Modulo**
   - MOD_Logs (módulo SYS_LOGS técnico)
 * - **Funcion RBAC**
   - LOG-007 ``view_technical_metrics`` (NUEVA v5.4.0 — gap UC_083)
 * - **Prioridad**
   - Alta
 * - **Complejidad**
   - Media
 * - **BReq Origen**
   - BRQ-LOG-007

2. Descripcion
--------------

Este caso de uso permite al sysadmin consultar métricas técnicas
agregadas del sistema IACT en ventanas temporales: utilización
de recursos, performance de endpoints, comportamiento de la cola
de exports, etc.

**Métricas típicas:**

- CPU% promedio / P95 / P99 por nodo.
- Memoria% promedio / pico por nodo.
- Latencia de endpoints HTTP (P50 / P95 / P99) por ruta.
- Throughput de la cola de exports (jobs/min).
- Cache hit rate.
- Tasa de errores 5xx.
- Tiempo medio de respuesta del ETL.

**Diferencias con UCs hermanos:**

- uc-log-01 (app logs): eventos secuenciales (errores 500).
- uc-log-05 (logs infra): eventos infra (timeouts, restarts).
- uc-log-06 (health): estado puntual (UP/DOWN).
- uc-log-07 (métricas): **agregaciones temporales** sobre ventanas.

3. Diagrama de Caso de Uso
--------------------------

.. uml::
 :caption: Diagrama de Caso de Uso - UC_LOG_07

 @startuml
 left to right direction
 actor "AGR-010\nsystem_admin_group" as USER

 rectangle "MOD_Logs" {
 usecase "UC_LOG_07\nVer Métricas" as UC07
 usecase "Seleccionar\nVentana" as VEN
 usecase "Seleccionar\nMétricas" as MET
 usecase "Visualizar\nGráfico" as GR
 }

 USER --> UC07
 UC07 --> VEN : include
 UC07 --> MET : include
 UC07 --> GR : extend
 @enduml

4. Contexto de Ejecucion
------------------------

4.1 Precondiciones
^^^^^^^^^^^^^^^^^^

.. list-table::
 :widths: 10 90
 :header-rows: 1

 * - ID
   - Precondicion
 * - PRE-01
   - Usuario tiene sesión activa con función LOG-007.
 * - PRE-02
   - Sistema de telemetría agregando métricas.

4.2 Trigger
^^^^^^^^^^^

El sysadmin accede al panel de métricas técnicas.

4.3 Postcondiciones
^^^^^^^^^^^^^^^^^^^

.. list-table::
 :widths: 10 90
 :header-rows: 1

 * - ID
   - Postcondicion
 * - POST-01
   - Se muestran las métricas seleccionadas en la ventana temporal indicada.

5. Flujo Normal
---------------

.. list-table::
 :widths: 10 20 70
 :header-rows: 1

 * - Paso
   - Actor
   - Acción
 * - 1
   - Usuario
   - Accede al panel de métricas técnicas.
 * - 2
   - Sistema
   - Valida función LOG-007.
 * - 3
   - Usuario
   - Selecciona ventana temporal (última hora / día / semana).
 * - 4
   - Usuario
   - Selecciona métricas a visualizar.
 * - 5
   - Sistema
   - Consulta métricas agregadas del backend de telemetría.
 * - 6
   - Sistema
   - Renderiza gráficos de tendencia.

6. Excepciones
--------------

6.1 EX-01: Sin Permiso LOG-007
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Usuario sin función LOG-007 → rechazo con error LOG-070.

6.2 EX-02: Backend de Telemetría No Disponible
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Si el backend de telemetría no responde, mostrar último snapshot
disponible con timestamp.

7. Reglas de Negocio
--------------------

.. list-table::
 :widths: 15 35 50
 :header-rows: 1

 * - ID
   - Regla
   - Descripción
 * - BR-LOG-70
   - Agregaciones temporales
   - Métricas son agregadas sobre ventanas (no eventos individuales)
 * - BR-LOG-71
   - Percentiles
   - Latencias siempre con P50/P95/P99 disponibles
 * - BR-LOG-72
   - Sin PII
   - Métricas no contienen información de usuario individual

8. Restricciones de Arquitectura
--------------------------------

.. list-table::
 :widths: 15 25 60
 :header-rows: 1

 * - CNST
   - Nombre
   - Aplicación
 * - CNST_025
   - Auditoría
   - Acceso al panel se registra
 * - CNST_026
   - Sin PII
   - Métricas son agregadas, NO contienen IDs de usuario

9. Trazabilidad
---------------

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **BReq Origen**
   - BRQ-LOG-007 (gap UC_083 ARQ-MOD-008)
 * - **Funcion RBAC**
   - LOG-007 ``view_technical_metrics`` (NUEVA v5.4.0)
 * - **UC Relacionados**
   - uc-log-05 (logs infra), uc-log-06 (health)
 * - **Clase de Dominio**
   - ``TechnicalMetric`` (primaria; D-05: agregacion, distinta de Metric de negocio) (per :doc:`/arquitectura-tecnica/modelo-dominio-iact` v1.0.0)

10. Historial de Cambios
------------------------

.. list-table::
 :widths: 15 15 70
 :header-rows: 1

 * - Versión
   - Fecha
   - Cambios
 * - 1.0.0
   - 2026-04-30
   - Versión inicial. Caso de uso nuevo en v5.4.0 — cubre gap UC_083 declarado en ARQ-MOD-008. Decision D-05.
