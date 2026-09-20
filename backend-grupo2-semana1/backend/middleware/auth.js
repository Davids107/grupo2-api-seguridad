// middleware/auth.js
// Verifica el token enviado en el header Authorization: "Bearer <token>"
// Si es válido, agrega la información del usuario a req.user.

const jwt = require("jsonwebtoken");

function requireAuth(req, res, next) {
  const header = req.headers["authorization"] || "";
  const token = header.startsWith("Bearer ") ? header.slice(7) : null;

  if (!token) {
    return res.status(401).json({
      error: { code: "NO_TOKEN", message: "No se envió un token de autenticación." },
    });
  }

  try {
    const payload = jwt.verify(token, process.env.JWT_SECRET);
    req.user = payload; // { id, email, roles }
    next();
  } catch (err) {
    return res.status(401).json({
      error: { code: "INVALID_TOKEN", message: "El token es inválido o expiró." },
    });
  }
}

module.exports = { requireAuth };
