from django.db import models
from django.shortcuts import reverse

# Create your models here.


class Course(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    # генерация ссылок на курс
    def get_absolute_url(self):
        return reverse('course_detail_url', kwargs={'name': self.name})


class Lesson(models.Model):
    number = models.IntegerField()
    theme = models.CharField(max_length=50)
    time = models.TimeField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return '{} {}'.format(self.number, self.theme)

    # генерация ссылок на урок
    def get_absolute_url(self):
        return reverse('lesson_detail_url', kwargs={'id': self.id})


class Test(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    theme = models.CharField(max_length=20)

    def __str__(self):
        return self.theme

    def get_absolute_url(self):
        return reverse('test_detail_url', kwargs={'id': self.id})


class Question(models.Model):
    text = models.CharField(max_length=80)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    right_answer = models.CharField(max_length=100)

    def __str__(self):
        return self.text
