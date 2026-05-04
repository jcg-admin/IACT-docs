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



.. note::

 Los detalles de implementacion de este componente estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.
