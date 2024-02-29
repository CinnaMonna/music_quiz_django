from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class Category(models.Model):
    title = models.CharField('название', max_length=150)
    slug = models.SlugField('URL', unique=True)
    description = models.TextField('описание', blank=True)
    sort_number = models.PositiveSmallIntegerField('номер п/п', default=0)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'categories'
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
    
    def get_absolute_url(self):
        return reverse(
            'category',
            kwargs={
                'category_slug': self.slug,
            }
        )


class Quiz(models.Model):
    title = models.CharField('название', max_length=150)
    slug = models.SlugField('URL', unique=False)
    description = models.TextField('описание', blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='категория')
    is_published = models.BooleanField('опубликован', default=True)
    created = models.DateTimeField('создан', auto_now_add=True)
    updated = models.DateTimeField('изменен', auto_now=True)
    sort_number = models.PositiveSmallIntegerField('номер п/п', default=0)

    def __str__(self):
        return f'{self.title} ({self.category})'
    
    class Meta:
        db_table = 'quiz'
        verbose_name = 'викторина'
        verbose_name_plural = 'викторины'
        unique_together = ('slug', 'category')

    def get_absolute_url(self):
        return reverse(
            'quiz',
            kwargs={
                'quiz_slug': self.slug,
                'category_slug': self.category.slug,
            }
        )
    
   
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, verbose_name='викторина')
    question = models.CharField('вопрос', max_length=150)
    full_text = models.TextField('описание вопроса', blank=True)
    image = models.ImageField('изображение', upload_to='quiz', blank=True)

    def __str__(self):
        return self.question[:50]
    
    class Meta:
        db_table = 'questions'
        verbose_name = 'вопрос'
        verbose_name_plural = 'вопросы'
 

class Answer(models.Model):
    answer = models.CharField('ответ', max_length=150)
    is_correct = models.BooleanField('правильный ответ', default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='вопрос')
    
    def __str__(self):
        return self.answer

    class Meta:
        db_table = 'answers'
        verbose_name = 'ответ'
        verbose_name_plural = 'ответы'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_teacher = models.BooleanField('является ли преподавателем', default=False, blank=True)

    def __str__(self):
        return self.user.username
    
    class Meta:
        db_table = 'profiles'
        verbose_name = 'профиль пользователя'
        verbose_name_plural = 'профили пользователей'

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()