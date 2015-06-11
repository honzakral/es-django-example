from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render

from .models import Question
from .search import Question as QuestionDoc

class QuestionList(ListView):
    model = Question
    ordering = '-creation_date'
    paginate_by = 10


class QuestionDetail(DetailView):
    model = Question

def search(request):
    s = QuestionDoc.search().execute()
    return render(request, 'qa/question_list.html', {'object_list': s})
