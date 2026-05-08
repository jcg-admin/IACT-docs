8.5 Diagrama de SoD validation
==============================

.. uml::
 :caption: Logica de validacion SoD (PASO 10)

 @startuml

 start

 :Recibir new_function_ids
  + current_function_ids del User;

 :effective_set =
  current_function_ids ∪ new_function_ids;

 :consultar SoDRule WHERE state='ACTIVE';

 repeat
   :tomar siguiente rule;
   :rule define {function_a, function_b}\no relacion compleja;
   if (rule violada por effective_set?) then (si)
     :raise SoDViolation\n(rule_id, conflict_pair);
     stop
   else (no)
   endif
 repeat while (mas rules?) is (si) not (no)

 :return OK (set permitido);
 stop

 @enduml
