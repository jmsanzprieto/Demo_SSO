<?php

namespace App\Controllers;

use Firebase\JWT\JWT;
use Firebase\JWT\Key;
use App\Models\TokenSsoModel;

class Home extends BaseController
{
    private function _loadDefaultView($title, $data, $view){ 
        // Permite cargar todas las vistas con una sola linea e incluyendo variables.

          $dataHeader=[
            'title'=> $title
          ];

          echo view ("templates/header",$dataHeader);
          echo view ("$view",$data);
          echo view ("templates/footer");
      }


      public function index()
      {
        exit;
      }

      public function main()
      {
          // Check if user is logged in
          if (!auth()->loggedIn()) {
              return redirect()->to('login')->with('error', 'You need to be logged in to access this page.');
          }
  
          // Get the currently logged in user
          $user = auth()->user();
  
          // Load the TokenSsoModel
          $tokenModel = new TokenSsoModel();
  
          // Get the token for the logged in user
          $tokenData = $tokenModel->where('id_usuario', $user->id)->first();
  
          // Check if the token exists
          $token = $tokenData['token'] ?? 'No token found';
          $decodedArray = null;
          $error = null;
  
          if ($token !== 'No token found') {
              try {
                  // Specify the secret key to decode the token
                  $secretKey = 'YOUR_SECRET_KEY'; // Replace with your actual secret key
  
                  // Decode the token
                  $decodedToken = JWT::decode($token, new Key($secretKey, 'HS256'));
  
                  // Convert the decoded token to an array
                  $decodedArray = (array) $decodedToken;
              } catch (\Exception $e) {
                  // Handle the error
                  $error = $e->getMessage();
              }
          }
  
          // Pass the token and decoded token data to the view
          $data = [
              'token' => $token,
              'decodedToken' => $decodedArray,
              'error' => $error,
          ];
  
          $this->_loadDefaultView("Bienvenido", $data, 'main');
      }
}
