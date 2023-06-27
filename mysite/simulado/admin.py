from django.contrib import admin
from .models import Simulado, Questao, Alternativa

# Register your models here.
admin.site.site_header = 'Administração Simulado'

class AlternativaInLine(admin.TabularInline):
    model = Alternativa
    extra = 2




class QuestaoAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['questao_texto']}),
        ('Date information', {'fields': ['questao_data']}),
        ('Pontuação', {'fields': ['pontuacao']}),
    ]
    inlines = [AlternativaInLine]
    list_display = ('questao_texto', 'id', 'questao_data')
    list_filter = ['questao_data']
    search_fields = ['questao_texto']



admin.site.register(Questao, QuestaoAdmin)