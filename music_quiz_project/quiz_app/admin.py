from django.contrib import admin

from .models import Category, Quiz, Question, Answer, Profile

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'sort_number']
    prepopulated_fields = {'slug': ('title',)} 
    ordering = ['sort_number']


class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_published', 'sort_number']
    prepopulated_fields = {'slug': ('title',)} 
    ordering = ['category', 'sort_number']
    list_filter = ['category']
    search_fields = ['title']
    search_help_text = 'Поиск по названию викторины'

    """Для страницы вывода отдельной записи"""
    readonly_fields = ['created', 'updated']
    fieldsets = [     
        (
            'Название и категория викторины',
            {
                'classes': ['wide'],      
                'fields': ['title', 'slug','category'],
            },
        ),
        (
            'Описание, статус публикации, порядковый номер в списке викторин',
            {
                'classes': ['collapse'],   
                'fields': ['description', 'is_published', 'sort_number'],
            },
        ),
        (
            None,
            {
                'description': 'Даты создания и изменения устанавливаются автоматически',
                'fields': ['created', 'updated']
            },
        ),
    ]


class AnswerTabularInLine(admin.TabularInline):
    model = Answer
    min_num = 2
    extra = 0


class QuestionAdmin(admin.ModelAdmin):
    inlines = (AnswerTabularInLine,)
    list_display = ['quiz', 'question']
    ordering = ['quiz']
    list_filter = ['quiz']


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_teacher']
    list_filter = ['is_teacher']

    """Для страницы вывода отдельной записи"""
    fields = ['user', 'is_teacher']
    

admin.site.register(Category, CategoryAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Profile, ProfileAdmin)

