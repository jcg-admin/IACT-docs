Qué hacen las clases y cómo encontrarlas
========================================

Las clases son el **vocabulario y terminología de un área del
conocimiento**. Conforme hable con los clientes, analice su
área de conocimiento y diseñe sistemas, este vocabulario se va
formando — es lo que el cliente realiza para resolver su problema
en un área específica. Se puede decir que las clases son el
**área de dominio específico** de lo que hará el sistema.

Con los clientes, preste atención a los **sustantivos** que
utilizan para describir las entidades de sus negocios; dichos
sustantivos se convertirán en las **clases** de su modelo. Y
preste atención a los **verbos** que escuche, dado que
constituirán las **operaciones** y los**atributos** de sus
clases.

Imagine que generará un modelo del juego de baloncesto, y que
entrevista a un entrenador para comprender el juego.

.. admonition:: Ejemplo de entrevista

 **Analista:** "Entrenador, ¿de qué se trata el juego?"

 **Entrenador:** "Consiste en arrojar el*balón* a través de un
 aro, conocido como *cesto*, y hacer una mayor*puntuación* que
 el oponente. Cada *equipo* consta de cinco*jugadores*: dos
 *defensas*, dos*delanteros* y un*central*. Cada equipo lleva
 el balón al cesto del equipo oponente con el objetivo de hacer
 que el balón sea encestado."

 **Analista:** "¿Cómo se hace para llevar el balón al otro
 cesto?"

 **Entrenador:** "Mediante*pases* y*dribles*. Pero el equipo
 tendrá que encestar antes de que termine el *lapso para tirar*."

 **Analista:** "¿El lapso para tirar?"

 **Entrenador:** "Así es, son 24 segundos en el baloncesto
 profesional, 30 en un juego internacional, y 35 en el colegial
 para tirar el balón luego de que un equipo toma posesión de él."

 **Analista:** "¿Cómo funciona el puntaje?"

 **Entrenador:** "Cada*canasta* vale dos puntos, a menos que el
 tiro haya sido hecho detrás de la *línea de los tres puntos*.
 En tal caso, serán tres puntos. Un *tiro libre* contará como
 un punto. A propósito, un tiro libre es la penalización que
 paga un equipo por cometer una *infracción*. Si un jugador
 infracciona a un oponente, se detiene el juego y el oponente
 puede realizar diversos tiros al cesto desde la *línea de tiro
 libre*."

 **Analista:** "Hábleme más acerca de lo que hace cada jugador."

 **Entrenador:** "Quienes juegan de defensa son, en general,
 quienes realizan la mayor parte de los dribles y pases. Por lo
 general tienen menor estatura que los delanteros, y éstos, a
 su vez, son menos altos que el central (que también se conoce
 como 'poste'). Se supone que todos los jugadores pueden burlar,
 pasar, tirar y rebotar. Los delanteros realizan la mayoría de
 los rebotes y los disparos de mediano alcance, mientras que el
 central se mantiene cerca del cesto y dispara desde un alcance
 corto."

 **Analista:** "¿Qué hay de las dimensiones de la*cancha*? Y
 ya que estamos en eso, ¿cuánto dura el juego?"

 **Entrenador:** "En un juego internacional, la cancha mide 28
 metros de longitud y 15 de ancho; el cesto se encuentra a 3.05
 m del piso. En un juego profesional, el juego dura 48 minutos,
 divididos en cuatro cuartos de 12 minutos cada uno. En un juego
 colegial e internacional, la duración es de 40 minutos,
 divididos en dos mitades de 20 minutos. Un *cronómetro del
 juego* lleva un control del tiempo restante."

Sustantivos descubiertos: **balón**,**cesto**,**equipo**,
**jugadores**,**defensas**,**delanteros**,**central** (o
**poste**),**tiro**,**lapso para tirar**,**línea de los tres
puntos**,**tiro libre**,**infracción**,**línea de tiro libre**,
**cancha**,**cronómetro del juego**.

Verbos descubiertos: **tirar**,**avanzar**,**driblar** (o
burlar), **pasar**,**infraccionar**,**rebotar**.

También cuenta con cierta **información adicional** respecto a
algunos de los sustantivos (como las estaturas relativas de los
jugadores de cada posición, las dimensiones de la cancha, la
cantidad total de tiempo en un lapso de tiro y la duración de un
juego).

Con el sentido común podría entrar en acción para generar
ciertos **atributos** por usted mismo. Usted sabe, por ejemplo,
que el balón cuenta con ciertos atributos, como volumen y
diámetro.

A partir de esta información, podrá crear un diagrama como el
siguiente. El diagrama también muestra **las responsabilidades**.
Podría usar este diagrama como fundamento para otras
conversaciones con el entrenador para obtener mayor información.

.. uml::

   @startuml

   class Balon {
     volumen : Float
     diametro : Float
     --
     rebotar()
   }

   class Cesto {
     altura : Float
   }

   class Cancha {
     longitud : Float = 28
     ancho : Float = 15
   }

   class Equipo {
     nombre : String
     puntuacion : Integer
     --
     atacar()
     defender()
   }

   class Jugador {
     estatura : Float
     numero : Integer
     --
     tirar()
     pasar()
     driblar()
     rebotar()
     infraccionar()
   }

   class Defensa
   class Delantero
   class Central

   Jugador <|-- Defensa
   Jugador <|-- Delantero
   Jugador <|-- Central

   Equipo "1" *-- "5" Jugador

   class Tiro {
     valor : Integer
   }
   class TiroLibre
   Tiro <|-- TiroLibre

   class CronometroJuego {
     tiempoRestante : Integer
   }

   class LapsoTirar {
     duracion : Integer
   }

   Cancha "1" o-- "2" Cesto
   Equipo "2" -- "1" Cancha
   Jugador "1" -- "0..*" Tiro
   @enduml
