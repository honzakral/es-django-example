import re

from django.db import models
from django.db.models.signals import post_save, pre_delete

from .search import Question as QuestionDoc, Answer as AnswerDoc

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

    def to_search(self):
        return {
            'display_name': self.display_name,
            'url': self.url,
        }

class Post(models.Model):
    owner = models.ForeignKey(User, blank=True, null=True)
    creation_date = models.DateTimeField()
    last_activity_date = models.DateTimeField()
    rating = models.IntegerField()
    body = models.TextField()
    comment_count = models.PositiveIntegerField()

    @property
    def comments(self):
        return self.comment_set.order_by('creation_date')

    def to_search(self):
        data = {
            '_id': self.pk,
            'id': self.pk,
            'creation_date': self.creation_date,
            'last_activity_date': self.last_activity_date,
            'body': self.body,
            'rating': self.rating,
            'comments': [c.to_search() for c in self.comments],
            'comment_count': self.comment_count,
        }
        if self.owner:
            data['owner'] = self.owner.to_search()
        return data


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

    @property
    def answers(self):
        return self.answer_set.order_by('-creation_date')

    @property
    def tags(self):
        return tag_re.findall(self.tags_string)

    def to_search(self):
        d = super(Question, self).to_search()
        d.update({
            'tags': self.tags,
            'title': self.title,
            'favorite_count': self.favorite_count,
            'view_count': self.view_count,
            'answer_count': self.answer_count,
            'has_accepted_answer': bool(self.accepted_answer_id),
        })
        if self.last_editor_id:
            try:
                d.update({
                    'last_editor': self.last_editor.to_search(),
                    'last_edit_date': self.last_edit_date
                })
            except models.ObjectDoesNotExist:
                pass
        return QuestionDoc(**d)

class Answer(Post):
    question = models.ForeignKey(Question)

    def to_search(self):
        d = super(Answer, self).to_search()
        return AnswerDoc(meta={'id': d.pop('_id'), 'parent': self.question_id}, **d)

class Comment(models.Model):
    owner = models.ForeignKey(User, blank=True, null=True)
    creation_date = models.DateTimeField()
    rating = models.IntegerField()
    text = models.TextField()

    class Meta:
        abstract = True

    def to_search(self):
        data = {
            'creation_date': self.creation_date,
            'rating': self.rating,
            'text': self.text,
        }
        if self.owner:
            data['owner'] = self.owner.to_search()
        return data



class QuestionComment(Comment):
    post = models.ForeignKey(Question, related_name='comment_set')


class AnswerComment(Comment):
    post = models.ForeignKey(Answer, related_name='comment_set')


def update_search(instance, **kwargs):
    instance.to_search().save()

def remove_from_search(instance, **kwargs):
    instance.to_search().delete()

post_save.connect(update_search, sender=Answer)
post_save.connect(update_search, sender=Question)
pre_delete.connect(remove_from_search, sender=Answer)
pre_delete.connect(remove_from_search, sender=Question)

