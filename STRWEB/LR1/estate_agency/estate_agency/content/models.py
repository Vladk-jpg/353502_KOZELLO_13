from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class About(models.Model):
    company_info = models.TextField(verbose_name='Информация о компании')
    video_link = models.FileField(upload_to='videos/', verbose_name='Видео', blank=True, null=True)
    logo = models.ImageField(upload_to='logos/', verbose_name='Логотип', blank=True, null=True)
    history = models.TextField(verbose_name='История компании', blank=True, null=True)
    requisites = models.TextField(verbose_name='Реквизиты компании', blank=True, null=True)
    sertificate = models.TextField(verbose_name='Сертификат компании', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'About'
        verbose_name_plural = 'About'
        ordering = ['-created_at']

    def __str__(self):
        return 'About company'

class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    image = models.ImageField(upload_to='articles/', verbose_name='Изображение')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_short_content(self):
        return self.content[:200] + '...' if len(self.content) > 200 else self.content

class FAQ(models.Model):
    question = models.CharField(max_length=255, verbose_name='Вопрос')
    answer = models.TextField(verbose_name='Ответ')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'
        ordering = ['-created_at']

    def __str__(self):
        return self.question

class Vacancy(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название вакансии')
    description = models.TextField(verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Vacancy'
        verbose_name_plural = 'Vacancies'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Review(models.Model):
    user_name = models.CharField(max_length=100, verbose_name='Имя пользователя')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Оценка'
    )
    text = models.TextField(verbose_name='Текст отзыва')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ['-created_at']

    def __str__(self):
        return f'Отзыв от {self.user_name}'
    
class Partners(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название партнера')
    image = models.ImageField(upload_to='partners/', verbose_name='Изображение')
    link = models.URLField(verbose_name='Ссылка на партнера')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Partner'
        verbose_name_plural = 'Partners'
        ordering = ['-created_at']

    def __str__(self):
        return self.name