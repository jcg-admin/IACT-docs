Subestados concurrentes
-----------------------

La GUI no sólo aguarda a que usted haga algo: también verifica
el cronómetro del sistema y (posiblemente) actualiza el
despliegue de una aplicación luego de un intervalo específico.
Una aplicación podría incluir un reloj en pantalla que tuviera
que actualizar la GUI.

Todo esto sucede al **mismo tiempo** que la secuencia anterior.
Cada secuencia es un conjunto de subestados secuenciales; las
dos secuencias son **concurrentes** entre sí.

Puede representar la concurrencia con una **línea discontinua**
entre las regiones concurrentes.

.. uml::

   @startuml

   state Operacion {
     state "Acciones del usuario" as RegionA {
       [*] --> Espera
       Espera --> Registro : accionUsuario
       Registro --> Representacion
       Representacion --> Espera
     }

     ||

     state "Cronómetro / Reloj" as RegionB {
       [*] --> Verificar
       Verificar --> Actualizar : intervaloCumplido
       Actualizar --> Verificar
     }
   }
   @enduml

Cuando **cada componente sea parte de un "todo"**, tratará con
una *composición*. Las partes concurrentes del estado *Operación*
tienen el mismo tipo de relación con él. Por ello, *Operación*
es un **estado compuesto**. Un estado que consta sólo de
subestados secuenciales también es un estado compuesto.
