from django import forms
from .models import Course, Lesson, Test, Question
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory


class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = ['name', 'description']

        widgets = {elem: forms.TextInput(attrs={'class': 'form-control'}) for elem in fields}

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
        fields = ['number', 'theme', 'time', 'course']

        widgets = {
            'number': forms.NumberInput(attrs={'class': 'form-control'}),
            'theme': forms.TextInput(attrs={'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'})
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'right_answer']

        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control'}),
            'right_answer': forms.TextInput(attrs={'class': 'form-control'}),
        }


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['lesson', 'theme']

        widgets = {
            'theme': forms.TextInput(attrs={'class': 'form-control'}),
            'lesson': forms.Select(attrs={'class': 'form-control'}),
                   }
