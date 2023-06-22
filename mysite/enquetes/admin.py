from django.contrib import admin
from .models import Question, Choice

# Register your models here.



admin.site.site_header = 'Administração DSWeb 2023.1'

class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 2




class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pubdate']}),
    ]
    inlines = [ChoiceInLine]
    list_display = ('question_text', 'id', 'pubdate', 'was_published_recently')
    list_filter = ['pubdate']
    search_fields = ['question_text']



admin.site.register(Question, QuestionAdmin)