from django.urls import path
from . import views

app_name = 'simulado'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('cadastro/', views.CadastrarEstudanteView.as_view(), name='registrar'),
    path('login/', views.login_usuarioView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('simulados/', views.ListarSimuladosView.as_view(), name='listar_simulados'),
    path('detalhar/<int:pk>/', views.DetalharSimuladosView.as_view(), name='detalhar_simulado'),
    path('adicionar/questao/', views.AdicionarQuestaoView.as_view(), name='adicionar_questao'),
    path('adicionar/simulado/', views.AdicionarSimuladoView.as_view(), name='adicionar_simulado'),
]