Aplicación a IACT
~~~~~~~~~~~~~~~~~

Aplicado al diagrama del modelo IACT consolidado (§ 7),
las descripciones precisas refuerzan la legibilidad:

.. uml::

   @startuml

   class Llamada
   class Segmento
   class EjecucionETL
   class VentanaETL
   class ErrorETL
   class Reporte
   class Filtro
   class Alerta
   class Supervisor
   class Usuario
   class Sesion
   class Grupo
   class Funcion
   class EventoAuditoria

   Llamada "1..*" -- "1" Segmento : pertenece a
   VentanaETL "1" -- "*" EjecucionETL : contiene
   EjecucionETL "*" -- "*" Llamada : carga
   EjecucionETL "1" *-- "*" ErrorETL : produce
   Reporte "*" -- "*" Llamada : agrega
   Reporte "1" o-- "*" Filtro : aplica
   Alerta "*" -- "1" Supervisor : es reconocida por
   Sesion "1" *-- "1" Usuario : pertenece a
   Usuario "*" o-- "*" Grupo : asignado a
   Grupo "*" o-- "*" Funcion : agrupa
   Usuario "1" --> "*" EventoAuditoria : genera
   @enduml

Notar:

- **``pertenece a``**, **``contiene``**, **``carga``**,
  **``agrega``**, **``aplica``**, **``es reconocida por``**
  — verbos precisos del dominio en lugar de ``has``
  genérico.
- **``Usuario --> EventoAuditoria : genera``** —
  asociación direccional. El ``EventoAuditoria`` no
  mantiene referencia bidireccional al usuario en
  sentido funcional; el flujo es solo "usuario genera
  evento" (CNST_025: el evento es inmutable y no se
  reasigna).
- **``Alerta -- Supervisor : es reconocida por``** —
  bidireccional, descripción válida en ambos sentidos
  con la misma frase desde el lado de la alerta.
