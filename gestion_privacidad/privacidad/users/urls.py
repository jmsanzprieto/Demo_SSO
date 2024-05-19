from django.urls import path

from .views import UserRegistrationView, CustomTokenObtainPairView, LogoutView, SSOLoginView





urlpatterns = [
    # URL PARA EL REGISTRO
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    # URL PARA EL LOGIN
    path('token/',CustomTokenObtainPairView.as_view(), name='token'),
    # URL PARA EL LOGOUT
    path('logout/', LogoutView.as_view(), name='logout_token'),
    
    # URL PARA EL SSO
    path('sso-login/', SSOLoginView.as_view(), name='sso_login'),
]
