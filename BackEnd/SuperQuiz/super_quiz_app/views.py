
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse
import random
from .forms import QuizForm
from .models import Quiz
from django.utils import timezone


from .models import Question

#imports for authentication
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login 



def login(request):
    """ login to app"""
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username=u, password=p)
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    return redirect('/', username=u)
                else:
                    print(f'{u} - account has been disabled')
                    return HttpResponseRedirect('/login')
            else:
                print('The username and/or password is none')
                return HttpResponseRedirect('/login')
        else:
            print('The username and/or password is not valid')
            return HttpResponseRedirect('/login')
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', { 'form': form })
    
def logout(request):
    return HttpResponseRedirect('/login')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/login')
        else:
            return render(request, 'signup.html', { 'form': form })
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', { 'form': form })
    
@login_required
def profile(request, username):
    user = User.objects.get(username=username)
    quiz = None
    try:
        quiz = Quiz.objects.get(user_id=user.id);
    except Exception as e:
        print('No quiz to display!')   
    return render(request, 'profile.html', {'user': user, 'quiz_title': quiz})

@login_required
def home(request):
    return render(request, "home.html")

@login_required
def update_title(request, username):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username=username)
            try:
                oldQuiz = get_object_or_404(Quiz, user_id=user.id);
                oldQuiz.delete();
            except Exception as e:
                print('first quiz!!')    
            quiz = form.save(commit=False)
            quiz.id = quiz.id
            quiz.user_id = user.id
            quiz.pub_date = timezone.now()
            quiz.title = form.cleaned_data['title'];
            form.save()
            return render(request, 'profile.html', {'user': user, 'quiz_title': quiz.title})
    else:
        form = QuizForm()
        user = User.objects.get(username=username)
    return render(request, 'quiz/edit_title.html', {'form': form, 'user': user})

@login_required
def delete_title(request, username):
    if request.method == 'POST':
        user = User.objects.get(username=username)
        try:
            oldQuiz = get_object_or_404(Quiz, user_id=user.id);
            oldQuiz.delete();
        except Exception as e:
            print('failed to delete quiz!!, No quiz exist')    
        return render(request, 'profile.html', {'user': user, 'quiz_title': ''})

@login_required
def generate_quiz(num_questions):
    total_questions = Question.objects.count()
    num_questions = min(num_questions, total_questions)
    random_questions = random.sample(list(Question.objects.all()), num_questions)
    return random_questions

def start_quiz(request):
    return redirect('random_question')

@login_required
def quiz_completed(request, score):
    return render(request, 'quiz/quiz_completed.html', {
        'score': score
    })  
@login_required
def random_question(request):
    if request.method == "POST":
        id = request.session.get('current_question_id')
        question = get_object_or_404(Question, pk=id)
        selected_choice_id = request.POST.get('choice')
        selected_choice = get_object_or_404(question.choice_set, pk=selected_choice_id)
        feedback = None
        if selected_choice.is_correct:
            feedback = "Correct!"
            request.session['correct_answer_count'] = request.session.get('correct_answer_count') + 1;
        else:
            feedback = "Incorrect."
        return render(request, 'quiz/random_question.html', {
            'question': question,
            'feedback': feedback,
            'answer_disabled' : True
        })
    
    if request.session.get('session_end'):
        request.session['session_end'] = False
        score = request.session.get('correct_answer_count')
        request.session['correct_answer_count'] = 0;
        return quiz_completed(request, score)

    if not request.session.get('quiz_questions'):
        request.session['session_end'] = False
        request.session['correct_answer_count'] = 0
        question_ids = list(Question.objects.values_list('id', flat=True))
        question_ids = random.sample(question_ids, 5)
        random.shuffle(question_ids)
        request.session['quiz_questions'] = question_ids
    
    question_ids = request.session.get('quiz_questions', [])
    next_question_id = question_ids.pop()
    request.session['current_question_id'] = next_question_id
    request.session['quiz_questions'] = question_ids
    question = get_object_or_404(Question, pk=next_question_id)
    if not question_ids:
        request.session['session_end'] = True
    return render(request, 'quiz/random_question.html', {
        'question': question,
        'feedback': None,
        'answer_disabled' : False
    })



