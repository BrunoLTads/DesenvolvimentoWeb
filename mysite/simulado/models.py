from django.db import models

# Create your models here.




class Simulado(models.Model):
    simulado_nome = models.CharField(max_length=100)
    simulado_data = models.DateTimeField("data criada")
    tema = models.CharField(max_length=200)


class Questao(models.Model):
    questao_texto = models.CharField(max_length=200)
    questao_data = models.DateTimeField("data publicada")
    pontuacao = models.PositiveIntegerField(default=0, max_length=3)
    simulado = models.ForeignKey(Simulado, on_delete=models.SET_NULL, null=True)


class Alternativa(models.Model):
    alternativa_texto = models.CharField(max_length=200)
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE)



#  COISAS PARA FAZER
#  Utilizar validador para delimitar pontuação da questão
#  Conseguir selecionar a questão para um simulado durante sua criação
#  Aprender a determinar qual alternativa será a correta
#
#
#