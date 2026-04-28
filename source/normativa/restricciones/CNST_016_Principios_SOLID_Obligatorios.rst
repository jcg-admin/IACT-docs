.. meta::
   :artefacto: CNST_016
   :tipo: Restriccion
   :dominio: normativa
   :subdominio: restricciones
   :estado: Vigente
   :version: 1.0.0
   :fecha_creacion: 2025-12-17
   :ultimo_cambio: 2026-04-28
   :autor: NestorMonroy
   :clasificacion: Alto

.. _cnst-016:

=======================================
CNST-016: Principios SOLID Obligatorios
=======================================

Enunciado
---------

El diseno de clases y modulos del sistema IACT DEBE cumplir los cinco
principios SOLID. Las violaciones documentadas requieren ADR con
justificacion.

Justificacion
-------------

SOLID es la base reconocida para un diseno orientado a objetos mantenible y extensible. Su aplicacion sistematica reduce el acoplamiento, facilita el testing y permite que el codebase crezca sin acumular deuda tecnica.

Principios
----------

- **S - Single Responsibility:** una clase, una razon para cambiar.
- **O - Open/Closed:** abierto a extension, cerrado a modificacion.
- **L - Liskov Substitution:** subclase debe sustituir a su base sin
  romper contrato.
- **I - Interface Segregation:** preferir interfaces especificas a
  una grande.
- **D - Dependency Inversion:** depender de abstracciones, no
  implementaciones.

Verificacion
------------

- Code review explicito con checklist SOLID.
- Metricas: complejidad ciclomatica <10, longitud de metodo <50 ln.

Referencias cruzadas
--------------------

- :doc:`CNST_015_Antipatrones_de_Arquitectura_Prohibidos`
