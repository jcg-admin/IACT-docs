Asociación
==========

Es importante saber cómo se conectan las clases entre sí. Cuando
las clases se conectan entre sí de **forma conceptual**, esta
conexión se conoce como **asociación**.

Por ejemplo: la asociación entre un jugador y un equipo. *"Un
jugador participa en un equipo"*. Se visualizará en UML como una
**línea que conectará a ambas clases**, con el nombre de la
asociación (``"participa en"``) justo sobre la línea.

Dicha línea indicará la dirección de la relación con un
**triángulo relleno** que apunte en la dirección apropiada.

.. uml::

   @startuml

   class Jugador
   class Equipo
   Jugador --> Equipo : participa en  ▶
   @enduml

.. note::

 Cuando una clase se asocia con otra, cada una de ellas **juega
 un papel dentro de tal asociación**.

Puede representar los papeles en el diagrama escribiéndolos
cerca de la línea de asociación, junto a la clase que juega el
papel correspondiente. Si el equipo es profesional, éste es un
**empleador** y el jugador es un**empleado**.

En el ejemplo, el equipo tiene jugadores a los que contrata para
jugar: el ``Equipo`` juega el rol de **empleador** porque es
quien da el trabajo y paga, los ``Jugadores`` actúan como
**empleados** porque aceptan el trabajo y desempeñan las
funciones asignadas.

.. note:: Relación empleador-empleado

 La *"relación empleador-empleado"* se refiere a una
 **interacción o vínculo** entre dos entidades donde una toma
 el papel de **quien contrata** (empleador) y la otra el papel
 de **quien es contratado** (empleado, que acepta ese trabajo y
 realiza las tareas establecidas por el empleador).

 Es un vínculo formal y de dependencia: una parte tiene
 autoridad para contratar y dar tareas, mientras que la otra
 parte sigue las directrices a cambio de un beneficio.

.. uml::

   @startuml

   class Equipo
   class Jugador
   Equipo "empleador" --> "empleado" Jugador : contrata
   @enduml

La asociación puede funcionar en dirección inversa: un equipo
emplea a jugadores; si no hay empleado (jugador), el empleador
(equipo) no tiene a quién contratar. Y si no hay empleador, el
empleado no tendría un trabajo. Por lo tanto, **ambos dependen
mutuamente** para que exista la relación de trabajo.

Mostrar ambas asociaciones en el mismo diagrama con un triángulo
relleno que indique la dirección de cada asociación.

.. uml::

   @startuml

   class Equipo
   class Jugador
   Equipo "empleador" --> "empleado" Jugador : contrata  ▶
   Jugador "empleado" --> "empleador" Equipo : trabaja para  ▶
   @enduml

Cómo identificar una relación inversa / dependencia mutua
---------------------------------------------------------

Debes identificar si existe una **interacción mutua** entre dos
entidades, donde ambas cumplen roles complementarios. Si cada
entidad tiene una función distinta pero interconectada, entonces
la relación puede observarse desde ambos lados.

Una "función distinta pero interconectada" se refiere a que en
una relación entre dos entidades, cada una **hace cosas
diferentes** (funciones distintas), pero ambas funciones están
relacionadas y dependen entre sí para que la relación exista.

Puedes preguntarte:

1. **¿Qué es A y B en su núcleo?**

   - ¿Qué rol o propósito fundamental cumple cada entidad en
     la relación?
   - ¿Qué función cumple cada entidad?
   - La respuesta tiene que ser acciones, como enseñar,
     aprender, dar trabajo, hacer el trabajo, comprar, vender.

2. **¿A puede cumplir su propósito sin B?**

   - ¿Puede cada entidad existir y realizar su función sin la
     otra, o necesita de la otra para tener sentido?
   - Si la respuesta es **no**, entonces no hay dependencia
     mutua.

3. **Si B no existe, ¿A sigue teniendo sentido?**

   - Si una entidad desaparece, ¿cómo afecta esto a la función
     o propósito de la otra?
   - Si una entidad no puede cumplir su rol sin la otra, hay
     dependencia mutua.

4. **¿Qué obtiene A de B y qué obtiene B de A?**

   - ¿Qué contribución o valor esencial proporciona cada
     entidad para mantener la relación?
   - Si no, es una relación dependiente.

5. **¿Ambos dependen de un intercambio necesario?**

   - ¿Es esta interacción una necesidad mutua, donde ambas
     entidades intercambian algo fundamental?
   - Esto refleja que la relación es **bidireccional** y que
     ambas partes dependen una de la otra.

Si descubres que **A y B no pueden cumplir su rol sin la otra**,
o que la relación pierde sentido si una de ellas no está
presente, entonces estás ante una **relación de dependencia
mutua**.

Las asociaciones podrían ser más complejas: **varias clases se
pueden conectar a una**. Los defensas, delanteros y central, así
como sus asociaciones con la clase ``Equipo``:

.. uml::

   @startuml

   class Equipo
   class Defensa
   class Delantero
   class Central

   Equipo "1" -- "2" Defensa   : tiene
   Equipo "1" -- "2" Delantero : tiene
   Equipo "1" -- "1" Central   : tiene
   @enduml
