# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os                                                                                                                                             
import unittest                                                                                                                                       
import sys 
from django.contrib.auth.models import User                                                                                                           
from django.db.models import Max                                                                                                                      
from django.utils import timezone 
import time

from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET
from django.core.paginator import Paginator

from qa.models import Question, Answer

# Create your views here.
from django.http import HttpResponse

def test(request, *args, **kwargs):
    return HttpResponse('OK')



def new_question(request):
    questions = Question.objects.new()
    limit = request.GET.get('limit', 10)
    page_number = request.GET.get('page', 1)
    paginator = Paginator(questions, limit)
    paginator.baseurl = '/?page='
    page = paginator.page(page_number)
    return render(request,'main_page.html',{
        'questions': page.object_list, 
        'page': page, 
        'paginator': paginator
    })

def popular_question(request):
    questions = Question.objects.popular()
    limit = request.GET.get('limit', 10)
    page_number = request.GET.get('page', 1)
    paginator = Paginator(questions, limit)
    paginator.baseurl = '/popular/?page='
    page = paginator.page(page_number)
    return render(request,'page_with_popular_q.html',{
        'questions': page.object_list, 
        'page': page, 
        'paginator': paginator
    })


@require_GET
def question(request,slug):
    question = get_object_or_404(Question, id = slug)
    try:
        answers = Answer.objects.all().filter(question_id = slug)
    except answers.DoesNotExist:
        answers = None
    return render(request, 'question_page.html', {
        'question': question,
        'answers': answers })

def new(request):
    res = Question.objects.all().aggregate(Max('rating'))                                                                                         
    max_rating = res['rating__max'] or 0                                                                                                          
    user, _ = User.objects.get_or_create(                                                                                                         
            username='x',                                                                                                                             
            defaults={'password':'y', 'last_login': timezone.now()})                                                                                  
    for i in range(30):                                                                                                                           
        question = Question.objects.create(                                                                                                       
            title='question ' + str(i),                                                                                                           
            text='text ' + str(i),                                                                                                                
            author=user,                                                                                                                          
            rating=max_rating+i                                                                                                                   
        )                                                                                                                                         
    time.sleep(2)                                                                                                                                 
    question = Question.objects.create(title='question last', text='text', author=user)                                                           
    question, _ = Question.objects.get_or_create(pk=3141592, title='question about pi', text='what is the last digit?', author=user)              
    question.answer_set.all().delete()                                                                                                            
    for i in range(10):                                                                                                                           
        answer = Answer.objects.create(text='answer ' + str(i), question=question, author=user)