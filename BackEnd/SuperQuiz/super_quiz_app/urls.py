from django.urls import path

from . import views

urlpatterns = [
    # path('questions/<int:question_id>/', views.question_detail, name="question_detail"),
    path('', views.home, name="home"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('signup/', views.signup, name='signup'),
    path('users/<username>/', views.profile, name='profile'),
    path('title/create/', views.create_title, name='create_title'),
    # path('title/edit/<int:quiz_id>/', views.edit_title, name='edit_title'),
    path('profile/delete/', views.delete_profile, name='delete_profile'),
    path('generate_quiz/', views.generate_quiz, name='generate_quiz'),
    path('start_quiz/', views.start_quiz, name='start_quiz'),
    path('random/', views.random_question, name='random_question'),
    path('quiz_completed/', views.quiz_completed, name='quiz_completed'),
]

