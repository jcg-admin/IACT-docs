Ejemplo IACT — vinculación textual recomendada
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. uml::

   @startuml
   title Modelo de dominio IACT — entidades de auditoria
   hide empty members
   class EventoAuditoria
   class DetalleAuditoria
   EventoAuditoria "1" *-- "1..*" DetalleAuditoria : detalla
   @enduml

**Referencias** asociadas a cada entidad (en el texto,
no en el diagrama):

- ``EventoAuditoria`` — definida en § 3 de este
  documento, restricción CNST_025 (auditoría
  inmutable), UCs que la generan: todos los UCs del
  catálogo (audit transversal).
- ``DetalleAuditoria`` — composición fuerte (§ 3 de
  :doc:`/requisitos/_metodologia-aplicacion/agregacion-interfaces/index`). Usada en
  :doc:`/requisitos/_metodologia-aplicacion/patrones-diseno/index` § 8 (Observer +
  ``AuditObserver``).
