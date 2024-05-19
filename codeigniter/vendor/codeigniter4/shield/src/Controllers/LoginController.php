<?php

declare(strict_types=1);

namespace CodeIgniter\Shield\Controllers;

use App\Controllers\BaseController;
use CodeIgniter\HTTP\RedirectResponse;
use CodeIgniter\Shield\Authentication\Authenticators\Session;
use CodeIgniter\Shield\Traits\Viewable;
use CodeIgniter\Shield\Validation\ValidationRules;
use Firebase\JWT\JWT;
use Firebase\JWT\Key;
use App\Models\TokenSsoModel;

class LoginController extends BaseController
{
    use Viewable;

    /**
     * Displays the form the login to the site.
     *
     * @return RedirectResponse|string
     */
    public function loginView()
    {
        if (auth()->loggedIn()) {
            return redirect()->to(config('Auth')->loginRedirect());
        }

        /** @var Session $authenticator */
        $authenticator = auth('session')->getAuthenticator();

        // If an action has been defined, start it up.
        if ($authenticator->hasAction()) {
            return redirect()->route('auth-action-show');
        }

        return $this->view(setting('Auth.views')['login']);
    }

    /**
     * Attempts to log the user in.
     */
    public function loginAction(): RedirectResponse
    {
        // Validate here first, since some things,
        // like the password, can only be validated properly here.
        $rules = $this->getValidationRules();

        if (! $this->validateData($this->request->getPost(), $rules, [], config('Auth')->DBGroup)) {
            return redirect()->back()->withInput()->with('errors', $this->validator->getErrors());
        }

        /** @var array $credentials */
        $credentials             = $this->request->getPost(setting('Auth.validFields')) ?? [];
        $credentials             = array_filter($credentials);
        $credentials['password'] = $this->request->getPost('password');
        $remember                = (bool) $this->request->getPost('remember');

        /** @var Session $authenticator */
        $authenticator = auth('session')->getAuthenticator();

        // Check if the user is already logged in, if so, log them out
        if (auth()->loggedIn()) {
            auth()->logout();
        }

        // Attempt to login
        $result = $authenticator->remember($remember)->attempt($credentials);
        if (! $result->isOK()) {
            return redirect()->route('login')->withInput()->with('error', $result->reason());
        }

        // Get user data
        $user = auth()->user();

        // Generate JWT token
        $key = 'YOUR_SECRET_KEY'; // Replace with your secret key
        $payload = [
            // 'iss' => "your_issuer", // Issuer
            // 'aud' => "your_audience", // Audience
            'iat' => time(), // Issued at
            'nbf' => time(), // Not before
            'exp' => time() + 3600, // Expiration time (e.g., 1 hour)
            'sub' => $user->id, // Subject
            'email' => $user->email, // Additional user data
            'name' => $user->username // Additional user data
        ];

        $jwt = JWT::encode($payload, $key, 'HS256');

        // Save or update the token in the database
        $tokenModel = new TokenSsoModel();
        $tokenModel->saveToken($user->id, $jwt);

        // If an action has been defined for login, start it up.
        if ($authenticator->hasAction()) {
            return redirect()->route('demo')->withCookies();
        }

        // Redirect to the intended page or home
        return redirect()->to(config('Auth')->loginRedirect())->with('message', lang('Auth.successLogin'));
    }

    /**
     * Returns the rules that should be used for validation.
     *
     * @return array<string, array<string, list<string>|string>>
     */
    protected function getValidationRules(): array
    {
        $rules = new ValidationRules();

        return $rules->getLoginRules();
    }

    /**
     * Logs the current user out.
     */
    public function logoutAction(): RedirectResponse
    {
        // Capture logout redirect URL before auth logout,
        // otherwise you cannot check the user in `logoutRedirect()`.
        $url = config('Auth')->logoutRedirect();

        auth()->logout();

        return redirect()->to($url)->with('message', lang('Auth.successLogout'));
    }
}
