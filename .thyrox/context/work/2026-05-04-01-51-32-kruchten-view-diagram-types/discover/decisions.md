```yml
created_at: 2026-05-04 01:51:32
project: IACT-docs
work_package: 2026-05-04-01-51-32-kruchten-view-diagram-types
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Aprobado
```

# Decisiones autonomas — kruchten-view-diagram-types

Decisiones tomadas durante la restructuracion de las vistas de
Kruchten y la definicion/implementacion de los tipos de diagrama
correctos por vista.

---

## D-KRUCHTEN-001 — Eliminar directorio uc/ como wrapper de vistas

**Decision:** Los 6 directorios de vistas Kruchten se mueven de
`arquitectura-tecnica/uc/{View}/` directamente a
`arquitectura-tecnica/{View}/`.

**Antes:**
```
arquitectura-tecnica/uc/DeployView/
arquitectura-tecnica/uc/DesignView/
...
```

**Despues:**
```
arquitectura-tecnica/DeployView/
arquitectura-tecnica/DesignView/
...
```

**Justificacion:** El nivel intermedio `uc/` no agrega valor semantico.
Las vistas son parte de la arquitectura tecnica, no solo de los UCs.
Ademas, `arquitectura-tecnica/index.rst` ya tenia un toctree de nivel
superior — el wrapper `uc/` era redundante.

**Impacto:** `vistas-kruchten.rst` renombrado desde `uc/index.rst`.
`arquitectura-tecnica/index.rst` actualizado con la nueva ruta.
Subdominio en metadata actualizado: `uc/DeployView` → `DeployView`.

---

## D-KRUCHTEN-002 — Eliminar prefijo uc- de archivos dentro de vistas

**Decision:** Los archivos dentro de los directorios de vista se
renombran de `uc-{mod}-{nn}.rst` a `{mod}-{nn}.rst`.

**Ejemplos:**
```
DeployView/uc-acc-01.rst → DeployView/acc-01.rst
DomainModel/uc-auth-01.rst → DomainModel/auth-01.rst
ProcessView/uc-inc-rpt-01.rst → ProcessView/inc-rpt-01.rst
```

**Justificacion:** El prefijo `uc-` pertenece exclusivamente a los
archivos de especificacion de casos de uso en `requisitos/casos-uso/`.
Los archivos en las vistas Kruchten son documentos arquitectonicos,
no especificaciones de UC. Usar el mismo prefijo generaba confusion
semantica sobre el tipo de documento.

**Impacto:** 480 archivos renombrados (80 por vista × 6 vistas).
Toctrees en los 6 index.rst actualizados.

---

## D-KRUCHTEN-003 — Tipos de diagrama canonicos por vista (5+1)

**Decision:** El modelo de Kruchten implementado en IACT usa 6 vistas
con los siguientes tipos de diagrama UML canonicos:

| Vista | Diagrama Principal | Diagrama Secundario |
|-------|-------------------|---------------------|
| DomainModel | Clases (conceptual) | Estados |
| DesignView | Secuencia | Comunicacion |
| ImplementationView | Componentes | — |
| UseCaseView | Casos de Uso | — |
| ProcessView | Actividades | — |
| DeployView | Despliegue | — |

**Justificacion por vista:**

- **DomainModel** — El diagrama de clases captura las entidades y sus
  relaciones estáticas. El diagrama de estados captura el ciclo de vida
  de la entidad principal que el UC manipula. Ambos son necesarios para
  la Vista Logica completa.

- **DesignView** — El diagrama de secuencia muestra el flujo temporal
  entre participantes. El diagrama de comunicacion muestra los mismos
  intercambios con mensajes numerados entre objetos (perspectiva
  estructural). Son complementarios: secuencia = CUANDO, comunicacion
  = QUIEN con QUIEN.

- **ImplementationView** — El diagrama de componentes muestra la
  organizacion del codigo (paquetes, modulos, interfaces). Suficiente
  para esta vista.

- **UseCaseView** — El diagrama UC con actores RBAC es el diagrama
  central del modelo 4+1. Une todas las demas vistas.

- **ProcessView** — El diagrama de actividades (con swimlanes o
  particiones) modela el flujo de control, bifurcaciones y
  concurrencia.

- **DeployView** — El diagrama de despliegue muestra los nodos fisicos
  (o virtuales), artefactos desplegados y canales de comunicacion.

**Impacto:** 80 archivos en DomainModel reciben diagrama de estados.
80 archivos en DesignView reciben diagrama de comunicacion. DesignView
y DeployView corrigen nombres de participantes/nodos.

