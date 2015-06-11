from django.conf import settings

from elasticsearch_dsl import DocType, Date, String, Nested, Object, Index, MetaField

user_field = Object(properties={
    'display_name': String(fields={'raw': String(index='not_analyzed')})
})

class Post(DocType):
    creation_date = Date()
    comments = Nested(properties={'owner': user_field})

class Question(Post):
    tags = String(index='not_analyzed', multi=True)


class Answer(Post):
    class Meta:
        parent = MetaField(type='question')

index = Index(settings.ES_INDEX)
index.doc_type(Answer)
index.doc_type(Question)
