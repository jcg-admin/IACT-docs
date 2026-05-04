Qué es un diagrama de actividades
=================================

Está diseñado para mostrar una **visión simplificada** de lo que
ocurre durante una operación o proceso.

Es una **extensión del diagrama de estados**: el de estados
muestra los estados de un objeto y representa las actividades
como flechas; el de actividades **resalta estas actividades**.

El procesamiento dentro de una actividad se lleva a cabo y, al
realizarse, se continúa con la siguiente.

- Cada actividad se representa por un **rectángulo con esquinas
  redondeadas**.
- Una **flecha** representa la transición de una a otra
  actividad.
- Cuenta con un **punto inicial** (círculo relleno) y un
  **punto final** (diana).

.. uml::

   @startuml

   start
   :Actividad 1;
   :Actividad 2;
   stop
   @enduml

----
