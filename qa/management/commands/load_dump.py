from __future__ import print_function

import sys
import time
from os.path import join
from xml.etree import cElementTree
from dateutil import parser as date_parser

from django.core.management.base import BaseCommand

from qa.models import User, Question, Answer, QuestionComment, AnswerComment

POST_TYPES = {
    1: Question,
    2: Answer,
}

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('dump_directory',
            help='Directory containing the XML files.')

    def handle(self, **options):
        self.dir = options['dump_directory']
        self._answers = set()
        self._questions = set()

        for m, f in (
                ('Users', self.parse_users),
                ('Posts', self.parse_posts),
                ('Comments', self.parse_comments)
            ):
            self.verbose_run(f, m)

    def verbose_run(self, cmd_func, name, report_every=100):
        print('Loading %s: ' % name, end='')
        start = time.time()
        cnt = 0
        for u in cmd_func():
            cnt += 1
            if cnt % report_every:
                print('.', end='')
                sys.stdout.flush()
        print('DONE\nLoaded %d %s in %.2f seconds'% (
            cnt, name, time.time() - start
        ))

    def _parse_file(self, xml_file):
        with open(join(self.dir, xml_file)) as input:
            root = cElementTree.iterparse(input)

            for event, e in root:
                if event != 'end' or e.tag != 'row':
                    continue
                yield dict(
                    (k, int(v) if v.isdigit() else v)
                        for (k, v) in e.items()
                )

    def parse_users(self, users_file='Users.xml'):
        """
        Parse data into User objects

            <row
                Id="2"
                Reputation="101"
                CreationDate="2011-01-03T20:14:55.783"
                DisplayName="Geoff Dalgas"
                LastAccessDate="2012-12-19T00:28:45.110"
                WebsiteUrl="http://stackoverflow.com"
                Location="Corvallis, OR"
                AboutMe="&lt;p&gt;Developer on ...."
                Views="6"
                UpVotes="6"
                DownVotes="0"
                EmailHash="b437f461b3fd27387c5d8ab47a293d35"
                Age="36"
            />
        """
        for user in self._parse_file(users_file):
            if user['Id'] == '-1':
                continue
            yield User.objects.create(
                id=user['Id'],
                email=user.get('EmailHash', ''),
                date_joined=date_parser.parse(user['CreationDate']),

                display_name=user['DisplayName'],
                url=user.get('WebsiteUrl', ''),
                location=user.get('Location', ''),
                description=user.get('AboutMe', ''),

                views=user['Views'],
                votes_up=user['UpVotes'],
                votes_down=user['DownVotes'],
                age=user.get('Age', 0)
            )
    

    def parse_comments(self, comments_file='Comments.xml'):
        """
        Comments.xml:

            <row
                Id="9"
                PostId="9"
                Score="3"
                Text="Point.... "
                CreationDate="2011-01-03T21:16:09.603"
                UserId="60"
            />
        """
        for comment in self._parse_file(comments_file):
            if comment['PostId'] in self._answers:
                cls = AnswerComment
            elif comment['PostId'] in self._questions:
                cls = QuestionComment
            else:
                continue

            yield cls.objects.create(
                post_id=comment['PostId'],
                owner_id=comment['UserId'],
                creation_date=date_parser.parse(comment['CreationDate']),
                score=comment['Score'],
                text=comment['Text']
            )


    def parse_posts(self, posts_file='Posts.xml'):
        """
            Posts.xml:
            Q:  <row
                Id="5"
                PostTypeId="1"
                AcceptedAnswerId="73"
                CreationDate="2011-01-03T20:52:52.880"
                Score="39"
                ViewCount="5638"
                Body="&lt;p&gt;....."
                OwnerUserId="24"
                LastEditorUserId="97"
                LastEditDate="2011-01-06T11:34:27.610"
                LastActivityDate="2012-01-27T19:12:50.900"
                Title="What are the differences between NoSQL and a traditional RDBMS?"
                Tags="&lt;nosql&gt;&lt;rdbms&gt;&lt;database-recommendation&gt;"
                AnswerCount="5"
                CommentCount="0"
                FavoriteCount="22"
            />

            A: <row
                Id="12"
                PostTypeId="2"
                ParentId="3"
                CreationDate="2011-01-03T21:01:19.160"
                Score="15"
                Body="&lt;p&gt;In ..."
                OwnerUserId="14"
                LastActivityDate="2011-01-03T21:01:19.160"
                CommentCount="3"
            />
        """

        for data in self._parse_file(posts_file):
            try:
                cls = POST_TYPES[data['PostTypeId']]
            except KeyError:
                # unknown post type, ignore
                continue

            post = cls(
                id=data['Id'],
                owner_id=data['OwnerUserId'],
                creation_date=date_parser.parse(data['CreationDate']),
                last_activity_date=date_parser.parse(data['LastActivityDate']),
                score=data['Score'],
                body=data['Body'],
                comment_count=data['CommentCount']
            )

            if isinstance(post, Question):
                post.answer_count = data['AnswerCount']
                post.tags_string = data['Tags']
                post.title = data['Title']
                post.favorite_count = data.get('FavoriteCount', 0)
                post.view_count = data['ViewCount']
                if 'AcceptedAnswerId' in data:
                    post.accepted_answer_id = data['AcceptedAnswerId']
                if 'LastEditorUserId' in data:
                    post.last_editor_id = data['LastEditorUserId']
                    post.last_edit_date = date_parser.parse(data['LastEditDate'])

                self._questions.add(post.pk)
            else:
                self._answers.add(post.pk)
                post.question_id = data['ParentId']

            post.save(force_insert=True)

            yield post
