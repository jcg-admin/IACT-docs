Ejemplo IACT — Carga ETL paginada (CNST_006/008)
------------------------------------------------

.. uml::

   @startuml
   start
   :Inicializar offset = 0;
   :Definir tamano_lote;
   while (existen mas filas?) is ([si])
     :Leer lote desde BD operativa (readonly);
     :Transformar registros;
     :Insertar en BDAnalytics;
     :Avanzar offset;
     if (ventana ETL agotada?) then ([si])
       :Marcar carga como incompleta;
       break
     else ([no])
     endif
   endwhile ([no])
   :Cerrar carga;
   :Registrar resumen en AuditLog;
   stop
   @enduml