---

## D-KRUCHTEN-004 — Participantes en diagramas de secuencia/comunicacion usan roles semanticos

**Decision:** Los diagramas de secuencia (DesignView) y de comunicacion
(DesignView) usan NOMBRES DE ROL semanticos para los participantes/
objetos — NO nombres de tecnologia concreta.

**Mapeo de transformacion:**

| Nombre tecnologico (PROHIBIDO) | Nombre de rol (CORRECTO) |
|-------------------------------|--------------------------|
| `React Frontend` | `Interfaz de {Modulo}` |
| `Django API` | `Servicio de {Modulo}` |
| `MariaDB` | `Almacen de Datos` |
| `MySQL` | `Almacen de Datos` |
| `Redis` | `Cache de Sesiones` |
| `Celery` | `Procesador Asincrono` |

**Nombres de rol por modulo:**

| Modulo | Interfaz | Servicio |
|--------|----------|---------|
| auth | Interfaz de Acceso | Servicio de Autenticacion |
| usr | Interfaz de Usuarios | Servicio de Usuarios |
| acc | Interfaz de Control | Servicio de Acceso |
| perm | Interfaz de Permisos | Servicio de Permisos |
| rpt | Interfaz de Reportes | Servicio de Reportes |
| alr | Interfaz de Alertas | Servicio de Alertas |
| pip | Interfaz de Pipeline | Servicio de Pipeline |
| aud | Interfaz de Auditoria | Servicio de Auditoria |
| log | Interfaz de Logs | Servicio de Logs |
| opr | Interfaz de Operador | Servicio de Operador |
| sup | Interfaz de Supervision | Servicio de Supervision |
| cli | Interfaz de Llamadas | Servicio de Llamadas |

**Justificacion:** Los diagramas de interaccion (secuencia, comunicacion)
describen LO QUE OCURRE entre roles funcionales, no entre sistemas
concretos. Si el stack tecnico cambia (e.g., React → Vue), los diagramas
no deberian cambiar. La tecnologia concreta pertenece a los diagramas de
despliegue e implementacion.

**Impacto:** 80 archivos en DesignView corregidos. 80 archivos en
DeployView no se afectan por esta regla (alli se permiten nombres reales).

---

## D-KRUCHTEN-005 — DeployView usa arquitectura Apache + mod_wsgi (NO nginx/gunicorn)

**Decision:** Los diagramas de despliegue (DeployView) reflejan la
arquitectura canonica IACT:

```
Cliente Web → Apache + mod_wsgi → Django App → MariaDB
                                             → Redis  (solo AUTH)
```

**Nodos canonicos:**
- `node "Cliente Web"` — navegador del usuario
- `node "Apache + mod_wsgi" { artifact "Django App" }` — servidor web
- `database "MariaDB"` — base de datos IVR + operacional
- `node "Redis"` — cache de sesiones (solo modulos AUTH)

**Tecnologias PROHIBIDAS en diagramas IACT:**
- nginx — IACT no usa nginx
- gunicorn — IACT usa mod_wsgi, no gunicorn
- Docker / K8s — IACT usa Vagrant + Apache (CNST_019)

**Justificacion:** La arquitectura de despliegue real del proyecto IACT
(documentada en index.rst, plan-documentacion-uc.rst, diagramas-
componentes.rst) usa Vagrant + Apache + mod_wsgi. Usar nginx o gunicorn
en los diagramas genera inconsistencia con la arquitectura real.

**Impacto:** 80 archivos en DeployView reemplazan el diagrama de 3 nodos
simple (`React Frontend → Django API → MariaDB`) con el patron correcto
usando Apache + mod_wsgi.

---

## D-KRUCHTEN-006 — Estado de implementacion: 4 vistas completas, 2 con gap

**Decision:** Al inicio de este WP, el estado de los 480 archivos de
vistas era:

| Vista | Estado | Gap |
|-------|--------|-----|
| DomainModel | Parcial | Faltaba diagrama de estados |
| DesignView | Parcial | Faltaba diagrama de comunicacion + nombres tecnologicos |
| ImplementationView | Completo | Diagrama de componentes presente |
| UseCaseView | Completo | Diagrama UC con actores RBAC presente |
| ProcessView | Completo | Diagrama de actividades presente |
| DeployView | Incorrecto | Arquitectura incorrecta (nginx-like en lugar de Apache) |

**Accion:** Script `add-diagrams.py` implementa las correcciones en
las 3 vistas que requieren cambios (DomainModel + DesignView + DeployView).
