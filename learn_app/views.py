from django.shortcuts import render
from .models import Lesson, Course, Test, Question, User, UserType, Group, TeacherGroup, UserAnswer, TestResult, Homework, UserGroup
from django.views.generic import View
from django.shortcuts import redirect

from django.shortcuts import get_object_or_404

from .forms import CourseForm, LessonForm, QuestionForm, TestForm, RegistrationForm, PassTestForm, HomeworkForm

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from django.db.models import Count, Max

from collections import Counter

from django.core.exceptions import ObjectDoesNotExist

import random
import operator

from  django.views.generic.edit import FormView

from django.utils.translation import gettext as _


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


def login_view(request):

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm(request)
    return render(request, 'login.html', {'form': form})


class UserDetail(View):
    model = User
    template = 'user_detail.html'

    def get(self, request, username):
        user = get_object_or_404(self.model, username__iexact=username)
        groups = list(TeacherGroup.objects.filter(teacher=user.id))
        return render(request, self.template, context={'user_p': user, 'groups': groups})


class Registration(View):
    def get(self, request):
        form = RegistrationForm()
        template = 'registration.html'
        context = {'form': form}

        return render(request, template, context)

    def post(self, request):
        form = RegistrationForm(request.POST,request.FILES, instance=User())

        if form.is_valid():
            new_user = form.save()
            new_user.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            return redirect('user_detail_url', username=new_user.username)

        context = {'form': form}

        return render(request, 'registration.html', context)


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
            new_test.user = request.user
            new_test.save()

            for qf in question_forms:
                new_question = qf.save(commit=False)
                new_question.test = new_test
                new_question.save()

            return redirect('test_detail_url', id=new_test.id)

        context = {'test_form': test_form, 'question_forms': question_forms}

        return render(request, 'test_create.html', context)


class LessonCreate(View):
    def get(self, request, name):
        form = LessonForm()
        return render(request, 'lesson_create.html', context={'form': form})

    def post(self, request, name):
        bound_form = LessonForm(request.POST)

        if bound_form.is_valid():
            new_lesson = bound_form.save()
            course = get_object_or_404(Course, name__iexact=name)
            new_lesson.course = course
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
        # user = get_object_or_404(User, id=test.user)
        return render(request, self.template, context={'test': test, 'questions': questions })


class CourseDetail(View):
    model = Course
    template = 'course_detail.html'

    def get(self, request, name):
        course = get_object_or_404(self.model, name__iexact=name)
        lessons = list(Lesson.objects.filter(course=course.id))
        return render(request, self.template, context={'course': course, 'lessons': lessons})


class LessonDetail(View):
    model = Lesson
    template = 'lesson_detail.html'

    def get(self, request, id):
        lesson = get_object_or_404(self.model, id__iexact=id)
        tests = list(Test.objects.filter(lesson=lesson.id))
        try:
            homework = Homework.objects.get(lesson=lesson)
        except ObjectDoesNotExist:
            homework = None
        return render(request, self.template, context={'lesson': lesson, 'tests': tests, 'homework': homework})


@login_required
def lessons_list(request):
    lessons = Lesson.objects.all()
    return render(request, 'lessons_list.html', context={'lessons': lessons})


def courses_list(request):
    courses = Course.objects.all()
    return render(request, 'courses_list.html', context={'courses': courses})


def teachers_list(request):
    teachers = User.objects.filter(user_type=1)
    print(list(UserType.objects.all()))
    return render(request, 'teachers_list.html', context={'teachers': teachers})


def home_page(request):
    user = request.user
    if request.user.is_authenticated:
        message = 'Вы авторизованы как ' + str(user.username)
    else:
        message = 'Вы не авторизованы'
    context = {'message': message}
    return render(request, 'index.html', context)


@login_required
def join_to_group(request, name):
    user = request.user
    course = get_object_or_404(Course, name__iexact=name)

    groups = list(Group.objects.filter(course=course.id).order_by('id'))

    if groups:
        group = groups[-1]
        students = list(UserGroup.objects.filter(group=group.id))

        if user.id in [student.user.id for student in students]:
            message = 'Вы уже учитесь на данном курсе!'
            return render(request, 'message.html', context={'message': message})

        if len(students) > 20:

            group_number = int(groups[-1].name.split('_')[-1])
            group_name = '_'.join([name[0] for name in name.split()]) + '_' + (group_number+1)
            new_group = Group(course=course, name=group_name)
            new_group.save()
            group = new_group

    else:
        group_name = '_'.join([name[0] for name in name.split()]) + '_1'
        new_group = Group(course=course, name=group_name)
        new_group.save()
        group = new_group

    user_group = UserGroup(user=user, group=group)
    user_group.save()

    return redirect('group_detail_url', name=group.name)

