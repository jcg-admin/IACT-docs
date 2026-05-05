9. Diagrama de distribución
---------------------------

**Propósito:** arquitectura física del sistema (dónde se
ejecuta cada cosa). Nodos (cubos) + conexiones + artefactos.

**Cuándo usarlo:** cuando necesitas mostrar **cómo se
despliega** el sistema en producción (dónde viven las
máquinas, cómo se conectan).

**Lección completa:** :doc:`/base-cognitiva/_uml/uml-13-diagramas-distribucion/index`.

.. uml::

   @startuml

   node "Cliente" <<dispositivo>> as C {
     component "Navegador"
   }
   node "Servidor Web" <<procesador>> as W {
     component "Apache + Django"
   }
   node "BD" <<procesador>> as DB {
     database "MySQL"
   }
   cloud "Stripe API" as S

   C -- W : <<HTTPS>>
   W -- DB : <<JDBC>>
   W -- S  : <<HTTPS>>
   @enduml
