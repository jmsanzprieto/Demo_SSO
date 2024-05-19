from django.urls import path
from . import views
from .views import NuevaContraseña


urlpatterns = [
    path('passwords/', views.ContraseñasListCreate.as_view(), name='password-list-create'),
    path('passwords/<int:pk>/', views.ContraseñasRetrieveUpdateDestroy.as_view(), name='password-detail'),
    path('passwords/usuario/<int:usuario_id>/', views.ContraseñasUsuarioList.as_view(), name='contraseñas-usuario-list'),
    path('nuevopassword/', NuevaContraseña.as_view(), name='nuevopassword'),

]
