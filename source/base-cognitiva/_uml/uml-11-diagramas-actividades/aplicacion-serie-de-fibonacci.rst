Aplicación: serie de Fibonacci
==============================

La serie ``1, 1, 2, 3, 5, 8, 13, ...`` se conoce como **serie
de Fibonacci**. Cada número es un *fib*: ``fib(1) = 1``,
``fib(2) = 1``, ``fib(3) = 2``, ... La regla: cada fib (excepto
los dos primeros) es la suma del par anterior.

Imagine que una clase ``Calculadora`` tiene la operación
``calcularFib(n)`` que muestra el enésimo fib.

Variables: ``Contador`` (control), ``Respuesta`` (resultado),
``Respuesta1`` y ``Respuesta2`` (dos fibs anteriores).

.. uml::

   @startuml

   start
   :Respuesta1 := 1;
   :Contador   := 1;
   if ([n = 1]) then (sí)
     :Respuesta := Respuesta1;
     :mostrar(Respuesta, Contador);
     stop
   else ([n > 1])
     :Respuesta2 := 1;
     :Contador := 2;
     if ([n = 2]) then (sí)
       :Respuesta := Respuesta2;
       :mostrar(Respuesta, Contador);
       stop
     else ([n > 2])
       repeat
         :Respuesta := Respuesta1 + Respuesta2;
         :Contador := Contador + 1;
         if ([n = Contador]) then (sí)
           :mostrar(Respuesta, Contador);
           stop
         else ([n > Contador])
           :Respuesta1 := Respuesta2;
           :Respuesta2 := Respuesta;
         endif
       repeat while ([n > Contador])
     endif
   endif
   @enduml
