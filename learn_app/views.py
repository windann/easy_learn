from django.shortcuts import render
from .models import Lesson, Course, Test, Question
from django.views.generic import View
from django.shortcuts import redirect

from django.shortcuts import get_object_or_404

from .forms import CourseForm, LessonForm, QuestionForm, TestForm

from django.contrib.auth.forms import UserCreationForm
from  django.views.generic.edit import FormView

# Create your views here.


class RegistrationForm(FormView):
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/account')

    def get(self, request):
        form = UserCreationForm()
        context = {'form':form}
        return render(request, 'registration.html', context)


class TestDelete(View):
    def get(self, request, id):
        test = Test.objects.get(id__iexact=id)
        return render(request, 'test_delete_form.html')


class TestCreate(View):
    def get(self, request):

        test_form = TestForm(instance=Test())
        question_forms = [QuestionForm(prefix=str(
            x), instance=Question()) for x in range(2)]

        template = 'test_create.html'

        context = {'test_form': test_form, 'question_forms': question_forms}

        return render(request, template, context)

    def post(self, request):
        test_form = TestForm(request.POST, instance=Test())

        question_forms = [QuestionForm(request.POST, prefix=str(
            x), instance=Question()) for x in range(2)]

        if test_form.is_valid() and all([qf.is_valid() for qf in question_forms]):
            new_test = test_form.save(commit=False)
            new_test.save()

            for qf in question_forms:
                new_question = qf.save(commit=False)
                new_question.test = new_test
                new_question.save()

            return redirect('test_detail_url', id=new_test.id)

        context = {'test_form': test_form, 'question_forms': question_forms}

        return render(request, 'test_create.html', context)


class LessonCreate(View):
    def get(self, request):
        form = LessonForm()
        return render(request, 'lesson_create.html', context={'form': form})

    def post(self, request):
        bound_form = LessonForm(request.POST)

        if bound_form.is_valid():
            new_lesson = bound_form.save()
            new_lesson.save()
            return redirect('lesson_detail_url', id=new_lesson.id)

        return render(request, 'lesson_create.html', context={'form': bound_form})


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


class TestDetail(View):
    model = Test
    template = 'test_detail.html'

    def get(self, request, id):
        test = get_object_or_404(self.model, id__iexact=id)
        questions = list(Question.objects.filter(test=test.id))

        return render(request, self.template, context={'test': test, 'questions': questions})


class CourseDetail(View):
    model = Course
    template = 'course_detail.html'

    def get(self, request, name):
        course = get_object_or_404(self.model, name__iexact=name)
        lessons = list(Lesson.objects.filter(course=course.id))
        return render(request, self.template, context={'course': course, 'lessons':lessons})


class LessonDetail(View):
    model = Lesson
    template = 'lesson_detail.html'

    def get(self, request, id):
        lesson = get_object_or_404(self.model, id__iexact=id)
        tests = list(Test.objects.filter(lesson= lesson.id))
        return render(request, self.template, context={'lesson': lesson, 'tests': tests})


def lessons_list(request):
    lessons = Lesson.objects.all()
    return render(request, 'lessons_list.html', context={'lessons': lessons})


def courses_list(request):
    courses = Course.objects.all()
    return render(request, 'courses_list.html', context={'courses': courses})


def home_page(request):
    return render(request, 'index.html')




