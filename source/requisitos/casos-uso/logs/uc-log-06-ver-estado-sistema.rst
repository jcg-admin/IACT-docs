.. meta::
 :artefacto: UC_LOG_06
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

================================================
UC_LOG_06: Ver Estado de Salud del Sistema
================================================

.. note::

 Caso de uso nuevo en v5.4.0. Cubre health endpoints y estado
 puntual de servicios externos (UP/DOWN/DEGRADED). NO es un log
 de eventos secuenciales — es estado puntual del sistema.
 Función dedicada LOG-006 ``view_system_health``.

 Trazabilidad: gap UC_081 declarado en ARQ-MOD-008 sin función
 RBAC backing. Decision D-05 (WP rbac-modelo-conceptual-cleanup).

1. Resumen
----------

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **ID**
   - UC_LOG_06
 * - **Nombre**
   - Ver Estado de Salud del Sistema
 * - **Actor Principal**
   - AGR-010: ``system_admin_group`` (sysadmin)
 * - **Modulo**
   - MOD_Logs (módulo SYS_LOGS técnico)
 * - **Funcion RBAC**
   - LOG-006 ``view_system_health`` (NUEVA v5.4.0 — gap UC_081)
 * - **Prioridad**
   - Alta
 * - **Complejidad**
   - Baja
 * - **BReq Origen**
   - BRQ-LOG-006

2. Descripcion
--------------

Este caso de uso permite consultar el estado actual de salud del
sistema IACT y sus dependencias externas. Provee visibilidad NOC
sobre componentes operativos.

**Estados posibles por componente:**

- **UP**: operativo y respondiendo en SLA.
- **DEGRADED**: respondiendo pero con latencia elevada o errores intermitentes.
- **DOWN**: no responde o respondiendo con error.

**Componentes monitoreados:**

- Aplicación IACT (Django + DRF).
- BD IVR (lectura, CNST-007).
- BD Analytics.
- Buzón interno (CNST-002).
- Cola de exports (CNST-019).
- Caché (Redis u otro, según ADR de implementación).

**Diferencia con uc-log-05 (logs de infraestructura):**

- uc-log-05: secuencia temporal de eventos (DOWN ocurrió a las
  10:23, UP recovered a las 10:28).
- uc-log-06: estado puntual ahora (¿está UP en este momento?).

3. Diagrama de Caso de Uso
--------------------------

.. uml::
 :caption: Diagrama de Caso de Uso - UC_LOG_06

 @startuml
 left to right direction
 actor "AGR-010\nsystem_admin_group" as USER

 rectangle "MOD_Logs" {
 usecase "UC_LOG_06\nVer Estado Sistema" as UC06
 usecase "Consultar\nApp" as APP
 usecase "Consultar\nBDs" as BD
 usecase "Consultar\nCola" as COLA
 usecase "Consultar\nBuzón" as BUZ
 }

 USER --> UC06
 UC06 --> APP : include
 UC06 --> BD : include
 UC06 --> COLA : include
 UC06 --> BUZ : include
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
   - Usuario tiene sesión activa con función LOG-006.
 * - PRE-02
   - Health endpoints expuestos por componentes monitoreados.

4.2 Trigger
^^^^^^^^^^^

El sysadmin accede al panel de salud del sistema.

4.3 Postcondiciones
^^^^^^^^^^^^^^^^^^^

.. list-table::
 :widths: 10 90
 :header-rows: 1

 * - ID
   - Postcondicion
 * - POST-01
   - Se muestra el estado actual de cada componente monitoreado.

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
   - Accede al panel de salud.
 * - 2
   - Sistema
   - Valida función LOG-006.
 * - 3
   - Sistema
   - Consulta health endpoints de cada componente.
 * - 4
   - Sistema
   - Agrega estados con timestamp del último check.
 * - 5
   - Sistema
   - Muestra panel con indicadores visuales (verde/amarillo/rojo).
 * - 6
   - Sistema
   - Auto-refresca cada N segundos (configurable).

6. Excepciones
--------------

6.1 EX-01: Sin Permiso LOG-006
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Usuario sin función LOG-006 → rechazo con error LOG-060.

6.2 EX-02: Health Endpoint No Responde
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Si un componente no responde al health check, mostrar como DOWN
con timestamp del último check exitoso.

7. Reglas de Negocio
--------------------

.. list-table::
 :widths: 15 35 50
 :header-rows: 1

 * - ID
   - Regla
   - Descripción
 * - BR-LOG-60
   - Estados canónicos
   - Tres estados únicos: UP, DEGRADED, DOWN
 * - BR-LOG-61
   - Auto-refresh
   - Panel se actualiza periódicamente
 * - BR-LOG-62
   - Last check
   - Cada componente muestra timestamp del último check exitoso

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
   - Acceso al panel se registra (informativo, sin metadata sensible)

9. Trazabilidad
---------------

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **BReq Origen**
   - BRQ-LOG-006 (gap UC_081 ARQ-MOD-008)
 * - **Funcion RBAC**
   - LOG-006 ``view_system_health`` (NUEVA v5.4.0)
 * - **UC Relacionados**
   - uc-log-05 (logs infra), uc-log-07 (métricas técnicas)
 * - **Clase de Dominio**
   - ``SystemHealth`` (primaria; D-05: snapshot, no es log) (per :doc:`/arquitectura-tecnica/modelo-dominio-iact` v1.0.0)

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
   - Versión inicial. Caso de uso nuevo en v5.4.0 — cubre gap UC_081 declarado en ARQ-MOD-008 sin función RBAC backing. Decision D-05.
