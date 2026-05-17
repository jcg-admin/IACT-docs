Creación de un objeto en la secuencia
=====================================

Con frecuencia un programa orientado a objetos debe crear un
objeto. En términos del software, una **clase es una plantilla
para crear un objeto** (como un molde de galletas para crear una
galleta).

¿Cómo representaría la creación de un objeto cuando represente
una secuencia de interacciones entre objetos?

Caso de uso *"Crear una propuesta"* de la LAN en una firma de
consultoría. Si damos por hecho que el consultor ya ha iniciado
una sesión, la secuencia es:

1. El consultor querrá volver a utilizar partes de una propuesta
   existente y busca en un área centralizada de la red.
2. Si el consultor encuentra una propuesta adecuada, abre el
   archivo y guarda con un nuevo nombre, creando un archivo
   nuevo.
3. Si no encuentra, abre la aplicación de oficina y crea un
   archivo para la propuesta.
4. Al trabajar, utiliza las aplicaciones del software integrado.
5. Cuando finaliza, guarda en el área de almacenamiento
   centralizada.

Esta secuencia trae consigo el uso de **si** y de un ciclo
**mientras**.

Cuando una secuencia da por resultado *la creación de un objeto*,
tal objeto se representa como un rectángulo con nombre. **No** se
coloca en la parte superior; se coloca a lo largo de la
dimensión vertical, de modo que su ubicación corresponda al
momento en que se cree.

El mensaje que crea al objeto se nombra ``Crear()`` (o se usa el
estereotipo ``«Crear»``). En un lenguaje OO, una **operación
constructor genera un objeto**.

En el caso del *mientras*, el control de flujo se representa
colocando la condición entre corchetes con un asterisco (``*``)
antes del primer corchete.

.. note:: Este ejemplo representa una abstracción

 He omitido detalles que no nos competen en lo particular.
 Primero, obvié los detalles de la LAN. La GUI es un objeto en
 el diagrama de secuencias, y no he incluido toda la complejidad
 del caso de uso *"Teclazo"* del ejemplo anterior — los detalles
 de la interacción de la GUI con el sistema operativo, la CPU y
 el monitor **no son importantes en este caso**.

.. uml::

   @startuml

   actor Consultor
   participant ":AreaCentral" as A
   participant ":AppOficina" as App
   participant ":Propuesta" as P

   Consultor -> A : buscarPropuesta()

   alt [propuesta encontrada]
     Consultor -> App : abrir(propuestaExistente)
     activate App
     App -> P ** : Crear(nuevoNombre)
     activate P
   else [no encontrada]
     Consultor -> App : abrir()
     activate App
     App -> P ** : Crear()
     activate P
   end

   loop *[mientras se trabaja en la propuesta]
     Consultor -> App : editar()
     App -> P : actualizar()
   end

   Consultor -> A : guardar(P)
   deactivate P
   deactivate App
   @enduml
