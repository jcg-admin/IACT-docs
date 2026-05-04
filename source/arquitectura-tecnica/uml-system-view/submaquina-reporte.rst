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

 state "Consulta de Reporte IVR" as RPT_EXEC {

   state "Solicitar Reporte" as R1
   R1 : entry / validar funcion view_reports en JWT
   R1 : do / enviar GET /api/reportes/?trimestre=
   R1 : exit / solicitud aceptada por DashboardEndpoint

   state "Resolver Segmento\nUC_INC_RPT_01" as R2
   R2 : entry / leer DIDs RBAC del usuario en PostgreSQL
   R2 : do / mapear DIDs via DID_MAP a segmentos IVR
   R2 : exit / lista de segmentos activos disponible

   state fork_seg <<fork>>

   state "Segmento nacional_A\n(DID 19028031)" as R3A
   R3A : entry / DID 19028031 activo en usuario
   R3A : do / filtrar rows por nacional_A
   R3A : exit / atributos de segmento disponibles

   state "Segmento nacional_B\n(DID 19020001)" as R3B
   R3B : entry / DID 19020001 activo en usuario
   R3B : do / filtrar rows por nacional_B
   R3B : exit / atributos de segmento disponibles

   state "Segmento Puebla\n(DID 19020084)" as R3C
   R3C : entry / DID 19020084 activo en usuario
   R3C : do / filtrar rows por Puebla
   R3C : exit / atributos de segmento disponibles

   state join_seg <<join>>

   state "Llamar sp_rpt_*" as R4
   R4 : entry / consolidar segmentos activos del usuario
   R4 : do / cursor.callproc(sp_rpt_*, [trimestre, segmentos])
   R4 : exit / rows de reporte disponibles

   state "Renderizar Reporte" as R5
   R5 : entry / recibir rows del sp_rpt_*
   R5 : do / enviar datos al frontend
   R5 : exit / reporte renderizado al usuario

   [*] --> R1
   R1 --> R2
   R2 --> fork_seg
   fork_seg --> R3A
   fork_seg --> R3B
   fork_seg --> R3C
   R3A --> join_seg
   R3B --> join_seg
   R3C --> join_seg
   join_seg --> R4
   R4 --> R5
   R5 --> [*]
 }

 [*] --> RPT_EXEC
 RPT_EXEC --> [*]

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
