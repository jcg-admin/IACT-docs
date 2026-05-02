.. _raci-rbac-iact-convenciones:

================================================
RACI RBAC IACT — Convenciones y Mantenimiento
================================================

7. Convenciones de uso
======================

7.1 Conflictos R/A
------------------

Si la misma persona/rol aparece como **R** y **A** para una funcion,
es valido (ejecuta + es accountable). Pero **A es unico**: no
puede haber dos roles distintos con A para la misma funcion.

7.2 Cambios al catalogo
-----------------------

Cualquier cambio al catalogo de funciones, grupos o reglas SoD
requiere:

1. Aprobacion del **TLB** (Accountable global del modelo).
2. Consulta a **AdmT** (DevSecOps, impacto tecnico).
3. Consulta a **Aud** (impacto en auditoria/compliance).
4. Notificacion a **Comp** tras el cambio.

Per :doc:`/normativa/gobernanza/adr-gob-009-rbac-modelo-conceptual`
y :doc:`/normativa/restricciones/cnst-029-rbac-modelo-plano`.

7.3 Permisos excepcionales (CNST-031)
-------------------------------------

Maximo **6 meses** de duracion. Renovacion requiere nueva
aprobacion **AdmT** + **TLB** + auditoria.

----

9. Mantenimiento
================

Esta matriz se actualiza cuando:

- Se agrega/elimina una funcion del catalogo.
- Se agrega/elimina un grupo predefinido.
- Se agrega/modifica una regla SoD.
- Cambia un stakeholder canonico.

**Owner del mantenimiento:** TLB (Tech Lead Backend).

----

10. Fundamento documental
=========================

Las asignaciones R/A/C/I de esta matriz se fundamentan en los
"Actor Tipico" + "Proposito" de cada grupo AGR documentados en
:doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index` § 4.1
(catalogo de los 10 grupos predefinidos del modelo v5.2.1):

.. list-table::
 :header-rows: 1
 :widths: 12 28 60

 * - AGR
   - Actor Tipico
   - Proposito (per modelo v5.2.1 § 4.2)
 * - AGR-001
   - Operador
   - Usuario basico que solo visualiza informacion.
 * - AGR-002
   - Analista
   - Analista que puede aplicar filtros pero no exportar.
 * - AGR-003
   - Supervisor
   - Supervisor con capacidad de configurar alertas propias.
 * - AGR-004
   - Data Analyst
   - Analista autorizado para exportar con limites CNST-007.
 * - AGR-005
   - Gestor Alertas
   - Gestor de alertas de equipo/departamento.
 * - AGR-006
   - Admin Usuarios
   - Administracion completa de identidades.
     **SoD:** NO puede tener funciones de AGR-008 (auditoria).
 * - AGR-007
   - Admin Permisos
   - Administracion de RBAC.
 * - AGR-008
   - Auditor
   - Solo auditoria. **SoD:** restriccion declarada en SOD-001/002/003.
 * - AGR-009
   - Admin Pipeline
   - Administracion de ETL.
 * - AGR-010
   - Sysadmin
   - Administracion tecnica del sistema.

**Razones de la R/A elegida en este documento:**

- ``A`` (Accountable) global = TLB porque es el owner unico del
  modelo conceptual (per :doc:`/normativa/gobernanza/adr-gob-009-rbac-modelo-conceptual`).
- ``R`` (Responsible) por funcion siguen el grupo AGR cuyo
  Proposito declarado en v5.2.1 incluye esa funcion. Por ejemplo:

  - ``view_reports`` (RPT-001): R = Op (incluye AGR-002
    "Analista que puede aplicar filtros pero no exportar" + AGR-003
    "Supervisor" + AGR-004 "Data Analyst") y AdmNT (AGR-006 que
    para administracion ve reportes propios).
  - ``view_audit_log`` (AUD-001): R = Aud unico porque AGR-008
    tiene SoD declarado contra otros admin groups
    (per :doc:`/normativa/restricciones/cnst-030-reglas-de-separacion-de-funciones-sod`).
  - ``view_separation_rules`` (ACC-005): R = AdmT, C = AdmNT/Aud
    porque modificar reglas SoD afecta directamente la
    administracion no-tech (y es auditable).

**Trazabilidad a fuente legacy del catalogo de grupos:**

- :doc:`/gestion/evidencia/rbac-historia/analisis-errores-modelo-rbac-v5-2-0`
  documenta el origen del nombre ingles canonico de cada grupo
  (corregido de espanol en v5.2.0).
- :doc:`/gestion/evidencia/rbac-historia/modelo-rbac-v4-0-roles-jerarquicos-deprecado`
  documenta los "bundles" v4.0 (10 predefinidos) que dieron
  origen a los AGR-001..010 vigentes.
