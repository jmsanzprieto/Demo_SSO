<template>
  <div>
    <h1>Esta es la página del usuario conectado</h1>
    <button class="btn btn-danger" @click="handleLogout">Cerrar sesión</button>
   
    
    <!-- Formulario para agregar nueva contraseña -->
    <div v-if="showForm" class="container card">
  <div class="row justify-content-center">
    <div class="col-md-6">
      <h4 class="text-center">Cargar Contraseña</h4>
      <form @submit.prevent="addNewPassword" class="row g-3">
        <div class="col-md-5">
          <label for="service" class="form-label">Servicio:</label>
          <input class="form-control" type="text" id="service" v-model="newPassword.service" required>
        </div>
        <div class="col-md-5">
          <label for="password" class="form-label">Contraseña:</label>
          <input class="form-control" type="password" id="password" v-model="newPassword.password" required>
        </div>
        <div class="col-md-2 mt-auto">
          <button type="submit" class="btn btn-primary" style="width: 100%">Guardar</button>
        </div>
      </form>
    </div>
  </div>
</div>





    <!-- Tabla para mostrar las contraseñas -->
    <table class="table">
      <thead>
        <tr>
          <th>Servicio</th>
          <th>Contraseña</th>
          <!-- Agrega más columnas según tus datos -->
        </tr>
      </thead>
      <tbody>
        <!-- Iterar sobre el array de contraseñas y mostrar cada elemento en una fila -->
        <tr v-for="(password, index) in passwords" :key="index">
          <td>{{ password.service }}</td>
          <td @click="revealPassword(index)">{{ maskedPasswords[index] }}</td>
          <!-- Agrega más celdas según tus datos -->
        </tr>
      </tbody>
    </table>
    <button class="btn btn-primary" @click="showNewPasswordForm">Nueva Contraseña</button>
  </div>
</template>

<script>
import auth from "@/logic/auth";
import { accessToken, refreshToken, user_id } from "@/logic/entorno.js";
import PasswordServices from "@/services/Passwords.js";

export default {
  data() {
    return {
      passwords: [], // Inicializar una variable para almacenar las contraseñas
      maskedPasswords: [], // Variable para almacenar las contraseñas enmascaradas
      showForm: false, // Controlar la visibilidad del formulario para agregar nueva contraseña
      newPassword: { service: '', password: '' }, // Variable para almacenar los valores del nuevo formulario
    };
  },
  mounted() {
    setTimeout(() => {
      this.loadPasswords(); // Llamar al método loadPasswords cuando el componente esté montado y listo
    }, 100); // Esperar 100 milisegundos antes de cargar las contraseñas
  },
  methods: {
    async loadPasswords() {
      try {
        // Llamada al método GetPasswords para obtener el listado de contraseñas
        const accessToken = sessionStorage.getItem("access_token");
        const user_id = sessionStorage.getItem("user_id");
        console.log("El access_token es: ", accessToken);
        console.log("El ID del usuario es: ", user_id);
        const passwordsResponse = await PasswordServices.GetPasswords(accessToken, user_id);
        this.passwords = passwordsResponse.data; // Almacenar las contraseñas en la variable de datos del componente
        // Inicializar maskedPasswords con las contraseñas enmascaradas
        this.maskedPasswords = this.passwords.map(password =>
          this.maskPassword(password.password)
        );
        console.log("Listado de contraseñas:", this.passwords);
      } catch (error) {
        console.error("Error al cargar las contraseñas:", error);
      }
    },
    async handleLogout() {
      try {
        const accessToken = sessionStorage.getItem("access_token");
        const refreshToken = sessionStorage.getItem("refresh_token");
        console.log("Para el logout: el token de acceso es: ", accessToken);
        console.log("Para el logout: el token de refresco es: ", refreshToken);
        await auth.logout(accessToken, refreshToken);
        sessionStorage.clear();
        this.$router.push("/");
      } catch (error) {
        console.error("Error al cerrar sesión:", error);
      }
    },
    maskPassword(password) {
      return "*".repeat(10); // Enmascarar la contraseña
    },
    revealPassword(index) {
      // Al hacer clic en una contraseña enmascarada, revelar la contraseña real
      this.maskedPasswords.splice(index, 1, this.passwords[index].password);
      // Temporizador para volver a enmascarar la contraseña después de 3 segundos
      setTimeout(() => {
        this.maskedPasswords.splice(index, 1, this.maskPassword(this.passwords[index].password));
      }, 3000);
    },
    showNewPasswordForm() {
      this.showForm = true; // Mostrar el formulario para agregar nueva contraseña
    },
    async addNewPassword() {
      try {
        const accessToken = sessionStorage.getItem("access_token");
        const user_id = sessionStorage.getItem("user_id");
        const response = await PasswordServices.AddPassword(accessToken, user_id, this.newPassword);
        console.log("Nueva contraseña agregada:", response.data);
        this.passwords.push(response.data); // Agregar la nueva contraseña al listado
        this.maskedPasswords.push(this.maskPassword(response.data.password)); // Agregar la contraseña enmascarada al listado
        this.newPassword = { service: '', password: '' }; // Reiniciar el formulario
        this.showForm = false; // Ocultar el formulario después de agregar la contraseña
      } catch (error) {
        console.error("Error al agregar la nueva contraseña:", error);
      }
    },
    async addNewPassword() {
  try {
    const accessToken = sessionStorage.getItem("access_token");
    const user_id = sessionStorage.getItem("user_id");
    const response = await PasswordServices.SavePassword(accessToken, user_id, this.newPassword);
    console.log("Nueva contraseña agregada:", response);
    // Actualizar la lista de contraseñas
    await this.loadPasswords();
    // Reiniciar el formulario
    this.newPassword = { service: '', password: '' };
    // Ocultar el formulario después de agregar la contraseña
    this.showForm = false;
  } catch (error) {
    console.error("Error al agregar la nueva contraseña:", error);
  }
}
  }
};
</script>

<style scooped>
 .card{background-color: #f0f0f1; padding:10px;margin-top:10px}
</style>
