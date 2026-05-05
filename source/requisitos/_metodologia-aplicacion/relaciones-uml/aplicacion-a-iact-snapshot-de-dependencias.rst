Aplicación a IACT — snapshot de dependencias
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Snapshot del facade y sus dependencias
inyectadas, complementando § 17.1:

.. uml::

   @startuml
   title Snapshot dependencias — ExportarReporteFacade

   class ExportarReporteFacade
   class SecRules
   class Reporte
   class Worker
   class Bus
   class Buzon

   ExportarReporteFacade ..> SecRules : inyecta
   ExportarReporteFacade ..> Reporte : inyecta
   ExportarReporteFacade ..> Worker : inyecta
   ExportarReporteFacade ..> Bus : usa (singleton)
   ExportarReporteFacade ..> Buzon : inyecta
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
