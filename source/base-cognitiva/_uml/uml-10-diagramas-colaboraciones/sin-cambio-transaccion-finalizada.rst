Sin cambio (transacción finalizada)
-----------------------------------

¿Qué ocurre cuando la máquina no cuenta con el cambio correcto?
Tendrá que mostrar un mensaje, devolver el dinero y pedir el
importe correcto. Agregue una **bifurcación** en el control de
flujo y un estereotipo ``«transacción finalizada»``.

.. uml::

   @startuml
   allowmixing

   actor Cliente
   object ":Fachada"     as F
   object ":Registrador" as R
   object ":Dispensador" as D

   Cliente -> F : "insertar(alimentacion, seleccion)"
   F -> R       : "1: agregar(alimentacion, seleccion)"
   R -> D       : "[alim = precio]\n2.1: despachar(seleccion)"
   R -> R       : "[alim > precio]\n2.2: verificarCambio(alim, precio)"
   D -> F       : "[hay cambio]\n3.1: despachar(seleccion)"
   R -> Cliente : "[hay cambio]\n3.2: devolver(cambio)"
   R -> Cliente : "<<transacción finalizada>>\n[no hay cambio]\n3.3: devolver(alim)"
   R -> F       : "[no hay cambio]\n3.4: mostrar('Inserte importe exacto')"
   @enduml

----
