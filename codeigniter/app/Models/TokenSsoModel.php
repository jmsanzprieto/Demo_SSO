<?php

namespace App\Models;

use CodeIgniter\Model;

class TokenSsoModel extends Model
{
    protected $table = 'token_sso';
    protected $primaryKey = 'id_token';
    protected $allowedFields = ['id_usuario', 'token'];

    /**
     * Inserta o actualiza el token para un usuario específico.
     *
     * @param int $userId
     * @param string $token
     * @return bool
     */
    public function saveToken(int $userId, string $token): bool
    {
        // Buscar si ya existe un registro para el usuario
        $existingToken = $this->where('id_usuario', $userId)->first();

        if ($existingToken) {
            // Actualizar el token existente
            return $this->update($existingToken['id_token'], ['token' => $token]);
        } else {
            // Insertar un nuevo registro
            return $this->insert(['id_usuario' => $userId, 'token' => $token]) !== false;
        }
    }
}
