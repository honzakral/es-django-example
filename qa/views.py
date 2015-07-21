from dateutil import parser

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render

from .models import Question
from .search import QASearch

class QuestionList(ListView):
    model = Question
    ordering = '-creation_date'
    paginate_by = 10


class QuestionDetail(DetailView):
    model = Question

def search(request):
    filters = {
        'tags': request.GET.getlist('tags', []),
        'months': list(map(parser.parse, request.GET.getlist('months', []))),
    }
    s = QASearch(query=request.GET.get('q', None), filters=filters)
    response = s.execute()
    return render(request, 'qa/question_list.html', {'object_list': response.hits, 'search': response})
