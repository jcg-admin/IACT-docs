.. meta::
 :artefacto: ARQ_MOD_008_DIAG_FLUJO_HEALTH
 :tipo: Diagrama Arquitectonico — Comportamiento de Modulo
 :dominio: arquitectura_tecnica
 :subdominio: modulos/logs/diagramas
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _arq_mod_008_flujo_health_check:

======================
Flujo del Health Check
======================

.. uml::
 :caption: Flujo del health check del sistema — recoleccion de metricas y evaluacion de umbrales.

 @startuml

 start

 :Inicio de ciclo de health check\n(APScheduler — intervalo periodico);

 :Recolectar metricas del sistema\n(CPU, memoria, disco, conexiones BD);

 :Recolectar estado de servicios\n(Almacen de Datos, PostgreSQL, ETL, cola async);

 :Comparar valores contra umbrales\nconfigurables (view_system_health);

 if (Algun umbral violado?) then (si)
   :Registrar SystemHealth\ncon estado DEGRADADO;
   :Notificar a modulo de alertas\n(generar alerta automatica);
   stop
 else (todos OK)
   :Registrar SystemHealth\ncon estado OK;
   stop
 endif

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modulos/logs/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
