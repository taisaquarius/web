# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os                                                                                                                                             
import unittest                                                                                                                                       
import sys 
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate                                                                                                          
from django.db.models import Max                                                                                                                      
from django.utils import timezone 
import time
from datetime import datetime, timedelta
import uuid
import hashlib
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET
from django.core.paginator import Paginator

from qa.models import Question, Answer, User, Session
from qa.forms import AskForm, AnswerForm, NewUser, Login
from qa.utils import get_user_by_session

import random
import string

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect

def test(request, *args, **kwargs):
    return HttpResponse('OK')

def authenticate_user(login, password):
    try:
        print("Try to login user '" , login, "' and password '", password, "'")
        user = User.objects.get(username=login)
        if user.password == hashlib.md5(password.encode('utf-8')).hexdigest():
            return user
        else:
            return None
    except Exception as exception:
        print("Authenticate error: ", type(exception), ", args: ", exception.args)
        return None

# def salt_and_hash(password):
#     hash = hashlib.md5(password).hexdigest()
#     return hash

def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def do_login(user,url):
    expires = datetime.now(tz=timezone.utc) + timedelta(days=5)
    session = Session.objects.create(key=randomString(5), user=user, expires=expires)
    print("New session:", session.key, ", user:", user)
    response = HttpResponseRedirect(url)
    response.set_cookie('sessionid', session.key,
     httponly=True, expires=session.expires)
    return response

def new_questions(request):
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


def question(request,slug):
    question = get_object_or_404(Question, id = slug)
    try:
        answers = Answer.objects.all().filter(question_id = slug)
    except answers.DoesNotExist:
        print('answers were not found for question', slug)
        answers = None
    if request.method == "GET":
        author = get_user_by_session(request)
        form = AnswerForm()
        if author is not None:
            form.fields["author"].initial = author.username
            print('user', author, 'was extracted from session')
        return render(request, 'question_page.html', {
            'question': question,
            'answers': answers,
            'form': form })
    else:
        author = get_user_by_session(request)
        form = AnswerForm(request.POST)
        if author is not None:
            form.fields["author"].initial = author.username
            print('user', author, 'was extracted from session')
        if form.is_valid():
            form.save()
            print('answer was saved')
        else:
            print('answer form is invalid')
            print(form.errors)
        return render(request,'question_page.html', {
            'question': question,
            'answers': answers,
            'form': form })


def create_question(request):
    print('create question request', request)
    author = get_user_by_session(request)
    if request.method == "POST":
        form = AskForm(request.POST)
        # author = get_user_by_session(request)
        # form.author.default = author.username
        if author is not None:
            print('author was found: ', author)
            # form.fields["author"].initial = author.username
            form.cleaned_data['author'] = author.username
        if form.is_valid():
            question = form.save()
            id = question.id
            return HttpResponseRedirect('/question/'+str(id))
        else:
            print(form.errors)
    else:
        form = AskForm()
        if author is not None:
            print('author was found: ', author)
            # form.fields["author"].initial = author.username
        # form.author.initial = author.username
        return render(request,'ask_form.html', {'form': form})


def signup(request):
    if request.method == "POST":
        form = NewUser(request.POST)
        
        if form.is_valid():
            print("NewUser form is valid")
            user = form.save()
            url = request.POST.get('continue', '/')
            return do_login(user,url)
        else:
            print("NewUser form is invalid")
            print(form.errors)
    else:
        form = NewUser()
        return render(request, 'signup_form.html', {'form': form})


def login(request):
    error = ''
    if request.method == 'POST':
        login = request.POST.get('username')
        password = request.POST.get('password')
        url = request.POST.get('continue', '/')
        # user = authenticate(request, username=login,password=password)
        user = authenticate_user(login, password)
        print(user)
        if user is not None:
           return do_login(user,url)
        else:
            error = u'Uncorrect login / password'
            form = Login()
            return render(request, 'login_form.html', {'error': error, 'form': form})
    else:
        form = Login()
        return render(request, 'login_form.html', {'error': error, 'form': form})


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