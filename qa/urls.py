from django.conf.urls import url

from .views import QuestionDetail, QuestionList, search

urlpatterns = [
    url(r'^$', QuestionList.as_view(), name='qa-list'),
    url(r'^(?P<pk>\d+)/$', QuestionDetail.as_view(), name='qa-question'),
    url(r'^search/$', search, name='qa-search'),
]
