# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User

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
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='question_like_user')
    class Meta:
        db_table = 'Question'


class Answer(models.Model):
    objects = models.Manager()
    text = models.TextField('')
    added_at = models.DateTimeField(auto_now_add=True)
    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name='answer_set')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        db_table = 'Answer'
