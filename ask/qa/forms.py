from django import forms
from qa.models import Question, Answer

class AskForm(forms.Form):
    title = forms.CharField(max_length=100)
    text = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(AskForm, self).__init__(*args, **kwargs)

    def clean(self):
        # title = self.cleaned_data['title']
        # text = self.cleaned_data['text']
        # if not is_ethic(text):
        #     raise forms.ValidationError(u'Incorrect text')
        # return Question(title=title, text=text)
        return self.cleaned_data

    def save(self):
        question = Question(title=self.cleaned_data['title'], text=self.cleaned_data['text'])
        question.save()
        return question




class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    question = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)

    def save(self):
        answer = Answer(text=self.cleaned_data['text'], question_id=self.cleaned_data['question'])
        answer.save()
        return answer

    def clean(self):
        return self.cleaned_data