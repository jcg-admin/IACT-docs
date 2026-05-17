Diagrama de secuencias
======================

El diagrama de secuencias UML muestra la mecánica de la
**interacción con base en tiempos**.

Entre los componentes de la lavadora se encuentran: una
**manguera de agua** (para obtener agua fresca), un**tambor**
(donde se coloca la ropa) y un **sistema de drenaje**. Por
supuesto, estos también son objetos (un objeto puede estar
conformado por otros objetos).

¿Qué sucederá cuando invoque al caso de uso *Lavar ropa*?

Si damos por hecho que están completas las operaciones *agregar
ropa*,*agregar detergente* y*activar*, la secuencia sería más
o menos así:

1. El agua empezará a llenar el tambor mediante una manguera.
2. El tambor permanecerá inactivo durante cinco minutos.
3. La manguera dejará de abastecer agua.
4. El tambor girará de un lado a otro durante quince minutos.
5. El agua jabonosa saldrá por el drenaje.
6. Comenzará nuevamente el abastecimiento de agua.
7. El tambor continuará girando.
8. El abastecimiento de agua se detendrá.
9. El agua del enjuague saldrá por el drenaje.
10. El tambor girará en una sola dirección y se incrementará su
    velocidad por cinco minutos.
11. El tambor dejará de girar y el proceso de lavado habrá
    finalizado.

El diagrama de secuencias captura las interacciones que se
realizan a través del tiempo entre el abastecimiento de agua, el
tambor y el drenaje (representados como rectángulos en la parte
superior del diagrama). El tiempo se da de arriba hacia abajo.

.. uml::

   @startuml

   participant "Manguera\nde agua" as M
   participant "Tambor" as T
   participant "Drenaje" as D

   M -> T : abrir agua
   note right of T : reposar 5 min
   M -> T : cerrar agua
   T -> T : girar 15 min
   T -> D : descargar agua jabonosa
   M -> T : abrir agua (enjuague)
   T -> T : girar
   M -> T : cerrar agua
   T -> D : descargar agua de enjuague
   T -> T : centrifugar 5 min
   T -> T : detenerse
   @enduml

Volviendo a las ideas acerca de los estados, podríamos
caracterizar:

- Los pasos 1 y 2 como el estado de **remojo**.
- Los pasos 3 y 4 como el estado de **lavado**.
- Los pasos 5 a 7 como el estado de **enjuague**.
- Los pasos 8 al 10 como el estado de **centrifugado**.
