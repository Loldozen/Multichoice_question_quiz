from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from . import views

app_name = 'Test'
urlpatterns = [
    path('', views.HomepageView.as_view(), name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', views.signup, name='signup'),
    path('signup/<str:access>/', views.signup, name='supervisor_signup'),
    #path('login/', auth_views.LoginView.as_view(template_name='Test/login.html'), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(template_name='Test/logout.html'),  name='logout'),
    path('story/<int:pk>/', views.StoryDetails.as_view(), name='story_details'),
    path('story/<int:pk>/questions/', views.QuestionView.as_view(), name='questions'),
    path('story/create/', views.createStory, name='create_story'),
    path('story/edit/<int:pk>/', views.editStory, name='edit_story'),
    path('story/delete/<int:pk>/', views.DeleteStory.as_view(), name='delete_story'),
    path('<int:pk>/question/create/', views.createQuestion, name='create_questions'),
    path('profile/', views.Profile.as_view(), name='profile'),
]