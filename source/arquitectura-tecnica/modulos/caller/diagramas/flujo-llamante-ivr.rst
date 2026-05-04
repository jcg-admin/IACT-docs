.. meta::
 :artefacto: ARQ_MOD_011_DIAG_FLUJO_LLAMANTE
 :tipo: Diagrama Arquitectonico — Comportamiento de Modulo
 :dominio: arquitectura_tecnica
 :subdominio: modulos/caller/diagramas
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _arq_mod_011_flujo_llamante_ivr:

============================
Flujo del Llamante en el IVR
============================

Flujo del Llamante en el IVR
==============================

.. uml::
 :caption: Flujo del Caller — llamada entrante, navegacion, cola y CSAT.

 @startuml

 start

 :Caller marca numero IVR;
 :Sistema IVR contesta\n(UC_CLI_01 — tbl_historico_detalle INSERT);

 :Navegar menu IVR\n(UC_CLI_02 — tbl_historico_detalle UPDATE menu_seleccion);

 if (Agente disponible?) then (si)
   :Conectar con agente\n(answer_inbound_calls);
   :Atencion de llamada;
   :Ofrecer encuesta CSAT\n(UC_CLI_05);
   :Registrar respuesta CSAT\n(tbl_historico_detalle.csat);
   stop
 else (no disponible)
   :Encolar llamada\n(UC_CLI_03 — estado=en_cola);
   if (Tiempo espera > umbral?) then (si)
     :Caller cuelga\n(tasa abandono para BR-016);
     :INSERT abandon en tbl_historico_detalle;
     stop
   else (espera aceptable)
     :Ofrecer callback\n(UC_CLI_04);
     if (Caller acepta callback?) then (si)
       :Registrar callback pendiente;
       :Sistema devuelve llamada automaticamente;
       :Conectar con agente;
       stop
     else (no)
       :Continuar espera en cola;
       stop
     endif
   endif
 endif

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modulos/caller/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
