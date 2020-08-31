from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from . managers import CustomUserManager
# Create your models here.

# Creating CustomUser so that the email would be used as the unique field instead 
# of django default user name and to differentiate between users that can create 
# story and questions from users who can only take the test.
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('Email address'), unique=True)
    first_name = models.CharField(_('First name'), max_length=20)
    last_name = models.CharField(_('Last name'), max_length=20)
    username = models.CharField(_('Preferred username'), max_length=20)
    is_staff = models.BooleanField(_('staff'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    date_joined = models.DateTimeField(_('date joined'),auto_now_add=True)
    last_login = models.DateTimeField(_('last login'), auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    objects = CustomUserManager()

    def __str__(self):
        return '%s %s' %(self.first_name, self.last_name)
    def get_email(self):
        return self.email

# Supervisor model to add extra fields to the user model
# Not entirely necesary right now but in future the app 
# might want to track users who created which questions
class Supervisor(models.Model):
    is_guest = models.BooleanField(_('guest'), default=False)
    is_supervisor = models.BooleanField(_('supervisor'), default=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    company = models.CharField(_('Grant organizers'), max_length=100)
    objects = models.Manager()

    def __str__(self):
        return self.company

class Story(models.Model):
    """LEVEL = (
        ('Junior','Junior'),
        ('Intermediate','Intermediate'),
        ('Senior','Senior'),
    )
    level = models.CharField(_('Level the material is meant for'), choices=LEVEL, max_length=12)"""
    topic = models.CharField(_('Topic'), max_length=50, null=True)
    text = models.TextField(_('Short story that the questions will be based on'))
    author = models.ForeignKey(Supervisor, on_delete=models.CASCADE)
    objects = models.Manager()

    class Meta:
        verbose_name_plural = 'Stories'

    def __str__(self):
        return self.topic

class Question(models.Model):
    question_text = models.TextField(_('Question text'))
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    objects = models.Manager()

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    choice_text = models.CharField(_('Choice text'), max_length=200)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)
    objects = models.Manager()

    def __str__(self):
        return self.choice_text

class Result(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    score= models.IntegerField(_('Score'), blank=True)
    
    @property
    def status(self):
        grade = self.score * 5
        final_grade = (grade/50)*100
        if final_grade > (75/100):
            return "Passed"
        else:
            return "Failed"