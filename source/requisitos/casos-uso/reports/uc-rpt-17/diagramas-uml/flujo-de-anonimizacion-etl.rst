8.3 Flujo de anonimizacion (ETL)
==================================

.. uml::

 @startuml
 component "tbl_historico_*\n(cTelefono_Origen raw)" as TblHistorico
 component "sp_etl_base_clientes\n(hash unidireccional)" as sp_etl_base_clientes
 component "base_ivr_clientes\n(telefono_hashed)" as BASE_ANALITICA_DESTINO
 component "sp_rpt_clientes\n(solo lee hash)" as sp_rpt_clientes
 TblHistorico --> sp_etl_base_clientes
 sp_etl_base_clientes --> BASE_ANALITICA_DESTINO
 BASE_ANALITICA_DESTINO --> sp_rpt_clientes
 note right of sp_etl_base_clientes
   PII nunca almacenada
   en base analitica
 end note
 @enduml

