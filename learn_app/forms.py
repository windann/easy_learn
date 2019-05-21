from django import forms
from .models import Course, Lesson, Test, Question, User, UserAnswer, Homework, Material
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'avatar', 'user_type', 'description']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'user_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

        labels = {
            'password2': 'Пароль',
        }


class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = ['name', 'description']

        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'}),
                'description': forms.Textarea(attrs={'class': 'form-control'})
                   }

    def clean_name(self):
        new_name = self.cleaned_data['name'].lower()

        if new_name == 'create':
            raise ValidationError('Придумайте другое название!')

        if Course.objects.filter(name__iexact=new_name).count():
            raise ValidationError('Имя курса должно быть уникальным!')

        return new_name


class LessonForm(forms.ModelForm):

    class Meta:
        model = Lesson
        fields = ['number', 'theme']

        widgets = {
            'number': forms.NumberInput(attrs={'class': 'form-control'}),
            'theme': forms.TextInput(attrs={'class': 'form-control'}),
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'right_answer', 'answers']

        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control'}),
            'right_answer': forms.NumberInput(attrs={'class': 'form-control'}),
            'answers': forms.TextInput(attrs={'class': 'form-control'}),
        }


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['lesson', 'theme']

        widgets = {
            'theme': forms.TextInput(attrs={'class': 'form-control'}),
            'lesson': forms.Select(attrs={'class': 'form-control'}),
                   }


class PassTestForm(forms.ModelForm):
    class Meta:
        model = UserAnswer
        fields = ['answer']

        widgets = {
            'answer': forms.NumberInput(attrs={'class': 'form-control'})
        }


class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ['text', 'deadline']

        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control'}),
            'deadline': forms.DateInput(attrs={'class': 'form-control'}),
        }


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['theme', 'text', 'material_type']

        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control'}),
            'theme': forms.TextInput(attrs={'class': 'form-control'}),
            'material_type': forms.Select(attrs={'class': 'form-control'}),

        }

