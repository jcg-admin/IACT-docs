3. Factory Method aplicado a reportes
=====================================

**Problema.** ``UC_RPT_*`` abarca varios tipos de reporte
(volumen, abandono, compliance de separacion de deberes).
Cada tipo tiene su propio agregador, pero comparte la
interfaz ``IReport``.

**Patron.** Factory Method (GoF). El nombre del PATRON
``Factory`` aplica como vocabulario disciplinar de patrones
de diseno (en este documento de metodologia, exempt segun
STD-010 §2.3). El nombre de la CLASE concreta sigue
CLEAN_CODE §1.4: describe el rol en el dominio, no el
patron.

**Rol de dominio:** la clase recibe un tipo discriminante
y devuelve la implementacion concreta correspondiente.
Es un **registro de tipos de reporte** que tambien los
instancia. Por eso se llama ``ReportTypeRegistry``, no
``ReportFactory``.

.. uml::

   @startuml
   interface IReport {
     + generate() : Result
   }
   class VolumeReport
   class AbandonmentReport
   class SeparationComplianceReport
   class ReportTypeRegistry {
     + {static} create(type : str, params) : IReport
     + {static} register(type : str, cls : Class<IReport>) : void
   }
   IReport <|.. VolumeReport
   IReport <|.. AbandonmentReport
   IReport <|.. SeparationComplianceReport
   ReportTypeRegistry ..> IReport : creates
   @enduml

.. note::

 La implementacion del patron sigue la estructura mostrada en el
 diagrama UML. Los detalles de codigo van en el repositorio fuente,
 no en la especificacion.

.. note::

 **Rename historico.** Esta documentacion fue renombrada de
 ``factory-reportefactory.rst`` a ``factory-method-reportes.rst``
 y la clase de ``ReportFactory`` a ``ReportTypeRegistry`` en el
 WP ``sprint1-filenames-and-factory`` (CLEAN_CODE §1.4). El
 nombre del documento preserva ``factory`` porque describe el
 patron GoF (vocabulario disciplinar aceptado en
 ``_metodologia-aplicacion/`` por STD-010 §2.3); el nombre de
 la clase fue cambiado porque viola §1.4. Tambien se renombro
 ``SoDComplianceReport`` -> ``SeparationComplianceReport``
 por consistencia con la regla "no Sod en identificadores"
 (Sprint 2 cubre el resto de identificadores SoD).
