// Gestión de las contraseñas
import axios from "axios";
import {API_PATH}  from "@/logic/entorno.js";
import { ref } from "vue";

const PasswordServices = {

    // Llamada al listado de contraseñas guardadas por un usuario concreto
    async GetPasswords(accessToken,user_id) {
        try {
           const response = await axios.get(API_PATH + "passwords/passwords/usuario/"+user_id+"/",{
            headers: {
              Authorization: `Bearer ${accessToken}` // Pasar el token de acceso en el encabezado de autorización
            }
          });
          return response; // Devuelve la respuesta
        } catch (error) {
          console.error("Error en la solicitud:", error.config); // Imprimir la configuración de la solicitud
          throw error;
        }
      },
    
  // Método para guardar una nueva contraseña
  async SavePassword(accessToken, user_id, newPasswordData) {
    try {
      const response = await axios.post(API_PATH + "passwords/nuevopassword/", {
        // Envía los datos de la nueva contraseña al servidor
        user: user_id,
        service: newPasswordData.service,
        password: newPasswordData.password,
      }, {
        headers: {
          Authorization: `Bearer ${accessToken}`, // Pasar el token de acceso en el encabezado de autorización
        },
      });
      return response.data; // Devuelve los datos de la nueva contraseña guardada
    } catch (error) {
      console.error("Error al guardar la contraseña:", error);
      throw error;
    }
  },

    };

export default PasswordServices;