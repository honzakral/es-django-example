from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render

from elasticsearch_dsl import Q

from .models import Question
from .search import Question as QuestionDoc

class QuestionList(ListView):
    model = Question
    ordering = '-creation_date'
    paginate_by = 10


class QuestionDetail(DetailView):
    model = Question

def search(request):
    s = QuestionDoc.search()
    if 'q' in request.GET:
        query = request.GET['q']
        # query in tags, title and body for query
        q = Q('multi_match', fields=['tags^10', 'title', 'body'], query=query)
        # also find questions that have answers matching query
        q |= Q('has_child', type='answer', query=Q('match', body=query))
        s = s.query(q)

    # add tags filters
    if 'tags' in request.GET:
        s = s.filter('terms', tags=request.GET.getlist('tags'))

    return render(request, 'qa/question_list.html', {'object_list': s.execute()})
