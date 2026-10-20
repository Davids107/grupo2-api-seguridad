# Pendientes del QA — Grupo 2 (Update No. 1 · 17-oct-2026)

Resumen del informe de Allison Espaderos (QA) y quién corrige cada cosa. Cada quien toca **solo sus archivos**. Los números G2-xx son los escenarios del plan de QA.

Prioridad: **Alta** → **Media** → **Baja**. El Planner de Allison tiene tres tareas (Alta, Media y Baja) con puntos por escenario; están sin responsable y con fecha 21/10. El detalle está en `GUIA_GRUPO2.md`, sección 8.

## Lo más urgente (crítico)

El middleware de usuarios y roles todavía lee el encabezado `usuario-actual` y una lista JSON temporal, en vez del JWT. Por eso cualquiera puede hacerse pasar por administrador (G2-10) y el login real no sirve para entrar a `/users` ni `/roles`. Esto bloquea G2-06, 08, 09, 17, 37 y 38.

## Estado al 20-oct

- **Randy** ya lee el token Bearer y agregó `GET /users/{id}` con 404, pero sigue buscando al usuario en la lista JSON y no en la base. Con eso, un token del login real todavía no entra a `/users`. Falta: leer desde la base, revisar que la sesión no esté revocada y usar el rol `admin`.
- **David** subió el import de `files` en `main.py` y las dependencias `puremagic` y `email-validator`.
- **Siguen pendientes:** logout, `/me`, bloqueo, auditoría, paginación y `test_errores.py`.

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

### Robert · Persona 5 · Base del proyecto e integración
| Semana | Qué toca | Estado |
|-|-|-|
| 1 | `main.py` conecta `error_handler`; `GUIA_GRUPO2.md` en la carpeta del grupo | ✅ Hecho |
| 2 | `main.py` con los routers `roles` y `files` (G2-18 a G2-22) | ✅ Hecho. `/me` se engancha solo cuando Daniel suba `me_router`. |
| 3 | `.env.example`, `requirements.txt`, `database.py` con `PyMySQL` y `DATABASE_URL` | ✅ Ya estaba; se agregó la opción de la base compartida. Falta probar la conexión real con tu `.env`. |
| 4 | `README.md` con títulos y tablas; `conftest.py` | ✅ README rehecho; `conftest.py` con guarda para no tocar la base compartida. ⚠️ `pytest` completo aún se interrumpe por `test_errores.py` (Edgar). |
| QA | G2-35 sin credenciales | PASS. Para mantenerlo: `grupo-2.txt` y `.env` nunca se suben; `semilla_local.py` se saca del repo. |
| QA | G2-33 documentación | Pendiente: revisar `/api/v1/docs` cuando todos terminen. |

## Estado de los escenarios (resumen)

- **PASS:** G2-02, 03, 04, 13, 14, 15, 16, 23, 24, 25, 27, 28, 29, 30, 32, 35.
- **Bloqueados o fallan:** G2-05, 06, 07, 08, 09, 10, 12, 37, 38.
- **Parcial:** G2-11, 17, 26, 33, 36.
- **No cumple / pendiente:** G2-34 (bloqueo), G2-31 (paginación), G2-18 a G2-22 (archivos).
- **En proceso:** G2-01 (falta probar el JWT en endpoints protegidos).

## Cómo corregirlo (archivos ya probados en la carpeta `solucion_qa/`)

Cada archivo de `solucion_qa/` es una versión corregida y **probada**: con ellos pasan las 12 pruebas nuevas de `tests/test_seguridad_qa.py` (G2-04, 05, 06, 07, 08, 09, 10, 12, 17, 18 a 22, 25, 27, 28, 31, 34, 36, 37 y 38). Son una **referencia**: cada persona los copia en **su propio archivo**, los revisa, los entiende y los sube con **su propia cuenta** (así se cuenta su commit).

**Pasos para todos:** (1) Pull de `grupo-2`. (2) Copiar la versión de `solucion_qa/` a su archivo. (3) Correr `python -m pytest`. (4) Probar que levante la API. (5) Commit con mensaje claro, Push y avisar en el grupo.

**Orden recomendado** (unos dependen de otros): Edgar (`registro.py`) → Randy (`auth_middleware.py`) → Daniel (`auth.py`) → Randy (`users.py`, `roles.py`) → Fulvio (`files.py`) → Robert (`main.py`, `config.py`, `.env.example`, `.gitignore`).

| Quién | Archivo | Qué cambia |
|-|-|-|
| Edgar | `utils/registro.py` | `registrar_accion()` usaba columnas que no existen (`entidad`, `entidad_id`, `ip`). La tabla `auditoria` tiene `tabla`, `registro_id` e `ip_origen`. Hoy **no guarda nada** y el conteo de intentos siempre da 0. |
| Edgar | `tests/test_errores.py` | Nombre de la función (`register_error_handlers`) y tabla falsa de auditoría con las columnas reales. |
| Randy | `middleware/auth_middleware.py` | Lee el token Bearer, valida firma, vencimiento y sesión no revocada; 401 si falla, 403 si no tiene rol. |
| Randy | `routers/users.py`, `routers/roles.py` | Pasan a la base; `GET /users/{id}` con 404; paginación; roles con los códigos del Grupo 1 (`admin`, `teacher`…); 401, 403, 404 y 409 documentados. |
| Daniel | `routers/auth.py` | `POST /auth/logout`, `GET /me`, bloqueo de 5 intentos por 15 minutos, auditoría y 422 con campos vacíos. |
| Fulvio | `routers/files.py` | Token obligatorio, archivo guardado con nombre aleatorio, `GET /files/{id}` solo para el autor o un administrador, sin salir de la carpeta. |
| Robert | `main.py`, `config.py`, `.env.example`, `.gitignore` | Incluir `auth.me_router` (**solo después de que Daniel suba `auth.py`**) y la variable `UPLOAD_DIR`. |

**Importante:**
- El código del rol en la base es `admin` (no `administrador`). Ya está alineado en la solución.
- Al crear usuarios el cuerpo ahora lleva `correo`, `password`, `nombres`, `apellidos` y `rol` (la base exige nombres y apellidos).
- Después de subir todo, la lista JSON de prueba (`datos_prueba/usuarios_prueba.json`) ya no se usa y se puede borrar.

### Pendiente de decidir con el PM (Edgar)
El `error_handler.py` responde `{"status", "error", "meta"}` y `details` como lista, pero el CONTRATO_COMUN pide `{"error": {"code", "message", "details": {}}}`. Por eso fallan 7 pruebas de `test_errores.py`. Hay que decidir si se cambia el manejador o el contrato; el QA ya dio PASS (G2-30) al formato actual.

### Notas de integración (Robert)
- `models.py` coincide con el diagrama del Grupo 1 (G2_Autenticacion.pdf): usuario, rol, permiso, usuario_rol, rol_permiso, sesion_token, archivo y auditoría.
- El Grupo 1 todavía no subió su script SQL (solo diagramas). Falta probar contra MariaDB real.
- `semilla_local.py` está en el repo aunque dice "NO SE SUBE" y trae una clave de demostración. Para G2-35 conviene sacarlo del repo y agregarlo al `.gitignore`.

## Fechas

Semana 2 · martes 20-oct · Semana 3 · martes 27-oct · Semana 4 · martes 03-nov · Semana 5 · martes 10-nov (revisión de los 36 escenarios y PR `grupo-2 → main`, solo Daniel).

*Nota: el resumen sale de los PDF del QA (Lista inicial, Updt_1 e Informe no. 1) y del Planner de Allison.*
