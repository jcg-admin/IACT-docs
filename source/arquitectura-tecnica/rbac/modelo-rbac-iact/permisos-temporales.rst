.. _modelo-rbac-iact-permisos-temporales:

==========================================
Modelo RBAC IACT — Permisos Temporales
==========================================

6. PERMISOS TEMPORALES
======================



6.1 Concepto
------------


Una función puede asignarse **temporalmente** con:
- **Justificación obligatoria** (mín 20 caracteres)
- **Fecha de vencimiento** (máx 6 meses)

**Casos de uso:**
- Cobertura de vacaciones
- Proyectos temporales
- Pruebas controladas


6.2 Reglas
----------


1. **Justificación:** Mínimo 20 caracteres
2. **Vencimiento:** Máximo 6 meses desde asignación
3. **Auditoría:** Registro obligatorio (CNST-009)
4. **Renovación:** Requiere nueva justificación
5. **Revocación:** Automática al vencer o manual


6.3 Ejemplo
-----------



.. code-block:: python

 # Asignar export_csv temporalmente por 3 meses
 UserFunctionAssignment.objects.create(
 user=user,
 function=Function.objects.get(function_id='RPT-004'), # export_csv
 assigned_by=admin,
 justification="Cobertura vacaciones analista principal",
 expiration_date=date.today + timedelta(days=90)
 )


