Proceso de creación de un documento
===================================

Actividades para utilizar una aplicación de oficina y crear un
documento:

1. Abrir la aplicación para procesamiento de textos.
2. Crear un archivo.
3. Guardar el archivo con un nombre único en una carpeta.
4. Teclear el documento.
5. Si se necesitan ilustraciones, abrir la app relacionada,
   generar los gráficos y colocarlos en el documento.
6. Si se necesita una hoja de cálculo, abrir la app relacionada,
   crear la hoja y colocarla.
7. Guardar el archivo.
8. Imprimir el documento.
9. Salir de la aplicación.

.. uml::

   @startuml

   start
   :Abrir procesador de textos;
   :Crear archivo;
   :Guardar con nombre único;
   :Teclear documento;
   if ([necesita ilustraciones]) then (sí)
     :Abrir app de gráficos;
     :Generar gráficos;
     :Insertar en documento;
   endif
   if ([necesita hoja de cálculo]) then (sí)
     :Abrir app de hoja de cálculo;
     :Crear hoja;
     :Insertar en documento;
   endif
   :Guardar archivo;
   :Imprimir documento;
   :Salir de la aplicación;
   stop
   @enduml
