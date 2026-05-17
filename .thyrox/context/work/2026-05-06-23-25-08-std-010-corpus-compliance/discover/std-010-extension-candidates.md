```yml
created_at: 2026-05-06 23:35:00
project: IACT-docs
work_package: 2026-05-06-23-25-08-std-010-corpus-compliance
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Borrador
version: 1.0.0
```

# STD-010 — Hallazgos Tier 3: candidatos de extensión

## Trigger

Ejecutor pidió documentar **todos** los hallazgos en este
WP, incluyendo los términos que el ejecutor mencionó como
parte del principio "máquina de gaseosa" pero que **no
están literalmente prohibidos** en STD-010 §3.

## Sección 1 — Universo de términos investigados

| Término | En STD-010 §3 | Apariciones (UC, excl. testing.rst) |
|---|---|---|
| `localStorage` | NO | 14 hits en 7 archivos |
| `sessionStorage` | NO | 0 hits |
| `Frontend\s*\(` (con paréntesis) | Solo `Frontend (React)` | 1 hit (`uc-perm-07/informacion-general.rst:62 — "Frontend (UC_PERM_08)"`) → falso positivo, no es tecnología |
| `Frontend` (palabra sola) | NO (solo `Frontend (React)`) | 103 archivos lo mencionan |
| `Backend` (palabra sola) | NO | 82 archivos lo mencionan |
| `Django` (sin "API") | NO | varias |
| `Django API` | Implícito en STD-010 §4 ejemplo | 0 hits literales |
| `API` (sola) | NO | múltiples |
| `Stripe` / `SendGrid` / `Twilio` | NO | 0 hits |

## Sección 2 — Análisis del término `localStorage`

**14 ocurrencias en archivos en ámbito de STD-010
(excluyendo testing.rst):**

| Archivo | Líneas |
|---|---|
| `auth/uc-auth-01/actores-precondiciones.rst` | 169, 237, 289 |
| `auth/uc-auth-02/actores-precondiciones.rst` | 85, 125, 144 |
| `auth/uc-auth-02/flujo-principal.rst` | 24, 217, 218 |
| `auth/uc-auth-02/informacion-general.rst` | 85 |
| `auth/uc-auth-02/criterios-aceptacion.rst` | 154, 155 |
| `auth/uc-auth-02/diagramas-uml/diagrama-de-actividad.rst` | 59 |
| `auth/uc-auth-02/diagramas-uml/diagrama-de-secuencia.rst` | 36 |

### Discusión

- `localStorage` es una API estándar de la plataforma web
  (WHATWG Web Storage), no una biblioteca de un vendor
  específico (a diferencia de `Redux`, `bcrypt`, `Celery`).
- STD-010 §3.4 lista `Redux Toolkit`, `React Router`, etc.
  pero NO menciona APIs nativas del navegador.
- En el principio "máquina de gaseosa" estricto, sería
  reemplazable por:
  - "almacenamiento local del cliente"
  - "almacén de tokens del cliente"
- Pero el ejecutor escribe textualmente
  ``localStorage.removeItem('access_token')`` como
  comportamiento observable, lo cual está más cerca de un
  contrato técnico que de una decisión de implementación.

### Recomendación

- **No corregir en este WP.** El término no está prohibido
  literalmente.
- Marcar como **candidato T3-1** para discusión futura
  sobre si STD-010 §3.4 debe extenderse con APIs de
  navegador.

## Sección 3 — Análisis del término `Frontend` / `Backend`

**103 archivos mencionan `Frontend`. 82 archivos mencionan
`Backend`.**

### Discusión

- STD-010 §4 da el ejemplo:
  ```
  ' PROHIBIDO
  participant "Frontend\n(React)" as F
  ```
  Es decir: la combinación `Frontend (React)` es prohibida.
- `Frontend` solo (sin la marca de tecnología) es una
  abstracción de capa, no un nombre de producto. Equivale
  a "lado del cliente" / "cliente web".
- STD-010 §3.4 recomienda `Interfaz de Usuario`, pero
  **no prohíbe** `Frontend` sin marca tecnológica.
- En contraste, `Django API` (en §4 ejemplo) sí está
  prohibido — `API` solo no, pero `Django API` sí.

### Decisión interpretativa

| Forma | Interpretación |
|---|---|
| `Frontend` (sin paréntesis) | Permitido (capa abstracta, no tecnología) |
| `Frontend (React)` / `Frontend\n(React)` | Prohibido (STD-010 §4 explícito) |
| `Backend` solo | Permitido (capa abstracta) |
| `Django API` | Prohibido (STD-010 §4 ejemplo) |
| `Django` + módulo concreto (e.g., `Django ORM`) | Prohibido por extensión razonable |

### Hits relevantes

Solo el patrón con paréntesis es claramente prohibido. Tras
revisión:

```
source/requisitos/casos-uso/permissions/uc-perm-07/informacion-general.rst:62:
"**(b) Frontend (UC_PERM_08)**"
```

Este NO es violación: el contenido entre paréntesis es un
identificador de UC (UC_PERM_08), no una tecnología.

**Cero violaciones reales** del patrón
`Frontend (Tecnología)` en el corpus.

## Sección 4 — Resumen Tier 3

| ID | Término | Acción |
|---|---|---|
| T3-1 | `localStorage` (14 hits) | Sin corrección. Marcar como candidato de extensión a STD-010. |
| T3-2 | `Frontend` solo (103 archivos) | Sin corrección. STD-010 §4 solo prohíbe la combinación con marca tecnológica. |
| T3-3 | `Backend` solo (82 archivos) | Sin corrección. Idem. |
| T3-4 | `Frontend (UC_PERM_08)` | Falso positivo (paréntesis contiene identificador, no tecnología). |
| T3-5 | `Stripe` / `SendGrid` | 0 hits. No aplica. |

## Sección 5 — Hallazgo meta: STD-010 §3 incompleto

El ejecutor mencionó como ejemplo: *"Stripe API → Gateway
de Pago"*, *"SendGrid → Servicio de Notificacion"*. STD-010
§3 NO incluye:

- Gateways de pago (`Stripe`, `PayPal`, `MercadoPago`).
- Servicios de notificación (`SendGrid`, `Twilio`,
  `Mailgun`).
- APIs del navegador (`localStorage`, `sessionStorage`,
  `IndexedDB`, `WebSocket`).
- Ejemplo: `Backend` sin tecnología (ambiguo si capa o
  marca).

**Recomendación al ejecutor (post-WP):** abrir WP
*std-010-extension-v1-1-0* para:

1. Ampliar §3.4 con APIs de navegador.
2. Agregar §3.7 "Pagos y Notificaciones".
3. Aclarar §4 sobre `Frontend`/`Backend` solos.

Este WP **no propone modificar STD-010**. Solo lo audita
contra el corpus. La extensión es decisión separada.

## Sección 6 — Cierre del inventario completo

| Tier | Acción en este WP | Hallazgos |
|---|---|---|
| Tier 1 (clear violations) | **Corregir** (C-1..C-4) | H-1..H-7 (ver `std-010-corpus-audit.md`) |
| Tier 2 (testing.rst libre por interpretación) | Sin cambio | T-1..T-3 |
| Tier 3 (no en STD-010 §3) | Sin cambio + documentar | T3-1..T3-5 |

**Total verificado:** 7 violaciones para corregir +
8 hits-libres documentados + ~200 ocurrencias de términos
no prohibidos verificadas y descartadas.

## Refs

- Audit principal: `discover/std-010-corpus-audit.md`.
- STD-010 v1.0.0: :doc:`/normativa/estandares/std-010-vocabulario-abstracto`.
