from django.shortcuts import render
from .models import Lesson, Course, Test, Question, Answer
from django.views.generic import View
from django.shortcuts import redirect

from django.shortcuts import get_object_or_404


from .utils import ObjectDetailMixin
from .forms import CourseForm, LessonForm, QuestionForm, AnswerForm, TestForm

# Create your views here.


class TestCreate(View):
    def get(self, request):

        test_form = TestForm(instance=Question())
        question_forms = [QuestionForm(prefix=str(
            x), instance=Answer()) for x in range(3)]

        answer_forms = [AnswerForm(prefix=str(
            x), instance=Answer()) for x in range(3)]

        template = 'test_create.html'

        context = {'test_form': test_form, 'question_forms': question_forms, 'answer_forms': answer_forms}

        return render(request, template, context)

    def post(self, request):
        test_form = TestForm(request.POST, instance=Test())
        question_forms = [QuestionForm(request.POST, prefix=str(
            x), instance=Question()) for x in range(0, 3)]

        answer_forms = [AnswerForm(prefix=str(
            x), instance=Answer()) for x in range(3)]

        if test_form.is_valid() and all([cf.is_valid() for cf in question_forms]) and all([cf.is_valid() for cf in question_forms]):
            new_test = test_form.save(commit=False)
            new_test.save()
            print('OK')
            for qf in question_forms:
                new_question = qf.save(commit=False)
                new_question.test = new_test
                new_question.save()
                for af in answer_forms:
                    new_answer = af.save(commit=False)
                    new_answer.question = new_question
                    new_answer.save()
            return redirect('test_detail_url', id=new_test.id)

        context = {'test_form': test_form, 'question_forms': question_forms, 'answer_forms': answer_forms}

        return render(request, 'test_create.html', context)


class QuestionCreate(View):
    def get(self, request):

        question_form = QuestionForm(instance=Question())
        answer_forms = [AnswerForm(prefix=str(
            x), instance=Answer()) for x in range(3)]
        template = 'question_create.html'
        context = {'question_form': question_form, 'answer_forms': answer_forms}
        return render(request, template, context)

    def post(self, request):
        question_form = QuestionForm(request.POST, instance=Question())
        answer_forms = [AnswerForm(request.POST, prefix=str(
            x), instance=Answer()) for x in range(0, 3)]
        if question_form.is_valid() and all([cf.is_valid() for cf in answer_forms]):
            new_question = question_form.save(commit=False)
            new_question.save()
            for cf in answer_forms:
                new_choice = cf.save(commit=False)
                new_choice.question = new_question
                new_choice.save()
            return redirect('question_detail_url', id=new_question.id)
        context = {'question_form': question_form, 'answer_forms': answer_forms}

        return render(request, 'question_create.html', context)


class TestDetail(View):
    model = Test
    template = 'test_detail.html'

    def get(self, request, id):
        obj = get_object_or_404(self.model, id__iexact=id)
        return render(request, self.template,
                      context={self.model.__name__.lower(): obj})


class LessonCreate(View):
    def get(self, request):
        form = LessonForm()
        return render(request, 'lesson_create.html', context={'form': form})

    def post(self, request):
        bound_form = LessonForm(request.POST)

        if bound_form.is_valid():
            new_lesson = bound_form.save()
            new_lesson.save()
            return redirect('lesson_detail_url', number=new_lesson.number)

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


class QuestionDetail(ObjectDetailMixin, View):
    model = Question
    template = 'question_detail.html'

    def get(self, request, id):
        question = get_object_or_404(self.model, id__iexact=id)
        return render(request, self.template, context={'question': question})


def lessons_list(request):
    lessons = Lesson.objects.all()
    return render(request, 'lessons_list.html', context={'lessons': lessons})


def courses_list(request):
    courses = Course.objects.all()
    return render(request, 'courses_list.html', context={'courses': courses})

def home_page(request):
    return render(request, 'index.html')




