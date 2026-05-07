.. _uc-rpt-17-parte-08-diagrama-flujo-de-anonimizacion-etl:

8.3 Diagrama de flujo — Anonimizacion en ETL
================================================

.. uml::
 :caption: UC_RPT_17 — pipeline de anonimizacion del telefono cliente.

 @startuml

 component "tbl_historico_*\n(cTelefono_Origen raw)" as TblHistorico
 component "sp_etl_base_clientes\n(hash unidireccional)" as sp_etl_base_clientes
 component "base_ivr_clientes\n(telefono_hashed)" as BaseAnaliticaDestino
 component "sp_rpt_clientes\n(solo lee hash)" as sp_rpt_clientes

 TblHistorico --> sp_etl_base_clientes : raw input
 sp_etl_base_clientes --> BaseAnaliticaDestino : write hashed
 BaseAnaliticaDestino --> sp_rpt_clientes : read hashed

 note right of sp_etl_base_clientes
   PII nunca almacenada
   en base analitica.
   Hash unidireccional con
   sal por segmento.
 end note

 @enduml

.. seealso::

 - :doc:`diagrama-de-caso-de-uso`.
 - :doc:`/arquitectura-tecnica/domain-model/pii-scanner`.
 - :doc:`/arquitectura-tecnica/domain-model/sanitizer`.
 - :doc:`/arquitectura-tecnica/domain-model/caller-report-service`.
 - :doc:`/requisitos/reglas-negocio/br-020-clasificacion-datos`.
