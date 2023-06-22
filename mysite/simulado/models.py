from django.db import models

# Create your models here.
class Questao(models.Model):
    questao_texto = models.CharField(max_length=200)
    data_pub = models.DateTimeField("data publicada")