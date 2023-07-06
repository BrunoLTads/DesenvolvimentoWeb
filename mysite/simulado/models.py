from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.


def pontuacao_certa(value):
    if (value < 0 or value > 100):
        raise ValidationError(str(value) + " não é um valor adequado. Por favor, selecione um número entre 0 e 100")

class Tema(models.Model):
    nome = models.CharField(max_length=50)

class Simulado(models.Model):
    nome = models.CharField(max_length=100)
    data_criacao = models.DateTimeField("data criada")
    tema = models.ForeignKey(Tema, on_delete=models.SET_NULL, null=True)


class Questao(models.Model):
    enunciado = models.CharField("enunciado", max_length=200)
    pontuacao = models.PositiveIntegerField(default=0, validators=[pontuacao_certa])
    simulado = models.ForeignKey(Simulado, on_delete=models.SET_NULL, null=True)



class Alternativa(models.Model):
    alternativa_texto = models.CharField(max_length=200)
    alternativa_correta = models.int
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE)





#  COISAS PARA FAZER
#  Utilizar validador para delimitar pontuação da questão
#  Conseguir selecionar a questão para um simulado durante sua criação
#  Aprender a determinar qual alternativa será a correta
#
#
#