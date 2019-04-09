from django import forms
from .models import Course
from django.core.exceptions import ValidationError


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
