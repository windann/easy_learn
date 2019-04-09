from django.shortcuts import render
from .models import Lesson, Course
from django.views.generic import View
from django.shortcuts import redirect

from django.shortcuts import get_object_or_404


from .utils import ObjectDetailMixin
from .forms import CourseForm

# Create your views here.


class CourseCreate(View):
    def get(self, request):
        form = CourseForm()
        return render(request, 'course_create.html', context={'form': form})

    def post(self, request):
        bound_form = CourseForm(request.POST)

        if bound_form.is_valid():
            new_course = bound_form.save()
            new_course.save()
            return redirect('course_detail_url', name=new_course.name)

        return render(request, 'course_create.html', context={'form': bound_form})


class CourseDetail(ObjectDetailMixin, View):
    model = Course
    template = 'course_detail.html'

    def get(self, request, name):
        course = get_object_or_404(self.model, name__iexact=name)
        lessons = list(Lesson.objects.filter(course=course.id))
        return render(request, self.template, context={'course': course, 'lessons':lessons})


class LessonDetail(ObjectDetailMixin, View):
    model = Lesson
    template = 'lesson_detail.html'


def lessons_list(request):
    lessons = Lesson.objects.all()
    return render(request, 'lessons_list.html', context={'lessons': lessons})


def courses_list(request):
    courses = Course.objects.all()
    return render(request, 'courses_list.html', context={'courses': courses})




