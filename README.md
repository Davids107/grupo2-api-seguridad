# Grupo 2 — API y Seguridad (Python)

### Proyecto integrador — Programación Web

\---

## 1\. Repositorio

* **Nombre del repo:** `grupo2-api-seguridad`
* Todo el trabajo del equipo de aquí en adelante se hace en el nuevo repo, en Python.

\---

## 2\. Alcance del grupo

Somos el **Grupo 2 (API y Seguridad)**, que al trabajar con 5 grupos en total absorbe también el alcance del Grupo 6 (Administración y Calidad). Esto quiere decir que somos responsables de:

* Autenticación (login, logout, sesión)
* Usuarios y roles
* Catálogos institucionales (sedes, cursos, períodos, modalidades, áreas)
* Notificaciones y auditoría
* Documentación de la API (OpenAPI)
* **Backend y frontend mínimo propio** (no hay grupo dedicado a frontend por lo que se entiende)
* Se entiende que más adelante recibiremos un **CSS general compartido** de otro grupo, que se aplicará sobre nuestra pantalla de login sin cambiar el backend.

\---

## 3\. Stack tecnológico

* **Lenguaje:** Python
* **Framework:** FastAPI
* **Servidor:** Uvicorn
* **Hash de contraseñas:** bcrypt / passlib
* **Base de datos:** por definir con Grupo 1 (mientras tanto, datos de prueba)

\---

## 4\. Estructura del repositorio

```
grupo2-api-seguridad/
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── requirements.txt
│   ├── .env.example
│   ├── routes/
│   │   ├── auth.py
│   │   ├── usuarios.py
│   │   ├── catalogos.py
│   │   └── notificaciones.py
│   └── middleware/
│       ├── auth\_middleware.py
│       └── error\_handler.py
├── frontend-login/
│   └── (pantalla de login)
├── openapi.yaml
└── README.md
```

\---

## 5\. Roles y responsabilidades

|Rol|Archivo(s) que le corresponden|
|-|-|
|**Persona 1**|`routes/auth.py`|
|**Persona 2**|`routes/usuarios.py`, `middleware/auth\_middleware.py`|
|**Persona 3**|`routes/catalogos.py`, `middleware/error\_handler.py`|
|**Persona 4**|`routes/notificaciones.py`, `frontend-login/`|
|**Persona 5**|`main.py`, `database.py`, `requirements.txt`, `.env.example`, `openapi.yaml`, `README.md`|

Cada quien escoge o se le asigna un número. Ese número define su archivo, su tarea y sus instrucciones abajo.

\---

## 6\. Instrucciones detalladas por persona

### Persona 1 — Login y autenticación

**Archivo:** `routes/auth.py`

**Qué hacer:**

1. Crear el endpoint `POST /auth/login` (recibe correo y contraseña)
2. Verificar la contraseña con hash (bcrypt) contra un usuario de prueba mientras no hay base de datos real
3. Generar un token cuando el login sea correcto
4. Crear `POST /auth/logout`
5. Crear `GET /me` (devuelve los datos del usuario dueño del token)

**Si no sabes mucho, investiga:**

* Qué es un hash y cómo funciona bcrypt
* Qué es un token (JWT es el tipo más común)
* Cómo se define una ruta POST en FastAPI

\---

### Persona 2 — Usuarios y roles

**Archivos:** `routes/usuarios.py`, `middleware/auth\_middleware.py`

**Qué hacer:**

1. Crear `GET /usuarios` (listar)
2. Crear `POST /usuarios` (crear usuario nuevo)
3. Crear `PATCH /usuarios/{id}` (editar o desactivar)
4. Definir cómo se guarda el rol de cada usuario (con datos de prueba por ahora)
5. Escribir el middleware que revisa el rol antes de dejar ejecutar una acción (ej. solo administrador puede borrar usuarios)

**Si no sabes mucho, investiga:**

* Qué es un middleware
* Diferencia entre PATCH y PUT
* Cómo proteger una ruta para que solo un rol específico la use

\---

### Persona 3 — Catálogos y formato de errores

**Archivos:** `routes/catalogos.py`, `middleware/error\_handler.py`

**Qué hacer:**

1. Definir el formato uniforme de error (código, mensaje, detalle) — **esto es lo primero que hay que tener listo, todos los demás lo van a usar**
2. Crear el CRUD (GET/POST/PATCH/DELETE) de sedes
3. Repetir el mismo patrón para cursos
4. Repetir para períodos
5. Repetir para modalidades y áreas

**Si no sabes mucho, investiga:**

* Qué es CRUD
* Códigos de estado HTTP (400, 401, 403, 404, 409, 422)
* Cómo estructurar una respuesta de error en JSON

\---

### Persona 4 — Notificaciones, auditoría y pantalla de login

**Archivos:** `routes/notificaciones.py`, `frontend-login/`

**Qué hacer:**

1. Crear `GET /notifications` (listar)
2. Crear `PATCH /notifications/{id}` (marcar como leída)
3. Crear `GET /audit` (historial de cambios, con datos de prueba al inicio)
4. Armar la pantalla simple con dos campos (correo, contraseña) y un botón que llame a `POST /auth/login`
5. Mostrar en pantalla si el login funcionó o no

**Si no sabes mucho, investiga:**

* HTML básico (formulario con inputs)
* Cómo hacer una petición desde una página web a una API (fetch)
* Qué es una auditoría en un sistema

\---

### Persona 5 — Base del proyecto, documentación y coordinación

**Archivos:** `main.py`, `database.py`, `requirements.txt`, `.env.example`, `openapi.yaml`, `README.md`

**Qué hacer:**

1. Crear `requirements.txt` con las librerías (fastapi, uvicorn, bcrypt, etc.)
2. Crear `database.py` con la conexión (datos de prueba mientras Grupo 1 no entrega su esquema)
3. Crear `main.py` que junte los archivos de rutas de las Personas 1-4
4. Documentar en `openapi.yaml` cada endpoint conforme las demás personas los vayan terminando
5. Escribir el `README.md` con instrucciones de instalación
6. Hablar con Grupo 1 sobre el esquema real de usuarios y avisar a los otros grupos cuándo está lista cada parte

**Si no sabes mucho, investiga:**

* Qué es OpenAPI y cómo se documenta un endpoint
* Cómo se conecta Python a una base de datos (SQLAlchemy es lo más común)
* Qué debe llevar un buen README

\---

## 7\. Forma de trabajo

* Cada persona trabaja su parte de forma independiente durante la semana, usando datos de prueba donde haga falta.
* Se sube el avance a GitHub aunque esté incompleto — mejor avance parcial que nada.
* Reunión semanal (30-40 min): cada quien dice qué subió, qué le falta y si tiene dudas. Se prueba que las partes funcionen juntas.
* Cualquier decisión de arquitectura (lenguaje, librerías, estructura) se avisa al grupo completo antes de aplicarla, no después.

..
