8.5 Diagrama de validacion de separacion
==============================

.. uml::
 :caption: Logica de validacion de separacion (PASO 10)

 @startuml

 start

 :Recibir new_function_ids
  + current_function_ids del User;

 :effective_set =
  current_function_ids ∪ new_function_ids;

 :consultar SeparationRule WHERE state='ACTIVE';

 repeat
   :tomar siguiente rule;
   :rule define {function_a, function_b}\no relacion compleja;
   if (rule violada por effective_set?) then (si)
     :raise SeparationRuleViolation\n(rule_id, conflict_pair);
     stop
   else (no)
   endif
 repeat while (mas rules?) is (si) not (no)

 :return OK (set permitido);
 stop

 @enduml
