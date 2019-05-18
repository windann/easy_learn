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

    def join_to_group_url(self):
        return reverse('join_group', kwargs={'name': self.name})

    def update(self):
        return reverse('course_update_url', kwargs={'name': self.name})

    def add_lesson(self):
        return reverse('lesson_create_url', kwargs={'name': self.name})


# 1 - преподаватель
# 2 - студент
class UserType(models.Model):
    user_type = models.CharField(max_length=30)

    def __str__(self):
        return self.user_type


class Lesson(models.Model):
    number = models.IntegerField(verbose_name='Номер урока')
    theme = models.CharField(max_length=50, verbose_name='Тема урока')
    course = models.ForeignKey(Course, null=True, on_delete=models.SET_NULL, verbose_name='Курс')

    def __str__(self):
        return '{} {}'.format(self.number, self.theme)

    # генерация ссылок на урок
    def get_absolute_url(self):
        return reverse('lesson_detail_url', kwargs={'id': self.id})

    def update(self):
        return reverse('lesson_update_url', kwargs={'id': self.id})

    def add_homework(self):
        return reverse('add_homework_url', kwargs={'id': self.id})


class Group(models.Model):
    name = models.CharField(max_length=20, verbose_name='Название группы')
    course = models.ForeignKey(Course, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('group_detail_url', kwargs={'name': self.name})

    def get_group_rating(self):
        return reverse('check_group_rating', kwargs={'name': self.name})

    def get_group_full_stat(self):
        return reverse('check_group_full_stat', kwargs={'name': self.name})

    def teach_group(self):
        return reverse('teach_group', kwargs={'name': self.name})


class User(AbstractUser):
    avatar = models.ImageField(null=True, blank=True, upload_to='media', verbose_name='Аватарка', default='media/default.png')
    user_type = models.ForeignKey(UserType, on_delete=models.CASCADE, null=True, verbose_name='Тип пользвателя')
    username = models.TextField(verbose_name='Имя пользователя', unique=True)
    description = models.TextField(null=True, verbose_name='О себе')
    first_name = models.TextField(verbose_name='Имя')
    last_name = models.TextField(verbose_name='Фамилия')
    score = models.IntegerField(default=0, verbose_name='Балл')

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('user_detail_url', kwargs={'username': self.username})

    def update(self):
        return reverse('user_update_url', kwargs={'username': self.username})


class UserGroup(models.Model):
    group = models.ForeignKey(Group, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)


class TeacherGroup(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    group = models.ForeignKey(Group, null=True, on_delete=models.SET_NULL)


class Test(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='По темам урока')
    theme = models.CharField(max_length=20, verbose_name='Тема тестирования')

    def __str__(self):
        return self.theme

    def get_absolute_url(self):
        return reverse('test_detail_url', kwargs={'id': self.id})

    def check_test_stat(self):
        return reverse('check_test_stat', kwargs={'id': self.id})

    def pass_test(self):
        return reverse('test_pass_url', kwargs={'id': self.id})


class Question(models.Model):
    text = models.CharField(max_length=80, verbose_name='Вопрос')
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    right_answer = models.CharField(max_length=100, verbose_name='Ответ')

    def __str__(self):
        return self.text


class TestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, blank=True)


class UserAnswer(models.Model):
    test = models.ForeignKey(TestResult, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)
    answer = models.CharField(max_length=100, verbose_name='Ответ')


class Homework(models.Model):
    text = models.CharField(max_length=600, verbose_name='Домашнее задание')
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, verbose_name='Урок')
    deadline = models.DateTimeField()


