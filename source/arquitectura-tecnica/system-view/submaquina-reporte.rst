.. meta::
 :artefacto: AT_UML_SISTEMA_13_ESTADOS_REPORTE
 :tipo: Diagrama Arquitectonico — UML Sistema
 :dominio: arquitectura_tecnica
 :subdominio: UMLSystemView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uml_sistema_submaquina_reporte:

==========================================================
Sistema IACT — Sub-maquina de Estados: Consulta de Reporte
==========================================================

13. Sub-maquina de Estados — Consulta de Reporte
=================================================

Sub-estado interno de ``MOD Reports``. Muestra el flujo de
``UC_INC_RPT_01`` (Resolver Segmento) seguido de la resolucion
paralela por segmento activo del usuario y la llamada al
``sp_rpt_*`` correspondiente con join antes de renderizar.

.. uml::
 :caption: Figura 14 — Sub-maquina de estados: Consulta de Reporte IVR

 @startuml

 state "Consulta de Reporte IVR" as ARTEFACTO_RPT_EJECUCION {

   state "Solicitar Reporte" as VER_DASHBOARD_IVR
   VER_DASHBOARD_IVR : entry / validar funcion view_reports en JWT
   VER_DASHBOARD_IVR : do / enviar GET /api/reportes/?trimestre=
   VER_DASHBOARD_IVR : exit / solicitud aceptada por DashboardEndpoint

   state "Resolver Segmento\nUC_INC_RPT_01" as RESOLVER_SEGMENTO
   RESOLVER_SEGMENTO : entry / leer DIDs RBAC del usuario en PostgreSQL
   RESOLVER_SEGMENTO : do / mapear DIDs via DID_MAP a segmentos IVR
   RESOLVER_SEGMENTO : exit / lista de segmentos activos disponible

   state fork_seg <<fork>>

   state "Segmento nacional_A\n(DID 19028031)" as EXTENSION_REPORTES_HISTORICOS
   EXTENSION_REPORTES_HISTORICOS : entry / DID 19028031 activo en usuario
   EXTENSION_REPORTES_HISTORICOS : do / filtrar rows por nacional_A
   EXTENSION_REPORTES_HISTORICOS : exit / atributos de segmento disponibles

   state "Segmento nacional_B\n(DID 19020001)" as EXTENSION_REPORTES_HISTORICOS_B
   EXTENSION_REPORTES_HISTORICOS_B : entry / DID 19020001 activo en usuario
   EXTENSION_REPORTES_HISTORICOS_B : do / filtrar rows por nacional_B
   EXTENSION_REPORTES_HISTORICOS_B : exit / atributos de segmento disponibles

   state "Segmento Puebla\n(DID 19020084)" as EXTENSION_REPORTES_HISTORICOS_C
   EXTENSION_REPORTES_HISTORICOS_C : entry / DID 19020084 activo en usuario
   EXTENSION_REPORTES_HISTORICOS_C : do / filtrar rows por Puebla
   EXTENSION_REPORTES_HISTORICOS_C : exit / atributos de segmento disponibles

   state join_seg <<join>>

   state "Llamar sp_rpt_*" as EJECUTAR_PROCEDIMIENTO_RPT
   EJECUTAR_PROCEDIMIENTO_RPT : entry / consolidar segmentos activos del usuario
   EJECUTAR_PROCEDIMIENTO_RPT : do / cursor.callproc(sp_rpt_*, [trimestre, segmentos])
   EJECUTAR_PROCEDIMIENTO_RPT : exit / rows de reporte disponibles

   state "Renderizar Reporte" as RENDERIZAR_REPORTE
   RENDERIZAR_REPORTE : entry / recibir rows del sp_rpt_*
   RENDERIZAR_REPORTE : do / enviar datos al frontend
   RENDERIZAR_REPORTE : exit / reporte renderizado al usuario

   [*] --> VER_DASHBOARD_IVR
   VER_DASHBOARD_IVR --> RESOLVER_SEGMENTO
   RESOLVER_SEGMENTO --> fork_seg
   fork_seg --> EXTENSION_REPORTES_HISTORICOS
   fork_seg --> EXTENSION_REPORTES_HISTORICOS_B
   fork_seg --> EXTENSION_REPORTES_HISTORICOS_C
   EXTENSION_REPORTES_HISTORICOS --> join_seg
   EXTENSION_REPORTES_HISTORICOS_B --> join_seg
   EXTENSION_REPORTES_HISTORICOS_C --> join_seg
   join_seg --> EJECUTAR_PROCEDIMIENTO_RPT
   EJECUTAR_PROCEDIMIENTO_RPT --> RENDERIZAR_REPORTE
   RENDERIZAR_REPORTE --> [*]
 }

 [*] --> ARTEFACTO_RPT_EJECUCION
 ARTEFACTO_RPT_EJECUCION --> [*]

 @enduml

.. note::

 El fork/join de segmentos es logico — el ``SegmentResolver``
 evalua en paralelo todos los segmentos del usuario. Solo los
 segmentos con DID asignado al usuario contribuyen rows al join.
 Si el usuario no tiene ningun DID activo, el flujo retorna
 400 ``USER_WITHOUT_SEGMENT`` antes del fork.

.. seealso::

 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/requisitos/casos-uso/index`
