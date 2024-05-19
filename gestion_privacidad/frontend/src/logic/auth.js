import axios from "axios";
import { API_PATH } from "@/logic/entorno.js";

const auth = {
  //  Validación y login de usuarios
  async login(username, password) {
    const user = { username, password };
    try {
      const response = await axios.post(API_PATH + "users/token/", user);
      return response; // Devuelve la respuesta
    } catch (error) {
      throw error;
    }
  },

  // Autenticación SSO
  async ssoLogin(token) {
    try {
      console.log("Enviando solicitud SSO con token:", token);
      const response = await axios.post(API_PATH + "users/sso-login/", { token });
      const data = response.data;
      console.log(response.data);

      // Guarda los tokens y la información del usuario en el almacenamiento local
      sessionStorage.setItem("access_token", data.access);
      sessionStorage.setItem("refresh_token", data.refresh);
      sessionStorage.setItem("user_id", data.user_id);
      sessionStorage.setItem("username", data.username);
      sessionStorage.setItem("email", data.email);

      console.log("Datos de autenticación guardados en sessionStorage");
      return response; // Devuelve la respuesta
    } catch (error) {
      console.error("Error en ssoLogin:", error);
      throw error;
    }
  },

  // Función para verificar si el usuario está autenticado
  isAuthenticated() {
    const accessToken = sessionStorage.getItem("access_token");
    return !!accessToken;
  },

  // Cierre de sesión de usuario
  async logout() {
    const accessToken = sessionStorage.getItem("access_token");
    const refreshToken = sessionStorage.getItem("refresh_token");

    try {
      const data = { refresh: refreshToken };
      const response = await axios.post(API_PATH + "users/logout/", data, {
        headers: {
          Authorization: `Bearer ${accessToken}`
        }
      });

      // Limpia el almacenamiento local al cerrar sesión
      sessionStorage.removeItem("access_token");
      sessionStorage.removeItem("refresh_token");
      sessionStorage.removeItem("user_id");
      sessionStorage.removeItem("username");
      sessionStorage.removeItem("email");

      console.log("Sesión cerrada correctamente");
      return response; // Devuelve la respuesta
    } catch (error) {
      console.error("Error en la solicitud de cierre de sesión:", error.config); // Imprimir la configuración de la solicitud
      throw error;
    }
  },
};

export default auth;
