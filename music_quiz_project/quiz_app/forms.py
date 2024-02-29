from django import forms
from django.forms import ModelForm, inlineformset_factory
from .models import Quiz, Question, Answer
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class AddQuizForm(ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'category', 'is_published', 'sort_number']


class AddQuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = "__all__"


class AddAnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['answer', 'is_correct']

AddAnswerInlineFormset = inlineformset_factory(Question, Answer, form=AddAnswerForm, extra=5)


class CreateProfileForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, help_text='Имя')
    last_name = forms.CharField(max_length=100, help_text='Фамилия')
    is_teacher = forms.BooleanField(required=False, label='Я - преподаватель')

    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'is_teacher', 'password'] 