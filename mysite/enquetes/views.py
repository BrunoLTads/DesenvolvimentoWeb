from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Choice, Question
from django.http import Http404




# Create your views here.
class IndexView(generic.ListView):
    template_name = "enquetes/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pubdate")[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = "enquetes/question_detail.html"

class ResultsView(generic.DetailView):
    model = Question
    template_name = "enquetes/results.html"

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "enquetes/detail.html",{"question": question, "error_message": "Você não selecionou uma alternativa.",},)
    else:
            selected_choice.votes += 1
            selected_choice.save()
            return HttpResponseRedirect(reverse("enquetes:results", args=(question.id,)))