from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('signup/', views.signup, name='signup'),
    path('users/<username>/', views.profile, name='profile'),
    path('title/update/<username>/', views.update_title, name='update_title'),
    path('generate_quiz/', views.generate_quiz, name='generate_quiz'),
    path('start_quiz/', views.start_quiz, name='start_quiz'),
    path('random/', views.random_question, name='random_question'),
    path('quiz_completed/', views.quiz_completed, name='quiz_completed'),
]

