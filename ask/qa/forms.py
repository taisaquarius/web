from django import forms
from qa.models import Question, Answer, User, Session
import hashlib
from django.contrib.auth import authenticate 

class AskForm(forms.Form):
    title = forms.CharField(max_length=100)
    text = forms.CharField(widget=forms.Textarea)
    author = forms.CharField(max_length=100,required=False)

    def __init__(self, *args, **kwargs):
        super(AskForm, self).__init__(*args, **kwargs)
    
    def clean(self):
        return self.cleaned_data

    def save(self):
        author = User.objects.get(username=self.cleaned_data['author'])
        question = Question(title=self.cleaned_data['title'], text=self.cleaned_data['text'], author=author)
        question.save()
        return question
        



class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    question = forms.IntegerField()
    author = forms.CharField(max_length=100, required=False)


    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)

    def save(self):
        author = User.objects.get(username=self.cleaned_data['author'])
        answer = Answer(text=self.cleaned_data['text'], question_id=self.cleaned_data['question'], author=author)
        answer.save()
        return answer

    def clean(self):
        return self.cleaned_data


def salt_and_hash(password):
    hash = hashlib.md5(password.encode('utf-8')).hexdigest()
    return hash

class NewUser(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(NewUser, self).__init__(*args, **kwargs)

    def save(self):
        print("Replace password")
        # print(self.fields)
        password = salt_and_hash(self.cleaned_data['password'])
        user = User(username=self.cleaned_data['username'], email=self.cleaned_data['email'], password=password)
        user.save()
        return user
    
    def clean(self):
        return self.cleaned_data


class Login(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(Login, self).__init__(*args, **kwargs)

    def clean(self):
        return self.cleaned_data

    def save(self):
        user = User(username=self.cleaned_data['username'],
          password=self.cleaned_data['password'])
        user.save()
        return user