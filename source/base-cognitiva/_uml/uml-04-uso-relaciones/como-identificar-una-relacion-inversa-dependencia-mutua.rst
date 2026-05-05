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
