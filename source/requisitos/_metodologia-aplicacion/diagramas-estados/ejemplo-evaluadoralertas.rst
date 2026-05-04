9.1 Ejemplo — EvaluadorAlertas
------------------------------

.. uml::

   @startuml

   [*] --> Monitoreando

   Monitoreando : do / consultar_metricas_cada_minuto()

   Monitoreando --> AlertandoUmbral : [valor >= umbral]\n/ disparar_alerta()

   AlertandoUmbral : do / esperar_reconocimiento()

   AlertandoUmbral --> Monitoreando : supervisor_reconoce()\n/ auditar(ALERT_ACK)
   AlertandoUmbral --> AlertandoUmbral : timeout_30min /\nescalar_severidad()

   note right of Monitoreando
     EvaluadorAlertas NUNCA
     se inactiva. No hay
     transición a [*]. Ciclo
     perpetuo Monitoreando ↔
     AlertandoUmbral.
   end note
   @enduml

----
