from typing import Any, Dict
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from .models import Estudante, Tema, Alternativa, Simulado, Questao
from django.db.models import Sum
import datetime





# Create your views here.
class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'simulado/index.html')


class ListarSimuladosView(View):
    def get(self, request, *args, **kwargs):
        simulados = Simulado.objects.all()
        termo_pesquisa = request.GET.get('q', None)

        if termo_pesquisa:
            simulados = simulados.filter(nome__icontains=termo_pesquisa)
        return render(request, 'simulado/listar_simulados.html', {'simulados': simulados})

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

class AdicionarQuestaoView(View):
    @method_decorator(login_required(login_url='/simulado/login', redirect_field_name=None))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        tema_select = Tema.objects.all()
        return render(request, 'simulado/adicionar_questao.html', {'tema_select':tema_select})
    
    def post(self, request, *args, **kwargs):
        questao_form = {
            'enunciado': request.POST['enunciado'],
            'pontuacao': request.POST['pontuacao'],
            'tema': request.POST['tema'],
        }
        tema_select = Tema.nome.field.choices

        questao_form['tema'] = Tema.objects.get(pk=questao_form['tema'])

        questao = Questao.objects.create(**questao_form)
        for i in range(1, 5):
            alternativa_texto = request.POST.get(f'alternativa_texto_{i}', None)
            alternativa_correta = request.POST.get(f'alternativa_correta', None)

            if alternativa_texto and alternativa_correta and int(alternativa_correta) == i:
                Alternativa.objects.create(alternativa_texto=alternativa_texto, alternativa_correta=True, questao=questao)
            else:
                Alternativa.objects.create(alternativa_texto=alternativa_texto, alternativa_correta=False, questao=questao)


        return redirect(reverse('simulado:index'))


class AdicionarSimuladoView(View):
    @method_decorator(login_required(login_url='/simulado/login', redirect_field_name=None))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        tema_select = Tema.objects.all()
        questoes_disponiveis = Questao.objects.all()
        return render(request, 'simulado/adicionar_simulado.html', {'tema_select':tema_select, 'questoes_disponiveis':questoes_disponiveis})
    
    def get(self, request, *args, **kwargs):
        tema_select = Tema.objects.all()
        questoes_disponiveis = Questao.objects.all()
        return render(request, 'simulado/adicionar_simulado.html', {'tema_select': tema_select, 'questoes_disponiveis': questoes_disponiveis})
    
    def post(self, request, *args, **kwargs):
        nome = request.POST['nome']
        data_criacao = request.POST['data_criacao']
        tema_id = request.POST['tema']
        questoes_selecionadas = request.POST.getlist('questoes[]')

        tema = Tema.objects.get(pk=tema_id)

        # Inicializa a nota máxima com 0
        nota_maxima = 0

        # Lista para armazenar as questões selecionadas com suas respectivas pontuações
        questoes_com_pontuacao = []

        for questao_id in questoes_selecionadas:
            questao = Questao.objects.get(pk=questao_id)
            pontuacao = request.POST.get(f'pontuacao_{questao_id}', 0)
            nota_maxima += int(pontuacao)  # Soma a pontuação da questão à nota máxima
            questoes_com_pontuacao.append((questao, pontuacao))

        # Cria o simulado com o tema selecionado
        simulado = Simulado.objects.create(nome=nome, data_criacao=data_criacao, tema=tema)

        # Adiciona as questões selecionadas ao simulado com suas pontuações personalizadas
        for questao, pontuacao in questoes_com_pontuacao:
            simulado.questao.add(questao, through_defaults={'pontuacao': pontuacao})

        # Salva a nota máxima no simulado
        simulado.nota_maxima = nota_maxima
        simulado.save()

        return redirect(reverse('simulado:index'))

class DetalharSimuladosView(DetailView):
    model = Simulado
    template_name = 'simulado/detalhar_simulado.html'
    context_object_name = 'simulado'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        # Calcula a nota máxima do simulado somando a pontuação de todas as questões
        nota_maxima = self.object.questao.aggregate(Sum('pontuacao'))['pontuacao__sum']

        # Adiciona a nota máxima ao contexto
        context['nota_maxima'] = nota_maxima

        return context
    #for i in range(1, 5):
    #        alternativa_texto = request.POST.get(f'alternativa_texto_{i}', None)
    #        alternativa_correta = request.POST.get(f'alternativa_correta', None)#
    #
    #        if alternativa_texto and alternativa_correta and int(alternativa_correta) == i:
    #            Alternativa.objects.create(alternativa_texto=alternativa_texto, alternativa_correta=True, questao=questao)
    ##        else:
    #            Alternativa.objects.create(alternativa_texto=alternativa_texto, alternativa_correta=False, questao=questao)