@login_required
def groups_list(request):
    groups = Group.objects.all()
    return render(request, 'groups_list.html', context={'groups': groups})


class GroupDetail(View):
    model = Group
    template = 'group_detail.html'

    def get(self, request, name):
        group = get_object_or_404(self.model, name__iexact=name)
        students = list(UserGroup.objects.filter(group=group.id))
        try:
            teacher = TeacherGroup.objects.get(group=group.id)
        except ObjectDoesNotExist:
            teacher = None

        return render(request, self.template, context={'students': students, 'group': group, 'teacher': teacher})


class TestPass(View):
    model = Test

    def get(self, request, id):
        questions = list(Question.objects.filter(test=id))
        print(questions)

        test = {}
        for question in questions:
            test[question] = PassTestForm(instance=UserAnswer(), prefix=str(question))

        return render(request, 'test_pass.html', context={'form': test})

    def post(self, request, id):
        test_o = get_object_or_404(self.model, id__iexact=id)
        user = get_object_or_404(User, id__iexact=request.user.id)

        test_result = TestResult(user=user, test=test_o)
        test_result.save()

        questions = list(Question.objects.filter(test=id))
        print(questions)

        test = {}
        for question in questions:
            test[question] = PassTestForm(instance=UserAnswer(), prefix=str(question), data=request.POST)

        print(test.values())
        print(test.keys())

        if all([qf.is_valid() for qf in test.values()]):

            for question, answer in test.items():
                print(answer)
                user_answer = answer.save(commit=False)
                user_answer.question = question
                user_answer.test = test_result
                user_answer.answer = answer.cleaned_data['answer']
                user_answer.save()

            return redirect('check_result', id=test_result.id)

        return render(request, 'test_pass.html', context={'form': test})


def check_test_result(request, id):
    count_right_answers = 0
    test_result = get_object_or_404(TestResult, id__iexact=id)
    answers = list(UserAnswer.objects.filter(test=test_result))

    user = get_object_or_404(User, id__iexact=test_result.user.id)

    all_answers = 0

    for answer in answers:
        question = Question.objects.get(id=answer.question.id)
        right_answer = question.right_answer
        if right_answer == answer.answer:
            count_right_answers += 1
        all_answers += 1

    user.score += count_right_answers
    user.save()

    return render(request, 'test_result.html', context={'result': (count_right_answers/all_answers) * 100})


"""def check_group_statistic(request, name):
    group = get_object_or_404(Group, name__iexact=name)
    students = User.objects.filter(group=group)

    number_of_students = len(students)

    test_results = {}
    test_result_percents = {}
    for student in students:
        #results = {}
        tests = list(TestResult.objects.filter(user=student))
        for test in tests:
            count_right_answers = 0
            answers = UserAnswer.objects.filter(test=test)

            for answer in answers:
                question = Question.objects.get(id=answer.question.id)
                right_answer = question.right_answer
                if right_answer == answer.answer:
                    count_right_answers += 1
            #results[test] = {'answers': answers, 'number_of_right': count_right_answers}
            test_result_percents[test] = {'student': student, 'number_of_right': count_right_answers}

        #test_results[student] = results

    percent_stat = {1: 0, 2: 0, 3: 0, 4: 0}
    for test, number_of_right in test_result_percents.items():

        percent = (number_of_right['number_of_right'] / 2) * 100
        if percent == 100:
            percent_stat[1] += 1
        elif percent < 100 and percent >= 75:
            percent_stat[2] += 1
        elif percent < 75 and percent >= 50:
            percent_stat[3] += 1
        elif percent < 50:
            percent_stat[4] += 1

    percent_stat_list = []

    for percent, count in percent_stat.items():
        percent_stat_list.append([percent, count])

    return render(request, 'test_result.html', context={'result': percent_stat_list, 'number_of_students': number_of_students})"""


def check_group_rating(request, name):
    group = get_object_or_404(Group, name__iexact=name)
    user_groups = list(UserGroup.objects.filter(group=group))

    students = {}

    for user_group in user_groups:
        student = get_object_or_404(User, id__iexact=user_group.user.id)
        students[student] = student.score

    sorted_students = sorted(students.items(), key=operator.itemgetter(1), reverse=True)

    return render(request, 'group_rating.html', context={'students': sorted_students, 'group': group})


