"""easy_learn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import learn_app.views as view

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', view.home_page, name='home'),

    path('lessons/', view.lessons_list, name='lessons'),
    path('lesson/<str:id>/', view.LessonDetail.as_view(), name='lesson_detail_url'),
    path('lesson/<str:name>/create', view.LessonCreate.as_view(), name='lesson_create_url'),
    path('lesson/<str:id>/update', view.LessonUpdate.as_view(), name='lesson_update_url'),

    path('courses/', view.courses_list, name='courses'),
    path('course/create', view.CourseCreate.as_view(), name='course_create_url'),
    path('course/<str:name>', view.CourseDetail.as_view(), name='course_detail_url'),
    path('course/<str:name>/update/', view.CourseUpdate.as_view(), name='course_update_url'),

    path('test/create', view.TestCreate.as_view(), name='test_create_url'),
    path('pass_test/<str:id>', view.TestPass.as_view(), name='test_pass_url'),
    path('check_test/<str:id>', view.check_test_result, name='check_result'),
    path('test/<str:id>/', view.TestDetail.as_view(), name='test_detail_url'),

    path('registration/', view.Registration.as_view(), name='registration_url'),
    path('user/<str:username>', view.UserDetail.as_view(), name='user_detail_url'),
    # path('user/<str:username>/update', view.UserUpdate.as_view(), name='user_update_url'),
    path('login/', view.login_view, name='login'),
    path('logout/', view.logout_view, name='logout'),

    path('teachers/', view.teachers_list, name='teachers'),

    path('groups/', view.groups_list, name='groups'),
    path('group/<str:name>', view.GroupDetail.as_view(), name='group_detail_url'),
    path('join/<str:name>', view.join_to_group, name='join_group'),

    path('check_group_rating/<str:name>', view.check_group_rating, name='check_group_rating'),
    path('check_group_full_stat/<str:name>', view.check_group_full_stat,
         name='check_group_full_stat'),

    path('check_test_stat/<str:id>', view.check_test_stat, name='check_test_stat'),

    path('add_homework/<str:id>', view.HomeworkAdd.as_view(), name='add_homework_url'),

    path('user_group', view.get_user_groups, name='user_groups'),

    path('teach_group/<str:name>', view.teach_group, name='teach_group')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
