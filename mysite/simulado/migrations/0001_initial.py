# Generated by Django 4.1.4 on 2023-07-06 00:34

from django.db import migrations, models
import django.db.models.deletion
import simulado.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Simulado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('data_criacao', models.DateTimeField(verbose_name='data criada')),
                ('tema', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='simulado.tema')),
            ],
        ),
        migrations.CreateModel(
            name='Questao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enunciado', models.CharField(max_length=200, verbose_name='enunciado')),
                ('pontuacao', models.PositiveIntegerField(default=0, validators=[simulado.models.pontuacao_certa])),
                ('simulado', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='simulado.simulado')),
            ],
        ),
        migrations.CreateModel(
            name='Alternativa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alternativa_texto', models.CharField(max_length=200)),
                ('questao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simulado.questao')),
            ],
        ),
    ]
