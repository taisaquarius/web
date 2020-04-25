# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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