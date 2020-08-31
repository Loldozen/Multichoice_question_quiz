from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse, HttpResponseForbidden
from django.views import View
from django.views.generic import CreateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.db import transaction

from .models import Supervisor, Story, Question, Choice, Result
from .forms import SignupForm, SupervisorSignupForm
from . import forms

User = get_user_model()
# Create your views here.

def signup(request, access='guest'):
    if access == 'guest':
        if request.method == 'POST':
            form = SignupForm(request.POST)
            if form.is_valid():
                user = form.save()
                user.save()
                return redirect('Test:login')
        else:
            form = SignupForm()
        return render(request, 'Test/signup.html', {'form':form})

    elif access == 'supervisor':
        if request.method == 'POST':
            user_form = SignupForm(request.POST)
            supervisor_form = SupervisorSignupForm(request.POST)
            if user_form.is_valid() and supervisor_form.is_valid():
                user = user_form.save()
                supervisor = supervisor_form.save(user=user)
                user.save()
                supervisor.save()
                return redirect('Test:login')
        else:
            user_form = SignupForm()
            supervisor_form = SupervisorSignupForm()
        return render(request, 'Test/supervisor_signup.html', {'user_form':user_form, 'supervisor_form':supervisor_form, 'access':access})

"""class StoryCreate(CreateView):
    model = Story
    fields = ['topic', 'text']
    #form_class = forms.StoryForm
    template_name = 'Test/create_story.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class StoryEdit(UpdateView):
    model = Story
"""

@login_required(login_url='Test:login')
#@permission_required('Test.is_supervisor', login_url='Test:login')
def createStory(request):
    if  not request.user.supervisor.is_supervisor:
        return HttpResponseForbidden()
    if request.method == 'POST': #process the form only if the call method os post
        form = forms.StoryForm(request.POST )
        if form.is_valid() :
            # pass the current user to the author field in modelform
            story = form.save(user=request.user)
            story.save()
            return redirect('Test:profile')
    else: #if call method is GET return empty form
        form = forms.StoryForm()
    return render(request, 'Test/create_story.html', {'form':form} )

@login_required
@permission_required('Test.is_supervisor')
def editStory(request, pk ):
    edit = get_object_or_404(Story, pk=pk )

    if request.method == 'POST':
        form = forms.StoryForm(request.POST, instance=edit)
        if form.is_valid():
            form.save(user=request.user)
            return redirect('Test:story_details', pk=pk) #redirect(reverse('Test:story_details', kwargs={'pk':pk}))
    else:
        form = forms.StoryForm(instance=edit)
        return render(request,'popat/create_story.html', {'form':form})

class DeleteStory(DeleteView):
    model = Story
    template_name = 'Test/delete_story.html'
    success_url = 'Test:profile'

    @method_decorator(login_required, name='dispatch')
    @method_decorator(permission_required('popat.is_supervisor'), name='dispatch')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@login_required(login_url='Test:login')
#@permission_required('Test.is_supervisor', login_url='Test:login')
def createQuestion(request, pk):
    if  not request.user.supervisor.is_supervisor:
        return HttpResponseForbidden()
    story = get_object_or_404(Story, pk=pk)
    if request.method == 'POST':
        question_formset = forms.QuestionFormset(request.POST)
        choice_formset = forms.ChoiceFormset(request.POST)
        if question_formset.is_valid() and choice_formset.is_valid():
            # pass the story to the model's story field
            question = question_formset.save(story=story)
            question.save()
            # pass the question to the model's question field
            choices = choice_formset.save(question=question)
            choices.save()
            return redirect('Test:profile')
    else:
        question_formset = forms.QuestionFormset()
        choice_formset = forms.ChoiceFormset()
    return render(
        request,
        'Test/create_questions.html',
        {'question_formset':question_formset,'choice_formset':choice_formset,'story':story})

class Profile(DetailView):
    model = Supervisor
    template_name = 'Test/profile.html'
    context_object_name = 'supervisor'

    def get_queryset(self):
        return Supervisor.objects.get(user=self.request.user)
    def get_object(self):
        return Supervisor.objects.get(user=self.request.user)
        
class HomepageView(ListView):

    model = Story
    template_name = 'Test/home.html'
    context_object_name = 'story_list'

    #def get_queryset(self):
        #return Story.objects.order_by

class StoryDetails(DetailView):
    model = Story
    template_name = 'Test/story_details.html'
    context_object_name = 'story'

    def get_queryset(self, **kwargs):
        return Story.objects.get(pk=self.kwargs['pk'])

    def get_object(self, **kwargs):
        return Story.objects.get(pk=self.kwargs['pk'])

class QuestionView(SingleObjectMixin, ListView):

    model = Question
    template_name = 'Test/question.html'
    context_object_name = 'question_list'

    #def get_queryset(self, **kwargs):
        #return Question.objects.get(pk=self.kwargs['pk'])
    def get_queryset(self, **kwargs):
        self.story = get_object_or_404(Story, pk=self.kwargs['pk'])
        return Question.objects.filter(pk=self.story.id)

    def get_object(self, **kwargs):
        self.story = get_object_or_404(Story, pk=self.kwargs['pk'])
        return Question.objects.filter(pk=self.story.id)

def result(request, question_id):
    #story = get_object_or_404(Story, pk=story_id)
    question_list = get_object_or_404(Question, pk=question_id)
