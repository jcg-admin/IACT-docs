8. Observer — AuditLog como observer de eventos
================================================

**Problema.** CNST_025 exige audit immutable y completo. En
lugar de que cada UC llame ``aud_app.registrar`` por
duplicado, los eventos de dominio se publican y
``audit_log`` se suscribe.

.. uml::

   @startuml
   interface Observer {
     + notificar(evento)
   }
   class Bus {
     - observers : list
     + suscribir(o : Observer)
     + publicar(evento)
   }
   class AuditObserver {
     + notificar(evento)
   }
   class MetricasObserver {
     + notificar(evento)
   }
   Observer <|.. AuditObserver
   Observer <|.. MetricasObserver
   Bus --> Observer
   @enduml

.. note::

 La implementacion del patron sigue la estructura mostrada en el
 diagrama UML. Los detalles de codigo van en el repositorio fuente,
 no en la especificacion.

Regla IACT: ``AuditObserver`` no se puede desuscribir en
runtime — eso violaría CNST_025.
