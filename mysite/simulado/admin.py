from django.contrib import admin
from .models import Tema, Simulado, Questao, Alternativa

# Register your models here.
admin.site.site_header = 'Administração Simulado'

class AlternativaInLine(admin.TabularInline):
    model = Alternativa
    extra = 2




class QuestaoAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['enunciado']}),
        ('Pontuação', {'fields': ['pontuacao']}),
    ]
    inlines = [AlternativaInLine]
    list_display = ('enunciado', 'id')
    #list_filter = ['questao_data']
    search_fields = ['enunciado']



admin.site.register(Questao, QuestaoAdmin)
admin.site.register(Tema)
admin.site.register(Simulado)