def check_group_full_stat(request, name):
    group = get_object_or_404(Group, name__iexact=name)
    user_groups = list(UserGroup.objects.filter(group=group))

    students = {}

    for user_group in user_groups:
        student = get_object_or_404(User, id__iexact=user_group.user.id)
        students[student] = student.score

    test_student = {}

    for student in students:
        tests = TestResult.objects.filter(user=student)
        tries_count = TestResult.objects.filter(user=student).annotate(tries=Count('user'))
        last_try = TestResult.objects.filter(user=student).latest('date')
        answers = UserAnswer.objects.filter(test=last_try)

        last_try_count = 0
        for answer in answers:
            question = Question.objects.get(id=answer.question.id)
            right_answer = question.right_answer
            if right_answer == answer.answer:
                last_try_count += 1

        scores = []

        for test in tests:
            count_right_answers = 0
            answers = UserAnswer.objects.filter(test=test)

            for answer in answers:
                question = Question.objects.get(id=answer.question.id)
                right_answer = question.right_answer
                if right_answer == answer.answer:
                    count_right_answers += 1
            scores.append(count_right_answers)

        test_student[student] = {'number_of_tries': len(tries_count),
                                 'last_try': last_try_count,
                                 'best_try': max(scores),
                                 'worst_try': min(scores),
                                 }

    return render(request, 'group_full_stat.html', context={'tests': test_student})


def check_test_stat(request, id):
    test = get_object_or_404(Test, id__iexact=id)

    test_results = TestResult.objects.filter(test=test)
    result = []
    for test_result in test_results:

        answers = UserAnswer.objects.filter(test=test_result)
        count_right_answers = 0
        for answer in answers:
            question = Question.objects.get(id=answer.question.id)
            right_answer = question.right_answer
            if right_answer == answer.answer:
                count_right_answers += 1

        result.append(count_right_answers)

    result = Counter(result)

    information_for_diagram = []

    for result, count in result.items():
        information_for_diagram.append([result, count])

    return render(request, 'test_stat.html', context={'result': information_for_diagram, 'test': test})


class CourseUpdate(View):
    def get(self, request, name):
        course = get_object_or_404(Course, name__iexact=name)
        form = CourseForm(instance=course)
        return render(request, 'course_update.html', context={'form': form})

    def post(self, request, name):
        course = get_object_or_404(Course, name__iexact=name)
        form = CourseForm(request.POST, instance=course)

        if form.is_valid():
            changed_course = form.save()
            return redirect('course_detail_url', name=changed_course.name)

        return render(request, 'course_update.html', context={'form': form})


class LessonUpdate(View):
    def get(self, request, id):
        lesson = get_object_or_404(Lesson, id__iexact=id)
        form = LessonForm(instance=lesson)
        return render(request, 'lesson_update.html', context={'form': form})

    def post(self, request, id):
        lesson = get_object_or_404(Lesson, id__iexact=id)
        bound_form = LessonForm(request.POST, instance=lesson)

        if bound_form.is_valid():
            changed_lesson = bound_form.save()
            return redirect('lesson_detail_url', id=changed_lesson.id)

        return render(request, 'lesson_update.html', context={'form': bound_form})

"""class UserUpdate(View):
    def get(self, request, username):
        user = get_object_or_404(User, username__iexact=username)
        form = RegistrationForm(instance=user)
        template = 'user_update.html'
        context = {'form': form}

        return render(request, template, context)

    def post(self, request, username):
        user = get_object_or_404(User, username__iexact=username)
        form = RegistrationForm(instance=user)

        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            return redirect('user_detail_url', username=new_user.username)

        context = {'form': form}

        return render(request, 'user_update.html', context)"""


class HomeworkAdd(View):
    def get(self, request, id):
        form = HomeworkForm()
        return render(request, 'homework_create.html', context={'form': form})

    def post(self, request, id):
        form = HomeworkForm(request.POST)
        lesson = get_object_or_404(Lesson, id__iexact=id)

        if form.is_valid():
            new_homework = form.save()
            new_homework.lesson = lesson
            new_homework.save()
            return redirect('lesson_detail_url', id=lesson.id)

        return render(request, 'homework_create.html', context={'form': form})


def get_user_groups(request):
    user = request.user

    if user.user_type.id == 1:
        groups = [user_group.group for user_group in TeacherGroup.objects.filter(teacher=user)]
    else:
        groups = [user_group.group for user_group in UserGroup.objects.filter(user=user)]

    return render(request, 'groups_list.html', context={'groups': groups})


def teach_group(request, name):
    group = get_object_or_404(Group, name__iexact=name)

    try:
        teacher = TeacherGroup.objects.get(group=group, teacher=request.user)

    except ObjectDoesNotExist:
        teacher_group = TeacherGroup(teacher=request.user, group=group)
        teacher_group.save()
        return redirect('group_detail_url', name=group.name)

    else:
        if teacher:
            print('hi')
            message = 'Вы уже обучаете эту группу!'
            return render(request, 'message.html', context={'message': message})




