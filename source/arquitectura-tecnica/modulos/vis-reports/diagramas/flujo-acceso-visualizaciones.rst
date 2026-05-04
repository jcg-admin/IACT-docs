.. meta::
 :artefacto: ARQ_MOD_005_DIAG_FLUJO_ACCESO
 :tipo: Diagrama Arquitectonico — Comportamiento de Modulo
 :dominio: arquitectura_tecnica
 :subdominio: modulos/vis-reports/diagramas
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _arq_mod_005_flujo_acceso_visualizaciones:

=================================
Flujo de Acceso a Visualizaciones
=================================

Flujo de Acceso a Visualizaciones
===================================

.. uml::
 :caption: Flujo de acceso a visualizaciones — consulta RBAC, segmentos y exportacion.

 @startuml

 start

 :view_reports solicita reporte IVR;

 :JWT + RBAC: verificar view_reports;

 if (Sin permiso?) then (si)
   :403 Forbidden;
   stop
 endif

 :SegmentResolver.resolve(user_id);
 :Mapear DIDs RBAC a segmentos IVR;

 if (Sin segmentos?) then (si)
   :400 USER_WITHOUT_SEGMENT;
   stop
 endif

 :cursor.callproc(sp_rpt_*, [trimestre, segmentos]);

 if (Tiene permiso export_csv?) then (si)
   :Retornar datos + opciones exportacion;
   if (Solicita exportacion?) then (si)
     :Encolar job de exportacion asincrona;
     :Notificar via InternalMailbox;
     stop
   else (no exporta)
     :Retornar dataset al frontend;
   stop
   endif
 else (solo view)
   :Retornar dataset filtrado por segmentos;
   stop
 endif

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modulos/vis-reports/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
