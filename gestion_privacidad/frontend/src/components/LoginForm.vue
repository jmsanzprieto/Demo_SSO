<template>
    <div class="container d-flex justify-content-center align-items-center vh-10">
       <div class="card w-50">
         <div class="card-body">
           <h5 class="card-title text-center mb-4">Formulario de inicio</h5>
           <form @submit.prevent="login">
             <div class="mb-3">
               <label for="username" class="form-label">Usuario:</label>
               <input type="text" id="username" v-model="username" class="form-control" required>
             </div>
             <div class="mb-3">
               <label for="password" class="form-label">Contraseña:</label>
               <input type="password" id="password" v-model="password" class="form-control" required>
             </div>
             <button type="submit" class="btn btn-primary">Iniciar sesión</button>
           </form>
           <div v-if="showAlert" class="alert alert-danger mt-3" role="alert">
             El nombre de usuario o la contraseña, no son correctos.
           </div>
         </div>
       </div>
     </div>
   </template>
   
   <script>
   import auth from "@/logic/auth";

   export default {
     data: () => ({
       username: "",
       password: "",
       showAlert: false, // Variable para controlar la visibilidad del alert
     }),
     methods: {
       async login() {
         try {
           const response = await auth.login(this.username, this.password);
           if (response.data && response.data.access) {
             sessionStorage.setItem("access_token", response.data.access);
             sessionStorage.setItem("refresh_token", response.data.refresh);
             sessionStorage.setItem("user_id", response.data.user_id);
             this.$router.push("/Dashboard");
           } else {
             this.showAlert = true; // Mostrar el alert si no se reciben tokens en la respuesta
           }
         } catch (error) {
           this.showAlert = true; // Mostrar el alert si hay un error
         }
       },
     },
   };
   </script>
   
   <style scoped>
   .card{background-color: #f0f0f1;}
   </style>
   