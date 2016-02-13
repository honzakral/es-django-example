from django.conf import settings

from elasticsearch_dsl import DocType, Date, String, Nested, Object, Index, \
    MetaField, analyzer, FacetedSearch, Q, TermsFacet, DateHistogramFacet, SF

# user is repeated in several places, reuse a field definition
user_field = Object(properties={
    'display_name': String(fields={'raw': String(index='not_analyzed')}),
})

# create our own analyzer
html_strip = analyzer('html_strip',
    tokenizer="standard",
    filter=["standard", "lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)

class Post(DocType):
    """
    Common superclass for Question and Answer, not being added to the index.
    """
    owner = user_field
    creation_date = Date()
    last_activity_date = Date()
    # have comments as nested type
    comments = Nested(properties={'owner': user_field})
    body = String(analyzer=html_strip)

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


class QASearch(FacetedSearch):
    doc_types = [Question]
    index = settings.ES_INDEX

    fields = ['tags', 'title', 'body']

    facets = {
        'tags': TermsFacet(field='tags'),

        'months': DateHistogramFacet(
            field='creation_date',
            interval='month',
            min_doc_count=0),
    }

    def query(self, search, query):
        if not query:
            return search
        # query in tags, title and body for query
        q = Q('multi_match', fields=['tags^10', 'title', 'body'], query=query)
        # also find questions that have answers matching query
        q |= Q('has_child', type='answer', query=Q('match', body=query))
        # take the popularity field into account when sorting
        search = search.query(
            'function_score',
            query=q,
            functions=[SF('field_value_factor', field='popularity')]
        )

        return search
