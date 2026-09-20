// db.js
// Aquí va la conexión real a la base de datos, usando el esquema y las
// migraciones que entregue el Grupo 1. Este archivo es solo un ejemplo
// de estructura para que la reemplacen por su driver real (por ejemplo
// "pg" para PostgreSQL o "mysql2" para MySQL).

require("dotenv").config();

// Ejemplo con PostgreSQL (instalar con: npm install pg)
// const { Pool } = require("pg");
// const pool = new Pool({
//   host: process.env.DB_HOST,
//   port: process.env.DB_PORT,
//   user: process.env.DB_USER,
//   password: process.env.DB_PASSWORD,
//   database: process.env.DB_NAME,
// });
// module.exports = pool;

// Mientras se conecta la base de datos real, usamos una "base de datos"
// en memoria SOLO para probar el flujo de login de la Semana 1.
// IMPORTANTE: reemplazar esto por consultas reales a la base de datos.
const bcrypt = require("bcryptjs");

const usuariosDeEjemplo = [
  {
    id: 1,
    email: "admin@example.com",
    // Contraseña real: "Admin123!" -> guardada como hash, nunca en texto plano
    passwordHash: bcrypt.hashSync("Admin123!", 10),
    roles: ["admin"],
  },
];

function buscarUsuarioPorEmail(email) {
  return usuariosDeEjemplo.find((u) => u.email === email) || null;
}

module.exports = { buscarUsuarioPorEmail };
