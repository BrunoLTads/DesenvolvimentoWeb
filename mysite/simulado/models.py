from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

# Create your models here.


def pontuacao_certa(value):
    if (value < 0 or value > 100):
        raise ValidationError(str(value) + " não é um valor adequado. Por favor, selecione um número entre 0 e 100")

class Tema(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

class Questao(models.Model):
    enunciado = models.CharField("enunciado", max_length=200)
    pontuacao = models.PositiveIntegerField(default=0, validators=[pontuacao_certa])
    tema = models.ForeignKey(Tema, on_delete=models.SET_DEFAULT, default=3)

    def __str__(self):
        return self.enunciado


class Simulado(models.Model):
    nome = models.CharField(max_length=100)
    data_criacao = models.DateTimeField("data criada")
    tema = models.ForeignKey(Tema, on_delete=models.SET_NULL, null=True)
    questao = models.ManyToManyField(Questao)

    def __str__(self):
        return self.nome

class Alternativa(models.Model):
    alternativa_texto = models.CharField(max_length=200)
    alternativa_correta = models.BooleanField(default=False)
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE)

    def __str__(self):
        return self.alternativa_texto

class Estudante(models.Model):
    tema_favorito = models.ForeignKey(Tema, on_delete=models.SET_NULL, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)



