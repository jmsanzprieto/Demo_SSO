<template>
  <div>
    <p>Iniciando sesión...</p>
  </div>
</template>

<script>
import auth from "@/logic/auth"; // Asegúrate de importar tu módulo de autenticación

export default {
  name: "SSOLogin",
  async created() {
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get('token');
    if (token) {
      try {
        console.log("Token encontrado:", token);
        const response = await auth.ssoLogin(token);
        console.log("Respuesta de la autenticación SSO:", response);
        if (response.status === 200) {
          console.log("Autenticación exitosa, redirigiendo...");
          this.$router.push({ name: 'Dashboard' }); // Redirige a la página principal u otra página
        } else {
          console.error("Error en la autenticación SSO, status no 200:", response.status);
        }
      } catch (error) {
        console.error("Error en la solicitud de autenticación SSO:", error);
      }
    } else {
      console.error("Token no proporcionado");
    }
  }
};
</script>
