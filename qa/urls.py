from django.conf.urls import patterns, url

from .views import QuestionDetail, QuestionList, search

urlpatterns = patterns('',
    url(r'^$', QuestionList.as_view(), name='qa-list'),
    url(r'^(?P<pk>\d+)/$', QuestionDetail.as_view(), name='qa-question'),
    url(r'^search/$', search, name='qa-search'),
)
