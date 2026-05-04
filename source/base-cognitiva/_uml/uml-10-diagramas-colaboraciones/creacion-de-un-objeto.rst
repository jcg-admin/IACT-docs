Creación de un objeto
=====================

Caso de uso *"Crear propuesta"* de la firma de consultoría:

1. El consultor busca en el área de almacenamiento centralizada
   una propuesta adecuada.
2. Si la encuentra, abre el archivo (y la aplicación de oficina);
   guarda con un nuevo nombre, creando un nuevo archivo.
3. Si no encuentra, abre la aplicación y crea un nuevo archivo.
4. Trabaja con la aplicación.
5. Al finalizar, guarda en el área centralizada.

Para mostrar la **creación de un objeto**, agregue un estereotipo
``«crear»`` al mensaje que genera al objeto. Use *si* (``[…]``)
y *mientras* (``*[…]``) según corresponda.

.. uml::

   @startuml
   allowmixing

   actor Consultor
   object ":GUI"               as GUI
   object ":Deposito"          as DEP
   object ":AplicacionOficina" as APP
   object ":Propuesta"         as P

   Consultor -> GUI : "1: iniciarBusqueda()"
   GUI       -> DEP : "2: buscar()"
   DEP       -> GUI : "3: resultado"
   Consultor -> GUI : "[encontrado] 4.1: abrir(archivo)"
   Consultor -> GUI : "[no encontrado] 4.2: nuevo(archivo)"
   GUI       -> APP : "5: abrirYGuardarComo(propuesta)"
   APP       -> P   : "<<crear>> 6: crearArchivo()"
   Consultor -> GUI : "*[trabajo] 7: usarAplicaciones()"
   GUI       -> APP : "8: usarAplicaciones()"
   APP       -> P   : "9: modificar()"
   Consultor -> GUI : "[completado] 10: cerrarYGuardar()"
   GUI       -> APP : "11: cerrarYGuardar()"
   APP       -> P   : "12: cerrar()"
   APP       -> DEP : "13: guardar()"
   APP       -> GUI : "14: completado()"
   @enduml

----
