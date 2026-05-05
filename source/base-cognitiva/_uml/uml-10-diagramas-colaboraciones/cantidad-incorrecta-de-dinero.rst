Cantidad incorrecta de dinero
-----------------------------

Agreguemos el caso de *"cantidad incorrecta de dinero"*. Hay
varias condiciones:

1. El usuario ha introducido más dinero del necesario.
2. La máquina cuenta con cambio.
3. La máquina no tiene cambio.

Coloque la **condición entre corchetes**, antecediendo la
etiqueta. **Lo importante es coordinar las condiciones con la
numeración.**

El paso que devuelve el cambio *es una consecuencia* del que
verifica si hay cambio. Para indicar esto se utiliza el mismo
número y se agrega ``.1`` (**anidación**):

- Si el mensaje que verifica el cambio es ``N``,
- el mensaje que devuelve el cambio será ``N.1``.

.. uml::

   @startuml
   allowmixing

   actor Cliente
   object ":Fachada"     as F
   object ":Registrador" as R
   object ":Dispensador" as D

   Cliente -> F : "insertar(alimentacion, seleccion)"
   F -> R       : "1: agregar(alimentacion, seleccion)"
   R -> D       : "[alimentacion = precio]\n2.1: despachar(seleccion)"
   R -> R       : "[alimentacion > precio]\n2.2: verificarCambio(alim, precio)"
   D -> F       : "[hay cambio]\n3.1: despachar(seleccion)"
   R -> Cliente : "[hay cambio]\n3.2: devolver(cambio)"
   @enduml
