6.2 Subestados concurrentes — Alerta evaluadora
-----------------------------------------------

Una alerta puede estar evaluando umbrales y, **al mismo
tiempo**, gestionando suscriptores.

.. uml::

   @startuml

   [*] --> Configurada

   Configurada --> EnEvaluacion : umbral_definido()

   state EnEvaluacion {
     state "Region: Evaluación de umbral" as RegionUmbral {
       [*] --> EsperandoMuestra
       EsperandoMuestra --> Comparando : nueva_metrica()
       Comparando --> EsperandoMuestra : [valor < umbral]
       Comparando --> Disparada : [valor >= umbral]
     }
     ||
     state "Region: Gestión de suscriptores" as RegionSusc {
       [*] --> Listo
       Listo --> Notificando : disparar()
       Notificando --> Listo : entrega_buzon_ok(CNST_001)
     }
   }

   EnEvaluacion --> Reconocida : supervisor_reconoce(UC_ALR_03)\n/ auditar()
   Reconocida --> [*]
   @enduml
