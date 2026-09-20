// routes/auth.js
// POST /api/v1/auth/login
// POST /api/v1/auth/logout
// GET  /api/v1/me

const express = require("express");
const bcrypt = require("bcryptjs");
const jwt = require("jsonwebtoken");
const { buscarUsuarioPorEmail } = require("../db");
const { requireAuth } = require("../middleware/auth");

const router = express.Router();

// --- POST /api/v1/auth/login ---
router.post("/login", (req, res, next) => {
  try {
    const { email, password } = req.body;

    if (!email || !password) {
      return res.status(422).json({
        error: {
          code: "VALIDATION_ERROR",
          message: "Faltan campos requeridos.",
          details: {
            email: !email ? "El correo es requerido." : undefined,
            password: !password ? "La contraseña es requerida." : undefined,
          },
        },
      });
    }

    const usuario = buscarUsuarioPorEmail(email);

    // Mismo mensaje genérico tanto si el usuario no existe como si la
    // contraseña es incorrecta, para no revelar cuál de los dos falló.
    const credencialesInvalidas = () =>
      res.status(401).json({
        error: { code: "INVALID_CREDENTIALS", message: "Correo o contraseña incorrectos." },
      });

    if (!usuario) return credencialesInvalidas();

    const contrasenaValida = bcrypt.compareSync(password, usuario.passwordHash);
    if (!contrasenaValida) return credencialesInvalidas();

    const token = jwt.sign(
      { id: usuario.id, email: usuario.email, roles: usuario.roles },
      process.env.JWT_SECRET,
      { expiresIn: "2h" }
    );

    // Nunca se devuelve el passwordHash en la respuesta.
    res.status(200).json({
      token,
      user: { id: usuario.id, email: usuario.email, roles: usuario.roles },
    });
  } catch (err) {
    next(err);
  }
});

// --- POST /api/v1/auth/logout ---
// Con JWT sin estado, "cerrar sesión" normalmente significa que el
// cliente descarta el token. Aquí solo confirmamos la operación.
router.post("/logout", requireAuth, (req, res) => {
  res.status(200).json({ message: "Sesión cerrada correctamente." });
});

module.exports = router;

// --- GET /api/v1/me ---
// Se exporta aparte porque va montado en /api/v1, no en /api/v1/auth
module.exports.meHandler = (req, res) => {
  res.status(200).json({ user: req.user });
};
