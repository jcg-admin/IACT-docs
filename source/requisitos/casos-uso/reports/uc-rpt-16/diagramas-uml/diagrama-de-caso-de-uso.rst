8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_RPT_16 — actores y casos asociados

 @startuml

 left to right direction

 actor "view_reports" as view_reports
 actor "ReportingService\n(sp_rpt_menu_redirigidos\n+ sp_rpt_menu_centro\n+ sp_rpt_cMENU_ERROR)" as ReportingService <<sistema>>
 database "BD_IVR" as BdIvrLegacy

 rectangle "MOD_Reports" {
   usecase "UC_RPT_16\nReporte de Menus IVR" as UC_RPT_16
   usecase "UC_INC_RPT_01\nResolver Segmento\n(included)" as UC_INC_RPT_01
   usecase "Vista: redirigidos" as VistaRedirigidos
   usecase "Vista: menu_centro" as VistaMenuCentro
   usecase "Vista: errores" as VistaErrores
 }

 view_reports --> UC_RPT_16
 UC_RPT_16 ..> UC_INC_RPT_01 : <<include>>
 UC_RPT_16 ..> VistaRedirigidos : <<extend>>
 UC_RPT_16 ..> VistaMenuCentro : <<extend>>
 UC_RPT_16 ..> VistaErrores : <<extend>>
 VistaRedirigidos --> ReportingService : callproc(sp_rpt_menu_redirigidos)
 VistaMenuCentro  --> ReportingService : callproc(sp_rpt_menu_centro)
 VistaErrores     --> ReportingService : callproc(sp_rpt_cMENU_ERROR)
 ReportingService --> BdIvrLegacy : CALL sp_rpt_*

 note bottom of UC_RPT_16
   BReq-001 + BReq-007. Identificar
   cuello de botella en IVR: opciones
   confusas, drop-off alto,
   tiempo en menu excesivo.
   CNST-007 read-only BD_IVR — TRIPLE SP.
   Cada vista mapea a un SP distinto;
   backend no agrega ni hace path mining.
 end note

 @enduml

.. seealso::

 Modelo del dominio relevante para este UC:

 - :doc:`/arquitectura-tecnica/domain-model/ivr-navigation-report-service` —
   servicio especifico para reporte IVR.
 - :doc:`/arquitectura-tecnica/domain-model/base-report-service` —
   patron template-method base.
 - :doc:`/arquitectura-tecnica/domain-model/bucket` —
   bucket de distribucion por opcion + drop-off por nodo.
 - :doc:`/arquitectura-tecnica/domain-model/call` —
   Call con paths IVR navegados.
 - :doc:`/requisitos/casos-uso/caller/uc-cli-02/index` —
   UC origen de la navegacion IVR.
