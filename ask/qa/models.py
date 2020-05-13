# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User

import hashlib


# Create your models here.
class QuestionManager(models.Manager):
    def new(self):
        return self.order_by('-id')

    def popular(self):
        return self.order_by('-rating')

class Question(models.Model):
    objects = QuestionManager()
    title = models.CharField(max_length=255)
    text = models.TextField('')
    added_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    likes = models.ManyToManyField(User, related_name='question_like_user')
    class Meta:
        db_table = 'Question'


class Answer(models.Model):
    objects = models.Manager()
    text = models.TextField('')
    added_at = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answer_set')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    class Meta:
        db_table = 'Answer'

class Session(models.Model):
    objects = models.Manager()
    key = models.CharField(unique=True,max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expires = models.DateTimeField()

# class User(User):
#     def salt_and_hash(password):
#         hash = hashlib.md5(password).hexdigest()
#         return hash

#     def generate_key():
#         return uuid.uuid1()

#     def do_login(username, password):
#         try:
#             user = User.objects.get(username=username)
#         except User.DoesNotExist:
#             return None
#         hashed_pass = salt_and_hash(password)
#         if user.password != hashed_pass:
#             return None
#         session = Session()
#         session.key = generate_key()
#         session.user = user
#         session.expires = datetime.now() + timedelta(days=5)
#         session.save()
#         return session.key
