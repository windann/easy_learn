from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Lesson, Course


class ObjectDetailMixin:
    model = None
    template = None

    def get(self, request, number):
        obj = get_object_or_404(self.model, number__iexact=number)
        return render(request, self.template,
                      context={self.model.__name__.lower(): obj})
