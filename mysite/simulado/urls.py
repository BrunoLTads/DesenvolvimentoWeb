from django.urls import path
from . import views

app_name = 'simulado'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('cadastro/', views.CadastrarEstudanteView.as_view(), name='registrar'),
    path('login/', views.login_usuarioView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]