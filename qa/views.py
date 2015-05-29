from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Question

class QuestionList(ListView):
    model = Question
    ordering = '-creation_date'
    paginate_by = 10


class QuestionDetail(DetailView):
    model = Question

