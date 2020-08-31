from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.apps import apps

from .forms import SignupForm, SupervisorSignupForm, UserEditForm
from .models import CustomUser, Supervisor, Story, Question, Choice
# Register your models here.
 
 # Displaying the user model on the admin page with details of each instances
class CustomUserAdmin(UserAdmin):
    add_form = SignupForm
    form = UserEditForm
    model = CustomUser
    list_display = ('email','first_name','last_name','username','last_login','is_active')
    list_filter = ('first_name','last_name','username')
    fieldsets = (
        (None, {'fields':('email','first_name','last_name','username','password',)}),
        ('Pemissions',{'fields':('last_login','is_active','is_staff')}),
    )
    add_fieldsets = (
        (None,{
            'classes': ('wide',),
            'fields': ('email','first_name','last_name', 'password1', 'password2', 'is_staff', 'is_active')
        }
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
admin.site.register(CustomUser, CustomUserAdmin)

class ChoiceAdmin(admin.StackedInline):
    model = Choice
    extra = 4

class QuestionAdmin(admin.ModelAdmin):
    
    model = Question
    inlines = [ChoiceAdmin]
    list_display = ['story', 'question_text']
    list_filter = ['question_text',]
admin.site.register(Question,QuestionAdmin )

# Class to automatically register all models in the app on the admin page
class ListAdminMixin(object):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields if field.name != "id"]
        super(ListAdminMixin,self).__init__(model,admin_site)

models = apps.get_models()
for model in models:
    admin_class = type('AdminClass',(ListAdminMixin, admin.ModelAdmin),{})
    try:
        admin.site.register(model, admin_class)
    except admin.sites.AlreadyRegistered:
        pass