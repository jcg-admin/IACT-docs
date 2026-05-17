6. Facade — ExportarReporteFacade (UC_RPT_04)
==============================================

**Problema.** UC_RPT_04 toca ``perm_app``, ``rpt_app``,
``log_app`` y ``aud_app``. Sin facade, los callers tendrían
que conocer todas las dependencias.

.. uml::

   @startuml
   class ExportarReporteFacade {
     - perm
     - rpt
     - log
     - aud
     + ejecutar(user, cfg) : ResultadoExport
   }
   ExportarReporteFacade --> perm_app
   ExportarReporteFacade --> rpt_app
   ExportarReporteFacade --> log_app
   ExportarReporteFacade --> aud_app
   @enduml

.. note::

 La implementacion del patron sigue la estructura mostrada en el
 diagrama UML. Los detalles de codigo van en el repositorio fuente,
 no en la especificacion.
