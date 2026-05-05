Diagrama de secuencias genérico
-------------------------------

El caso de uso *"Comprar gaseosa"* tenía dos escenarios alternos:
máquina sin la gaseosa seleccionada, y cliente sin el dinero
exacto.

.. warning:: Diagrama de secuencias genérico

 Es un diagrama de secuencias que toma en cuenta **todos los
 escenarios** de un caso de uso.

Para representar cada condición en la secuencia, tal condición
se coloca en un *si condicional* entre **corchetes**:

::

 [alimentación > precio]
 [alimentación - precio no presente]
 [alimentación - precio presente]

**Cada condición causa una bifurcación** del control en el
mensaje, que separará al mensaje en rutas distintas. Como cada
ruta irá al mismo objeto, la bifurcación causa una *"ramificación"*
del control en la línea de vida del objeto receptor. En algún
lugar de la secuencia, las ramas confluirán.

Escenario "Monto incorrecto":

.. uml::

   @startuml

   actor Cliente
   participant ":Fachada"     as F
   participant ":Registrador" as R
   participant ":Dispensador" as D

   Cliente -> F  : insertarDinero
   Cliente -> F  : seleccionarMarca
   F -> R        : enviarDinero
   R -> R        : verificarMonto

   alt [alimentación > precio]
     alt [alimentación - precio presente]
       R -> Cliente : devolverCambio
       R -> D       : entregarGaseosa
       D -> F       : depositarGaseosa
     else [alimentación - precio no presente]
       R -> Cliente : devolverDinero
       R -> F       : "Inserte importe exacto"
     end
   else [alimentación = precio]
     R -> D : entregarGaseosa
     D -> F : depositarGaseosa
   else [alimentación < precio]
     F -> Cliente : "Esperando más dinero"
   end
   @enduml

Escenarios "Monto incorrecto" + "Sin marca":

1. Una vez que el cliente elige una marca agotada, la máquina
   muestra un mensaje de *"Agotado"*.
2. La máquina muestra un mensaje que solicita al cliente que
   haga otra elección.
3. El cliente tiene la opción de oprimir un botón para que se le
   regrese su dinero.
4. Si el cliente elige una marca en existencia, todo procede
   como en el mejor escenario.
5. Si el cliente elige otra marca agotada, el proceso se repite.

.. uml::

   @startuml

   actor Cliente
   participant ":Fachada"     as F
   participant ":Registrador" as R
   participant ":Dispensador" as D

   Cliente -> F  : insertarDinero
   F -> R        : enviarDinero

   loop mientras [marca no disponible y cliente no cancela]
     Cliente -> F : seleccionarMarca
     F -> D       : verificarMarca
     alt [no disponible]
       D --> F : "Agotado"
       F -> Cliente : pedirOtraSeleccion
     else [disponible]
       break
     end
   end

   alt [cliente cancela]
     R -> Cliente : devolverDinero
   else [marca disponible]
     R -> R : verificarMonto
     alt [monto correcto]
       R -> D : entregarGaseosa
       D -> F : depositarGaseosa
     else [monto incorrecto]
       R -> Cliente : devolverDineroOAjustar
     end
   end
   @enduml

Si empieza a pensar que un diagrama de secuencias está implícito
en cada caso de uso, ya tiene la idea.
