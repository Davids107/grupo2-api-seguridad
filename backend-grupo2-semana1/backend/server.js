// server.js
require("dotenv").config();
const express = require("express");
const cors = require("cors"); // npm install cors
const authRoutes = require("./routes/auth");
const { requireAuth } = require("./middleware/auth");
const errorHandler = require("./middleware/errorHandler");

const app = express();

app.use(cors()); // en producción, restringir a los dominios permitidos
app.use(express.json());

// Todas las rutas de este grupo cuelgan de /api/v1, según el contrato común
app.use("/api/v1/auth", authRoutes);
app.get("/api/v1/me", requireAuth, authRoutes.meHandler);

// Ruta de prueba para confirmar que el servidor está vivo
app.get("/api/v1/health", (req, res) => res.json({ status: "ok" }));

// El middleware de errores va siempre al final
app.use(errorHandler);

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Servidor escuchando en http://localhost:${PORT}`);
});
