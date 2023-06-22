from django.contrib import admin
from .models import Question, Choice

# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pubdate']}),
    ]

class ChoiceAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['choice_text']}),
        ('Votos', {'fields': ['votes']}),
    ]




admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)