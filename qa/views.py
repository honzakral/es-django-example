from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.conf import settings
from django.shortcuts import render

from elasticsearch_dsl import Search

from .models import Question

class QuestionList(ListView):
    model = Question
    ordering = '-creation_date'
    paginate_by = 10


class QuestionDetail(DetailView):
    model = Question

def search(request):
    s = Search(index=settings.ES_INDEX, doc_type='question')
    if 'q' in request.GET:
        s = s.query(
            'multi_match',
            fields=['title', 'tags', 'body'],
            query=request.GET['q']
        )

    r = s.execute()

    return render(request, 'qa/question_list.html', {'object_list': r.hits})
