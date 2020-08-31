from django import forms
from django.forms import modelformset_factory, inlineformset_factory
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db import transaction

from .models import CustomUser, Supervisor, Story, Question, Choice

# Creating the signup form from the user model for the signup view

class SignupForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('first_name','last_name','email','username',)

class UserEditForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('first_name','last_name','email','username',)

class SupervisorSignupForm(forms.ModelForm):
    
    class Meta:
        model = Supervisor
        fields = ('company',)
        
    @transaction.atomic
    def save(self, user=None):
        supervisor = super().save(commit=False)
        supervisor.is_supervisor = True
        supervisor.user = user
        supervisor.save()
        return user

class StoryForm(forms.ModelForm):
    
    class Meta:
        model = Story
        fields = ('topic', 'text')

    @transaction.atomic
    def save(self, user=None):
        story = super().save(commit=False)
        story.author = user.supervisor
        story.save()
        return user

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('story','question_text')

    @transaction.atomic
    def save(self, story=None):
        question = super().save(commit=False)
        question.story = story
        question.save()
        return question

QuestionFormset = modelformset_factory(
    Question,
    #fields = ('story','question_text'),
    form=QuestionForm,
    extra=10, 
    can_delete=True
)

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ('question','choice_text','is_correct')

    @transaction.atomic
    def save(self, question=None):
        choice = super().save(commit=False)
        choice.question = question
        choice.save()
        return choice
        
ChoiceFormset = inlineformset_factory(
    parent_model=Question,
    model=Choice,
    form=ChoiceForm,
    extra=4,
    can_delete=True,
    )