from django.db import models
from django.shortcuts import reverse
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class Course(models.Model):
    name = models.CharField(max_length=20,verbose_name='Название курса')
    description = models.CharField(max_length=200, verbose_name='Описание курса')

    def __str__(self):
        return self.name

    # генерация ссылок на курс
    def get_absolute_url(self):
        return reverse('course_detail_url', kwargs={'name': self.name})


# 1 - преподаватель
# 2 - студент
class UserType(models.Model):
    user_type = models.CharField(max_length=30)

    def __str__(self):
        return self.user_type


class User(AbstractUser):
    avatar = models.ImageField(null=True, blank=True, upload_to='media', verbose_name='Аватарка', default='media/default.png')
    user_type = models.ForeignKey(UserType, on_delete=models.CASCADE, null=True, verbose_name='Тип пользвателя')
    username = models.TextField(verbose_name='Имя пользователя', unique=True)
    description = models.TextField(null=True, verbose_name='О себе')
    first_name = models.TextField(verbose_name='Имя')
    last_name = models.TextField(verbose_name='Фамилия')
    course = models.ForeignKey(Course, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('user_detail_url', kwargs={'username': self.username})


class Lesson(models.Model):
    number = models.IntegerField(verbose_name='Номер урока')
    theme = models.CharField(max_length=50, verbose_name='Тема урока')
    time = models.TimeField(verbose_name='Время урока')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')

    def __str__(self):
        return '{} {}'.format(self.number, self.theme)

    # генерация ссылок на урок
    def get_absolute_url(self):
        return reverse('lesson_detail_url', kwargs={'id': self.id})


class Test(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='По темам урока')
    theme = models.CharField(max_length=20, verbose_name='Тема тестирования')

    def __str__(self):
        return self.theme

    def get_absolute_url(self):
        return reverse('test_detail_url', kwargs={'id': self.id})


class Question(models.Model):
    text = models.CharField(max_length=80, verbose_name='Вопрос')
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    right_answer = models.CharField(max_length=100, verbose_name='Ответ')

    def __str__(self):
        return self.text


class TestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    date = models.DateTimeField()


class UserAnswer(models.Model):
    test = models.ForeignKey(TestResult, on_delete=models.CASCADE)
    answer = models.CharField(max_length=100, verbose_name='Ответ')
