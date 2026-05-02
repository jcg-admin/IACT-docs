.. _raci-rbac-iact-stakeholders:

===================================
RACI RBAC IACT — Stakeholders
===================================

1. Convencion RACI
==================

.. list-table::
 :header-rows: 1
 :widths: 12 88

 * - Codigo
   - Significado
 * - **R**
   - **Responsible** — ejecuta la funcion (rol que la realiza)
 * - **A**
   - **Accountable** — autoridad final / owner de la spec de la funcion
 * - **C**
   - **Consulted** — consultado antes de cambios a la funcion
 * - **I**
   - **Informed** — notificado tras cambios o ejecucion

**Regla unica per funcion:** una sola **A** (accountable). Multiples
**R**, **C**, **I** permitidos.

----

2. Stakeholders identificados
=============================

Los 6 stakeholders agrupan los **10 Actores Tipicos** documentados
en :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index` § 4.1
(catalogo de grupos AGR-001..010). El mapeo es 1-N: un
stakeholder puede agrupar multiples Actores Tipicos.

.. list-table::
 :header-rows: 1
 :widths: 22 12 36 30

 * - Stakeholder
   - Codigo
   - Descripcion
   - Mapeo a Actor Tipico v5.2.1 / Grupo AGR
 * - Admin no-tech
   - **AdmNT**
   - Asigna agrupadores predefinidos a usuarios. Perfil
     RH/Ops sin background tecnico.
   - "Admin Usuarios" -> AGR-006 (``user_admin_group``)
 * - Admin tecnico (DevSecOps)
   - **AdmT**
   - Crea grupos custom, define funciones, gestiona permisos
     excepcionales.
   - "Admin Permisos" -> AGR-007 (``permission_admin_group``);
     "Admin Pipeline" -> AGR-009 (``pipeline_admin_group``);
     "Sysadmin" -> AGR-010 (``system_admin_group``)
 * - Operador final
   - **Op**
   - Consume funciones operativas via su asignacion de grupo.
   - "Operador" -> AGR-001 (``basic_operator_group``);
     "Analista" -> AGR-002 (``report_viewer_group``);
     "Supervisor" -> AGR-003 (``quality_supervisor_group``);
     "Data Analyst" -> AGR-004 (``data_exporter_group``);
     "Gestor Alertas" -> AGR-005 (``alert_manager_group``)
 * - Tech Lead Backend
   - **TLB**
   - Owner tecnico de la spec del modelo RBAC + implementacion
     backend (framework web + base de datos). Accountable global del modelo.
   - Externo a los grupos AGR (rol de gobernanza tecnica)
 * - Equipo de Auditoria
   - **Aud**
   - Consulta logs RBAC + reglas SoD. Aplica restriccion SoD
     declarada en v5.2.1 § 4.2 (NO puede tener funciones de
     otros admin groups).
   - "Auditor" -> AGR-008 (``auditor_group``)
 * - Equipo Compliance
   - **Comp**
   - Notificado de cambios al modelo RBAC para reportes
     normativos (SOX, ISO 27001).
   - Externo a los grupos AGR (rol stakeholder regulatorio)

