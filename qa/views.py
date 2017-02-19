from dateutil import parser

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render

from .models import Question
from .search import QASearch
from .forms import SearchForm

class QuestionList(ListView):
    model = Question
    ordering = '-creation_date'
    paginate_by = 10


class QuestionDetail(DetailView):
    model = Question

def search(request):
    q = None
    filters={}

    form = SearchForm(request.GET)
    if form.is_valid():
        filters = {
            'tags': form.cleaned_data['tags'],
            'months': form.cleaned_data['months']
        }
        q = form.cleaned_data['q']
    s = QASearch(query=q, filters=filters)

    paginator = Paginator(s, 10)
    page_no = request.GET.get('page')
    try:
        page = paginator.page(page_no)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    response = page.object_list.execute()
    return render(
        request,
        'qa/question_list.html',
        {
            'object_list': response.hits,
            'search': response,
            'page_obj': page,
            'paginator': paginator
        }
    )
