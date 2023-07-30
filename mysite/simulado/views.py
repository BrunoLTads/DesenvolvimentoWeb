from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .models import Estudante, Tema, Alternativa, Simulado, Questao





# Create your views here.
class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'simulado/index.html')


class CadastrarEstudanteView(View):
    def get(self, request, *args, **kwargs):
        tema_favorito_select = Tema.objects.all()
        return render(request, 'simulado/cadastro.html', {'tema_favorito_select': tema_favorito_select})
    
    def post(self, request, *args, **kwargs):
        estudante_form = {
            'tema_favorito': request.POST['tema_favorito'],
        }
        tema_favorito_select = Tema.nome.field.choices

        estudante_form['tema_favorito'] = Tema.objects.get(pk=estudante_form['tema_favorito'])

        user_form = {
            'username': request.POST['username'],
            'password': request.POST['password'],
            'email': request.POST['email'],
        }

        if User.objects.filter(username=user_form['username']):
            contexto = {
                'error': {'field':'username', 'message': 'Nome de usuário já está em uso"'},
                'estudante_form': estudante_form,
                'user_form': user_form
            }
            return render(request, 'simulado/cadastro.html', contexto)

        if User.objects.filter(email=user_form['email']):
            contexto = {
                'error': {'field':'email', 'message': 'Email já está em uso'},
                'estudante_form': estudante_form,
                'user_form': user_form
            }
            return render(request, 'simulado/cadastro.html', contexto)
    
        user = User.objects.create_user(
            username=user_form['username'], email=user_form['email'], password=user_form['password']
            )
        
        if not user:
            return render(request, 'simulado/erro.html')
        
        novo_estudante = Estudante(**estudante_form, user=user)

        novo_estudante.save()

        login(request, user)

        return render(request, 'simulado/index.html', {'estudante': novo_estudante})




class login_usuarioView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'simulado/login.html')
    
    def post(self, request, *args, **kwargs):
        login_form = {
            'username': request.POST['username'],
            'password': request.POST['password'],
        }

        user = authenticate(request, **login_form)

        if user is not None:
            login(request, user)
            return redirect(reverse('simulado:index'))
        
        context = {
            'login_form': login_form,
            'error': {
                'message': "Credenciais inválidas."
            }
        }

        print(context)
        return render(request, 'simulado/login.html', context)

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return render(request, 'simulado/index.html')