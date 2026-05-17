Aplicación a IACT — snapshot de dependencias
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Snapshot del facade y sus dependencias
inyectadas, complementando § 17.1:

.. uml::

   @startuml
   title Snapshot dependencias — ExportReportFacade

   class ExportReportFacade
   class SecRules
   class Report
   class Worker
   class Bus
   class Mailbox

   ExportReportFacade ..> SecRules : injects
   ExportReportFacade ..> Report : injects
   ExportReportFacade ..> Worker : injects
   ExportReportFacade ..> Bus : uses (singleton)
   ExportReportFacade ..> Mailbox : injects
   @enduml

Lectura del snapshot:

- **Cuatro dependencias inyectadas** y una
  **acoplada al singleton** (``Bus``).
- La asimetría entre etiquetas (``inyecta`` vs
  ``usa singleton``) **resalta** un punto
  discutible: ¿deberíamos inyectar el bus también
  para mejorar testabilidad?
- El diagrama **no necesita atributos ni
  métodos** para esta pregunta — solo la red de
  dependencias.
