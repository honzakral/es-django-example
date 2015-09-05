from django.conf import settings

from elasticsearch_dsl import DocType, Date, String, Nested, Object, Index, \
    MetaField

# user is repeated in several places, reuse a field definition
user_field = Object(properties={
    'display_name': String(fields={'raw': String(index='not_analyzed')}),
})

class Post(DocType):
    """
    Common superclass for Question and Answer, not being added to the index.
    """
    owner = user_field
    creation_date = Date()
    last_activity_date = Date()
    # have comments as nested type
    comments = Nested(properties={'owner': user_field})
    body = String()

class Question(Post):
    tags = String(index='not_analyzed', multi=True)
    last_editor = user_field
    last_edit_date = Date()


class Answer(Post):
    class Meta:
        parent = MetaField(type='question')

# create an index and register the doc types
index = Index(settings.ES_INDEX)
index.doc_type(Answer)
index.doc_type(Question)

