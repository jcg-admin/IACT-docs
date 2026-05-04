.. meta::
 :artefacto: AT_PERSPECTIVA_AVAILABILITY
 :tipo: Perspectiva Arquitectonica — Availability and Resilience
 :dominio: arquitectura_tecnica
 :subdominio: Perspectivas
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at-perspectiva-availability:

======================================
Perspectiva Availability y Resilience
======================================

Analisis transversal de la propiedad de calidad **disponibilidad y resiliencia**
en el sistema IACT. El sistema soporta operaciones de accion ciudadana territorial
— la indisponibilidad tiene impacto directo en campo.

El riesgo principal no es la caida del servidor de aplicacion, sino el fallo
del pipeline ETL cuando la BD Operativa IVR no esta disponible o sus datos
contienen errores. La arquitectura aisle este fallo por diseno (P-04).

Aplicacion a vistas
=====================

Vista Functional (Use Case View)
------------------------------------

Las operaciones del sistema se clasifican por su dependencia del ETL y del IVR.

.. list-table::
 :header-rows: 1
 :widths: 35 65

 * - Grupo de operaciones
   - Disponibilidad
 * - **Consulta de datos IACT**
   - Siempre disponibles mientras la BD propia (PostgreSQL) este activa.
     No dependen del IVR ni del estado del ETL.
 * - **Dashboard y reportes**
   - Disponibles con los datos del ultimo ETL exitoso. Si el ETL falla,
     se muestran datos del run anterior — no hay degradacion funcional.
 * - **Alertas y notificaciones**
   - Disponibles sobre los datos existentes. Nuevas alertas se generan
     en el siguiente ETL exitoso.
 * - **Pipeline ETL**
   - Dependiente de la BD Operativa IVR. Si el IVR no esta disponible,
     el pipeline falla y registra ``ETLEjecucion.estado = fallido``.
     P-04: el fallo no corrompe datos existentes ni bloquea operaciones.
 * - **Administracion RBAC**
   - Independiente del IVR. Siempre disponible mientras la BD propia
     este activa.

Vista Process View (Concurrency)
-----------------------------------

El pipeline ETL se ejecuta como proceso aislado con estado propio.

.. list-table::
 :header-rows: 1
 :widths: 30 70

 * - Patron de resiliencia
   - Descripcion
 * - **Aislamiento de fallos**
   - P-04: el fallo del ETL no corrompe datos existentes ni bloquea
     operaciones del sistema. La aplicacion continua sirviendo los
     ultimos datos validos.
 * - **Estado explicito**
   - ``ETLEjecucion.estado`` es la fuente de verdad del pipeline:
     ``en_ejecucion``, ``exitoso``, ``fallido``. AGR_OPERADOR puede
     consultar el estado en tiempo real.
 * - **Retry manual**
   - AGR_OPERADOR puede solicitar retry del pipeline (``request_pipeline_retry``)
     tras diagnosticar y resolver la causa del fallo.
 * - **Siguiente disparo automatico**
   - Un fallo no bloquea el siguiente disparo APScheduler. El sistema
     intenta el proximo run segun el horario configurado.

Vista Deployment (+1)
-----------------------

La disponibilidad del sistema esta determinada por la disponibilidad de
sus componentes fisicos.

.. list-table::
 :header-rows: 1
 :widths: 30 70

 * - Componente
   - Impacto en disponibilidad
 * - **Servidor de aplicacion (DRF)**
   - Punto unico critico en la variante deploy-estandar. Las variantes
     deploy-auth-cache y deploy-etl separan el worker ETL, reduciendo
     la carga del servidor principal.
 * - **PostgreSQL (BD propia)**
   - Perdida de BD propia = sistema completamente inoperativo.
     Requiere respaldo periodico y plan de recovery.
 * - **MariaDB IVR (BD Operativa)**
   - Solo afecta al pipeline ETL. Si el IVR no esta disponible, el
     ETL falla (P-04) pero el resto del sistema continua operando.
 * - **APScheduler**
   - Embebido en el proceso Django. Si el proceso se reinicia, el
     scheduler se reinicia automaticamente con el siguiente arrange.
     No persiste estado entre reinicios.

Vista Operational
-------------------

Los procedimientos operacionales implementan la respuesta ante fallos.

.. uml::
 :caption: Figura — Estados de disponibilidad del sistema IACT

 @startuml

 skinparam state {
   BackgroundColor White
   BorderColor #333333
 }
 skinparam ArrowColor #444444
 skinparam shadowing false

 [*] --> Operativo : despliegue exitoso

 Operativo --> DegradadoETL : IVR no disponible\no error en datos
 DegradadoETL --> Operativo : IVR restaurado\no retry exitoso

 Operativo --> InoperativoApp : fallo servidor\no BD propia caida
 InoperativoApp --> Operativo : recovery servidor\ny BD propia

 DegradadoETL : Datos IACT accesibles\nETL en estado fallido\nUltimos datos validos visibles

 note right of DegradadoETL
   P-04: fallo ETL no
   bloquea operaciones
   de consulta ni RBAC.
 end note

 @enduml

Procedimiento de recovery
===========================

.. list-table::
 :header-rows: 1
 :widths: 25 75

 * - Escenario
   - Procedimiento
 * - **ETL falla por IVR no disponible**
   - Verificar disponibilidad de BD Operativa IVR.
     Escalar a Ops/DBA si IVR esta caido.
     Solicitar retry cuando IVR este disponible.
     Ver :doc:`/arquitectura-tecnica/operational-view/system-support`.
 * - **ETL falla por datos invalidos**
   - Revisar ``ETLLog`` (``view_etl_logs``, campo ``mensaje_error``).
     Corregir parametros ETL si es necesario. Solicitar retry.
 * - **BD propia (PostgreSQL) no disponible**
   - Sistema completamente inoperativo. Recovery desde respaldo.
     Ejecutar migraciones si es necesario tras recovery.
     Ver :doc:`/arquitectura-tecnica/operational-view/system-installation`.
 * - **Proceso Django caido**
   - Reiniciar proceso (APScheduler se restaura automaticamente).
     Verificar ``ApplicationLog`` y ``SystemHealth`` tras reinicio.

Restricciones y principios
============================

.. list-table::
 :header-rows: 1
 :widths: 15 85

 * - Ref
   - Descripcion
 * - **P-04**
   - El fallo del ETL no corrompe datos existentes ni bloquea
     operaciones del sistema. Aislamiento de fallos por diseno.
 * - **P-01**
   - El sistema IACT nunca escribe en la BD Operativa IVR. La
     indisponibilidad del IVR no puede causar perdida de datos
     en IACT — solo impide actualizar datos de llamadas.
 * - **CNST-008**
   - Ventana de ejecucion ETL: 6-12 horas. El pipeline no es
     un proceso de tiempo real — un fallo temporal no tiene
     impacto critico inmediato en la operacion del sistema.

.. seealso::

 :doc:`/arquitectura-tecnica/process-view/index`
 :doc:`/arquitectura-tecnica/deploy-view/index`
 :doc:`/arquitectura-tecnica/operational-view/system-support`
 :doc:`/arquitectura-tecnica/operational-view/system-installation`
 :doc:`/base-cognitiva/_uml/uml-14-uml-vistas-arquitectonicas/perspectivas-arquitectonicas`
