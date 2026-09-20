// middleware/errorHandler.js
// Middleware común de errores: respuesta uniforme en JSON,
// sin trazas, sin SQL y sin rutas internas del servidor.

function errorHandler(err, req, res, next) {
  const status = err.status || 500;

  // Registro interno (para el equipo, no para el cliente)
  console.error(`[${new Date().toISOString()}] ${req.method} ${req.originalUrl} ->`, err.message);

  res.status(status).json({
    error: {
      code: err.code || "INTERNAL_ERROR",
      message: status === 500 ? "Ocurrió un error interno." : err.message,
      details: err.details || {},
    },
  });
}

module.exports = errorHandler;
