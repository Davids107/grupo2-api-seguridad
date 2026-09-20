// Cambia esta URL si tu backend corre en otro puerto o dominio
const API_BASE = "http://localhost:3000/api/v1";

const formLogin = document.getElementById("formLogin");
const btnLogout = document.getElementById("btnLogout");
const mensaje = document.getElementById("mensaje");
const datosUsuario = document.getElementById("datosUsuario");

// Guardamos el token solo en memoria de la página (variable JS),
// no en el HTML ni en la consola.
let tokenActual = null;

formLogin.addEventListener("submit", async (evento) => {
  evento.preventDefault();

  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value;

  try {
    const respuesta = await fetch(`${API_BASE}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    const data = await respuesta.json();

    if (!respuesta.ok) {
      mostrarError(data.error?.message || "No se pudo iniciar sesión.");
      return;
    }

    tokenActual = data.token;
    mostrarExito(`Sesión iniciada como ${data.user.email}`);
    datosUsuario.textContent = JSON.stringify(data.user, null, 2);

    formLogin.style.display = "none";
    btnLogout.style.display = "block";
  } catch (error) {
    mostrarError("No se pudo conectar con el servidor.");
  }
});

btnLogout.addEventListener("click", async () => {
  try {
    await fetch(`${API_BASE}/auth/logout`, {
      method: "POST",
      headers: { Authorization: `Bearer ${tokenActual}` },
    });
  } finally {
    tokenActual = null;
    datosUsuario.textContent = "";
    mostrarExito("Sesión cerrada.");
    formLogin.reset();
    formLogin.style.display = "flex";
    btnLogout.style.display = "none";
  }
});

function mostrarExito(texto) {
  mensaje.textContent = texto;
  mensaje.style.color = "green";
  if (window.Swal) Swal.fire({ icon: "success", title: texto, timer: 1500, showConfirmButton: false });
}

function mostrarError(texto) {
  mensaje.textContent = texto;
  mensaje.style.color = "crimson";
  if (window.Swal) Swal.fire({ icon: "error", title: "Error", text: texto });
}
