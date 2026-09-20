# Backend Grupo 2 - API y Seguridad (Semana 1)

Ejemplo mínimo de login / logout / me para probar el flujo de autenticación.

## Cómo correrlo

1. Instalar dependencias:
   ```
   npm install
   ```
2. Copiar el archivo de variables de entorno:
   ```
   cp .env.example .env
   ```
   Y editar `.env` con sus propios valores.
3. Levantar el servidor:
   ```
   npm start
   ```
4. Probar que responde:
   http://localhost:3000/api/v1/health

## Usuario de prueba

- Correo: `admin@example.com`
- Contraseña: `Admin123!`

(Está guardado en `db.js` solo con fines de prueba, ya con su contraseña
hasheada con bcrypt. Deben reemplazar `db.js` por la conexión real a la
base de datos del Grupo 1 antes de la entrega final.)

## Endpoints de esta semana

- `POST /api/v1/auth/login` — body: `{ "email": "...", "password": "..." }`
- `POST /api/v1/auth/logout` — requiere header `Authorization: Bearer <token>`
- `GET  /api/v1/me` — requiere header `Authorization: Bearer <token>`

## Pendiente para las próximas semanas

- Conectar `db.js` a la base de datos real (esquema del Grupo 1).
- Roles y permisos (Edgar).
- Middleware de validación reutilizable y utilidades de paginación/filtros (Randy).
- Servicio de archivos (todo el equipo).
- Especificación OpenAPI y colección de pruebas.
