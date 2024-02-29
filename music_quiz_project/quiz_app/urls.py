from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('add-quiz/', views.add_quiz_form_view, name='addquiz'),
    path('add-question/', views.add_question_form_view, name='addquestion'),
    path('<slug:category_slug>/', views.category_view, name='cat'),
    path('<slug:category_slug>/<slug:quiz_slug>/', views.quiz_view, name='quiz'),
    
]