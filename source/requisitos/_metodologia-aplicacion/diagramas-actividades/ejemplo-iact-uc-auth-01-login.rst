Ejemplo IACT — UC_AUTH_01 (Login)
---------------------------------

.. uml::

   @startuml
   start
   :Recibir credenciales;
   :Validar usuario en LDAP;
   if (credenciales validas?) then ([si])
     if (sesion previa activa?) then ([no])
       :Crear sesion (CNST_002);
       :Registrar acceso en AuditLog (CNST_025);
       stop
     else ([si])
       :Cerrar sesion previa;
       :Crear sesion nueva;
       stop
     endif
   else ([no])
     :Incrementar contador throttling (CNST_011);
     :Registrar intento fallido;
     stop
   endif
   @enduml
