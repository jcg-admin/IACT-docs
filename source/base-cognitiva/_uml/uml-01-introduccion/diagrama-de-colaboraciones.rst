Diagrama de colaboraciones
==========================

Los elementos de un sistema trabajan en conjunto para cumplir con
los **objetivos del sistema**. El diagrama de colaboraciones UML
está diseñado con este fin.

Este ejemplo agrega un **cronómetro interno** al conjunto de
clases que constituyen a una lavadora. Luego de cierto tiempo, el
cronómetro detendrá el flujo de agua y el tambor comenzará a
girar de un lado a otro.

.. uml::

   @startuml

   object Cronometro
   object Manguera
   object Tambor

   Cronometro "1" -- "1" Manguera : controla
   Cronometro "1" -- "1" Tambor   : activa
   Manguera   "1" -- "1" Tambor   : llena
   @enduml
