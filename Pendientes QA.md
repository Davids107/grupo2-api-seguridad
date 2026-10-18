# Pendientes del QA — Grupo 2 (Update No. 1 · 17-oct-2026)

Resumen del informe de Allison Espaderos (QA) y quién corrige cada cosa. Cada quien toca **solo sus archivos**. Los números G2-xx son los escenarios del plan de QA.

Prioridad: **Alta** → **Media** → **Baja**. Las tareas del Planner: Alta, Media, Baja y Update No. 1 (17/10).

## Lo más urgente (crítico)

El middleware de usuarios y roles todavía lee el encabezado `usuario-actual` y una lista JSON temporal, en vez del JWT. Por eso cualquiera puede hacerse pasar por administrador (G2-10) y el login real no sirve para entrar a `/users` ni `/roles`. Esto bloquea G2-06, 08, 09, 17, 37 y 38.

## Por persona

### Daniel · Persona 1 · Autenticación
| Escenario | Prioridad | Qué falta | Archivo |
|-|-|-|-|
| G2-05 | Alta | `POST /auth/logout` no existe. Debe poner `revocado_en` en `sesion_token`. | `routers/auth.py` |
| G2-07 | Media | `GET /me` devuelve 404. Debe dar usuario, roles y permisos. | `routers/auth.py` |
| G2-34 | Baja | El login no usa el contador ni el bloqueo (5 fallos = 15 min). | `routers/auth.py` |
| G2-36 | Baja | El login no llama a `registrar_accion()` ni `registrar_login_fallido()`. | `routers/auth.py` |
| G2-04 | Media | Con campos vacíos devuelve 401; el QA esperaba 422 (revisar con el PM). | `routers/auth.py` |
| G2-33 | Media | Documentar 401 en el login (`responses=`). | `routers/auth.py` |

### Randy · Persona 2 · Usuarios y roles
| Escenario | Prioridad | Qué falta | Archivo |
|-|-|-|-|
| G2-10, 06, 08, 09, 17, 37, 38 | Alta | Leer `Authorization: Bearer` con `verificar_token()` de Daniel y dejar de usar `usuario-actual`. Sin token = 401; sin permiso = 403. | `middleware/auth_middleware.py`, `routers/users.py`, `routers/roles.py` |
| G2-11, 12, 26 | Media | `GET /users/{id}` no existe (da 405); debe dar 404 si no existe. | `routers/users.py` |
| G2-31 | Baja | La lista de usuarios no pagina; usar `paginacion.py` de Edgar. | `routers/users.py` |
| G2-33 | Media | Documentar 401 y 409 en `POST /users`; el ejemplo del 201 es un string. | `routers/users.py` |
| Roles | Media | El código del rol es `admin` en la lista pero `requerir_rol(["administrador"])` en el POST; alinear con el PM. Además `"coordinador "` tiene un espacio al final. | `routers/roles.py` |

### Edgar · Persona 3 · Errores, paginación y registro
| Escenario | Prioridad | Qué falta | Archivo |
|-|-|-|-|
| Pruebas | Alta | `tests/test_errores.py` importa `registrar_manejadores`, pero la función se llama `register_error_handlers`. Hoy `pytest` se interrumpe por esto. | `tests/test_errores.py` |
| G2-36 | Baja | Las funciones de `registro.py` existen, pero nadie las llama; coordinar con Daniel y Randy. | `utils/registro.py` |
| G2-30 | Media | Cumple (PASS). Revisar que 401, 403, 404, 409 y 422 salgan con el formato común. | `middleware/error_handler.py` |

### Fulvio · Persona 4 · Archivos y frontend
| Escenario | Prioridad | Qué falta | Archivo |
|-|-|-|-|
| G2-18 a G2-22 | Alta | Ya existe `POST /files` y valida el tipo real con `puremagic`. Falta probar G2-19 y G2-20 con el QA, descarga `GET /files/{id}` con token (G2-21), y evitar rutas manipuladas (G2-22). | `routers/files.py` |
| G2-18 | Media | `POST /files` aún no exige token (se activa cuando Randy termine el middleware). | `routers/files.py` |
| Pruebas | Media | Falta `tests/test_files.py`. | `tests/test_files.py` |

### Roberto · Persona 5 · Base del proyecto e integración
| Escenario | Prioridad | Qué falta | Archivo |
|-|-|-|-|
| Integración | Alta | `main.py` incluía `files.router` sin importar `files` (la API no arrancaba). **Corregido en la semana 2.** | `main.py` |
| G2-35 | Alta | Sin credenciales en el repo: PASS. Mantener el `.env` fuera del repo. | `.env.example`, `.gitignore` |
| G2-33 | Media | Cuando todos terminen, revisar que `/api/v1/docs` coincida con la API. | `main.py` |
| Semana 3 | Baja | `PyMySQL` y `DATABASE_URL` ya están; falta probar con la base real del Grupo 1. | `database.py`, `.env.example` |
| Semana 4 | Baja | README con títulos y tablas; revisar que `pytest` corra para todos. | `README.md`, `tests/conftest.py` |

## Estado de los escenarios (resumen)

- **PASS:** G2-02, 03, 04, 13, 14, 15, 16, 23, 24, 25, 27, 28, 29, 30, 32, 35.
- **Bloqueados o fallan:** G2-05, 06, 07, 08, 09, 10, 12, 37, 38.
- **Parcial:** G2-11, 17, 26, 33, 36.
- **No cumple / pendiente:** G2-34 (bloqueo), G2-31 (paginación), G2-18 a G2-22 (archivos).
- **En proceso:** G2-01 (falta probar el JWT en endpoints protegidos).

## Fechas

Semana 2 · martes 20-oct · Semana 3 · martes 27-oct · Semana 4 · martes 03-nov · Semana 5 · martes 10-nov (revisión de los 36 escenarios y PR `grupo-2 → main`, solo Daniel).

*Nota: El resumen sale de los PDF del QA (Lista inicial, Updt_1 e Informe no. 1). Falta contrastarlo con el Planner cuando Allison confirme las tareas.*
