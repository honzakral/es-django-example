import re

from django.db import models

tag_re = re.compile(r'<([^>]+)>')

class User(models.Model):
    email = models.CharField(max_length=200)
    date_joined = models.DateTimeField()
    display_name = models.CharField(max_length=200)
    url = models.CharField(max_length=400)
    location = models.CharField(max_length=400)
    description = models.TextField()
    views = models.PositiveIntegerField()
    votes_up = models.PositiveIntegerField()
    votes_down = models.PositiveIntegerField()
    age = models.PositiveIntegerField()

class Post(models.Model):
    owner = models.ForeignKey(User)
    creation_date = models.DateTimeField()
    last_activity_date = models.DateTimeField()
    score = models.IntegerField()
    body = models.TextField()
    comment_count = models.PositiveIntegerField()

    @property
    def comments(self):
        return self.comment_set.order_by('creation_date')

    @classmethod
    def get_es_mapping(cls):
        return {}

    def to_search(self):
        return {
            '_id': self.pk,
        }

    class Meta:
        abstract = True


class Question(Post):
    answer_count = models.PositiveIntegerField()
    tags_string = models.TextField()
    title = models.CharField(max_length=1024)
    favorite_count = models.PositiveIntegerField()
    view_count = models.PositiveIntegerField()
    accepted_answer = models.ForeignKey('Answer', related_name='accepted_for',
            null=True, blank=True)

    last_editor = models.ForeignKey(User, null=True, blank=True,
            related_name='last_edited_questions')
    last_edit_date  = models.DateTimeField(null=True, blank=True)

    def get_answers(self):
        return self.answer_set.order_by('-creation_date')

    @property
    def tags(self):
        return tag_re.findall(self.tags_string)

    def to_search(self):
        d = super().to_search()
        d.update({
            'tags': self.tags,
            'title': self.title,
        })
        return d

class Answer(Post):
    question = models.ForeignKey(Question)

    def to_search(self):
        d = super().to_search()
        d.update({
        })
        return d


class Comment(models.Model):
    owner = models.ForeignKey(User)
    creation_date = models.DateTimeField()
    score = models.IntegerField()
    text = models.TextField()

    class Meta:
        abstract = True


class QuestionComment(Comment):
    post = models.ForeignKey(Question, related_name='comment_set')


class AnswerComment(Comment):
    post = models.ForeignKey(Answer, related_name='comment_set')

