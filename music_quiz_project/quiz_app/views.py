from django.utils.safestring import SafeString
from music_quiz_project.settings import MEDIA_URL
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify 
from .models import Category, Quiz, Question
from .forms import AddQuizForm, AddQuestionForm, AddAnswerInlineFormset, CreateProfileForm
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import login, logout, authenticate
import logging

logger = logging.getLogger(__name__)


def index_view(request): 
    categories = Category.objects.all().order_by('sort_number')
    context = {
        'title' : 'Главная страница',
        'categories' : categories, 
    }

    logger.info('Index page accessed')

    return render(request, "quiz_app/index.html", context)
    

def category_view(request, category_slug): 
    category = get_object_or_404(Category, slug=category_slug)
    quizzes = Quiz.objects.filter(category=category, is_published=True).order_by('sort_number')
    context = {
        'title' : f'Викторины: {category.title}',
        'category' : category,
        'quizzes' : quizzes, 
    }

    logger.info('Category page accessed')

    return render(request, "quiz_app/category.html", context)


def quiz_view(request, category_slug, quiz_slug): 
    quiz = get_object_or_404(Quiz, slug=quiz_slug, category__slug=category_slug)
    questions = quiz.question_set.all().prefetch_related('answer_set')

    quiz_data = {
        'questions': []
    }

    for question in questions:
        _html = f'{question.question}</h2>'
        _html += f'<div style="margin:-8px 0 20px">' \
                f'<img src="{MEDIA_URL}{question.image}">' \
                f'</div>' if question.image else ''
        _html += f'<p style="margin-top:-8px; line-height:1.4">' \
                f'{question.full_text}' \
                f'</p>' if question.full_text else ''
        _html += '<h2>'

        question_data = {
            'q': _html,
            'a': '',
            'options': [],
        }

        for answer in question.answer_set.all():
            if answer.is_correct:
                question_data['a'] = answer.answer
            question_data['options'].append(answer.answer)

        quiz_data['questions'].append(question_data)

    context = {
        'title': quiz.title,
        'quiz_data': SafeString(quiz_data),
    }

    if request.user.is_authenticated:
        logger.info(f'User {request.user} took {quiz}')
    else:
        logger.info(f'Guest took {quiz}')
    
    return render(request, "quiz_app/quiz.html", context)
    
    
def add_quiz_form_view(request):
    if request.method == 'POST':
        form = AddQuizForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            slug = slugify(title, allow_unicode=False)
            description = form.cleaned_data['description']
            category = form.cleaned_data['category']
            is_published = form.cleaned_data['is_published']
            sort_number = form.cleaned_data['sort_number']

            quiz = Quiz(title=title, slug=slug, description=description, category=category, is_published=is_published, sort_number=sort_number)
            quiz.save()

            logger.info(f'Received and saved data: quiz {quiz} in category {category}')

            return redirect('addquestion')
    else:
        form = AddQuizForm()
    return render(request, 'quiz_app/add_quiz_form.html', {'form': form})
    
    
def add_question_form_view(request):
    if request.method == 'POST':
        form = AddQuestionForm(request.POST, request.FILES)
        answer_formset = AddAnswerInlineFormset(request.POST)
        if form.is_valid() and answer_formset.is_valid():
            quiz = form.cleaned_data['quiz']
            question = form.cleaned_data['question']
            full_text = form.cleaned_data['full_text']
            image = form.cleaned_data['image']
            fs = FileSystemStorage()
            fs.save(image.name, image)   

            question = Question(quiz=quiz, question=question, full_text=full_text, image=request.FILES['image'])
            question.save()
            answers = answer_formset.save(commit=False)

            for answer in answers:
                answer.question = question
                answer.save()

            logger.info(f'Received and saved data: question {question} and answers for quiz {quiz}')

            return redirect('index')
    else:
        form = AddQuestionForm()
        answer_formset = AddAnswerInlineFormset()
    return render(request, 'quiz_app/add_question_form.html', {'form': form, 'answer_formset': answer_formset})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('index') 
    else: 
        form = CreateProfileForm()
        if request.method == 'POST':
            form = CreateProfileForm(request.POST)
            if form.is_valid() :
                user = form.save()
                user.refresh_from_db()
                user.profile.first_name = form.cleaned_data.get('first_name')
                user.profile.last_name = form.cleaned_data.get('last_name')
                user.profile.is_teacher = form.cleaned_data.get('is_teacher')
                user.save()
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                login(request, user)

                logger.info(f'User {user} is registered and logged in')

                return redirect('/')
        return render(request,'quiz_app/register.html', {'form' : form})
 

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                logger.info(f'User {user} has logged in')

                return redirect('/')
        return render(request,'quiz_app/login.html', {})
    

def logout_view(request):
    logout(request)

    logger.info('User has logged out')

    return redirect('/')
